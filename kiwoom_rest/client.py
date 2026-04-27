import os
import json
import time
import threading
import asyncio
import requests
import websockets
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Optional, Callable

class KiwoomException(Exception):
    """
    키움증권 API 호출 중 발생하는 예외를 처리하는 커스텀 클래스입니다.
    HTTP 오류 뿐만 아니라 서버 내부의 비즈니스 로직(return_code != 0) 오류도 포함합니다.
    """
    def __init__(self, return_code: str, return_msg: str, status_code: int = 200):
        self.return_code = return_code
        self.return_msg = return_msg
        self.status_code = status_code
        super().__init__(f"[{return_code}] {return_msg} (HTTP Status: {status_code})")

class KiwoomClient:
    """
    키움증권 OpenAPI (REST) 사용을 위한 파이썬 클라이언트 모듈.
    토큰 발급/자동 갱신 및 기본 헤더 주입을 처리하며, 재사용 가능합니다.
    """
    def __init__(self, appkey: str, secretkey: str, base_url: str = "https://api.kiwoom.com", ws_url: str = "wss://api.kiwoom.com:10000", acc_id: str = "", apis_spec_path: str = None):
        self.appkey = appkey
        self.secretkey = secretkey
        self.base_url = base_url.rstrip("/")
        
        custom_ws_url = ws_url.rstrip("/")
        if custom_ws_url.endswith("/api/dostk/websocket"):
            self.ws_url = custom_ws_url
        else:
            self.ws_url = f"{custom_ws_url}/api/dostk/websocket"
            
        self.acc_id = acc_id
        
        self._token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        
        # API 호출 빈도 제한 (Rate Limit) 설정
        self._lock = threading.Lock()
        self._last_call_time = 0.0
        
        # 모의투자(mock)는 초당 1회 미만 (안전하게 1.2초), 실전투자는 초당 5회 미만 (안전하게 0.25초)
        if "mock" in self.base_url.lower():
            self._call_delay = 1.2
        else:
            self._call_delay = 0.25
            
        self.apis_spec = {}
        self._load_apis_spec(apis_spec_path)
        
        self._ws = None
        self._ws_listen_task = None
        self._on_message_callback = None
        self._is_ws_connected = False

    def _wait_for_rate_limit(self):
        """키움증권 API 호출 빈도 제한을 준수하기 위해 대기합니다."""
        with self._lock:
            now = time.time()
            elapsed = now - self._last_call_time
            if elapsed < self._call_delay:
                time.sleep(self._call_delay - elapsed)
            self._last_call_time = time.time()

    def _load_apis_spec(self, apis_spec_path: Optional[str]):
        if not apis_spec_path:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            possible_paths = [
                os.path.join(base_dir, 'apis.json'),
                os.path.join(base_dir, 'static', 'apis.json'),
                os.path.join(base_dir, '..', 'static', 'apis.json')
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    apis_spec_path = p
                    break
                    
        if apis_spec_path and os.path.exists(apis_spec_path):
            try:
                with open(apis_spec_path, 'r', encoding='utf-8') as f:
                    spec_list = json.load(f)
                    for api in spec_list:
                        self.apis_spec[api['id']] = api
            except Exception as e:
                print(f"[Warn] Failed to load apis.json from {apis_spec_path}: {e}")

    def _check_kiwoom_error(self, resp: requests.Response) -> Dict[str, Any]:
        if not resp.ok:
            raise KiwoomException(
                return_code=f"HTTP_{resp.status_code}", 
                return_msg=resp.text, 
                status_code=resp.status_code
            )
            
        body = resp.json() if resp.text else {}
        return_code = str(body.get("return_code", "0"))
        
        if return_code != "0":
            return_msg = body.get("return_msg", "Unknown Kiwoom Error")
            raise KiwoomException(
                return_code=return_code, 
                return_msg=return_msg, 
                status_code=resp.status_code
            )
            
        return body

    def _get_token(self) -> str:
        """
        토큰이 없거나 만료된 경우 새로 발급받고, 유효하면 캐시된 토큰을 반환합니다.
        """
        if self._token and self._token_expires_at and datetime.now() < self._token_expires_at:
            return self._token
            
        self._wait_for_rate_limit()
        resp = requests.post(
            f"{self.base_url}/oauth2/token",
            json={
                "grant_type": "client_credentials",
                "appkey": self.appkey,
                "secretkey": self.secretkey
            },
            headers={
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "application/json"
            }
        )
        
        body = self._check_kiwoom_error(resp)
        self._token = body.get("token")
        expires_dt = body.get("expires_dt")
        if expires_dt:
            self._token_expires_at = datetime.strptime(expires_dt, "%Y%m%d%H%M%S")
        return self._token

    async def connect_ws(self, on_message: Callable[[Dict[str, Any]], Any]):
        if self._is_ws_connected:
            return

        self._on_message_callback = on_message
        
        token = self._get_token()
        headers = {
            "authorization": f"Bearer {token}",
            "appkey": self.appkey,
            "secretkey": self.secretkey
        }

        self._ws = await websockets.connect(self.ws_url, additional_headers=headers)
        
        # [수정] 웹소켓 접속 직후 'LOGIN' 페이로드 전송 (키움 공식 스펙 반영)
        auth_payload = {
            "trnm": "LOGIN",
            "token": token
        }
        await self._ws.send(json.dumps(auth_payload))
        # 인증 처리를 위한 아주 짧은 대기
        await asyncio.sleep(0.1)

        self._is_ws_connected = True
        self._ws_listen_task = asyncio.create_task(self._listen_ws())

    async def _listen_ws(self):
        try:
            async for message in self._ws:
                if self._on_message_callback:
                    try:
                        data = json.loads(message)
                    except json.JSONDecodeError:
                        data = {"raw": message}
                    
                    # [신규 추가] 서버의 PING(생존 확인) 메시지 자동 에코 응답
                    if data.get("trnm") == "PING":
                        asyncio.create_task(self.send_ws(data))
                        
                    if asyncio.iscoroutinefunction(self._on_message_callback):
                        await self._on_message_callback(data)
                    else:
                        self._on_message_callback(data)
        except websockets.exceptions.ConnectionClosed:
            self._is_ws_connected = False
        except Exception as e:
            self._is_ws_connected = False
            print(f"WebSocket listening error: {e}")

    async def send_ws(self, payload: Dict[str, Any]):
        if not self._is_ws_connected or not self._ws:
            raise Exception("WebSocket is not connected")
            
        await self._ws.send(json.dumps(payload))

    async def disconnect_ws(self):
        if self._ws:
            await self._ws.close()
        if self._ws_listen_task:
            self._ws_listen_task.cancel()
        self._is_ws_connected = False

    def revoke_token(self) -> Dict[str, Any]:
        """
        현재 발급된 토큰을 즉시 폐기(로그아웃)합니다.
        """
        if not self._token:
            return {"status": "ok", "msg": "No active token found"}
            
        try:
            self._wait_for_rate_limit()
            resp = requests.post(
                f"{self.base_url}/oauth2/revoke",
                json={
                    "appkey": self.appkey,
                    "secretkey": self.secretkey,
                    "token": self._token
                },
                headers={
                    "Content-Type": "application/json;charset=UTF-8"
                }
            )
            body = self._check_kiwoom_error(resp)
            self._token = None
            self._token_expires_at = None
            return body
        except Exception:
            self._token = None
            self._token_expires_at = None
            raise

    def request(self, method: str, path: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        API를 호출합니다.
        **kwargs를 통해 json, params 등 requests 라이브러리가 지원하는 인자를 유연하게 전달할 수 있습니다.
        자동으로 토큰을 갱신하고 필수 인증 헤더를 주입합니다.
        
        Returns:
            Dict: {
                "headers": Response Headers (dict),
                "body": Response Body (dict)
            }
        Raises:
            Exception: HTTP 에러(200번대가 아님) 또는 네트워크 에러 발생 시
        """
        token = self._get_token()
        url = f"{self.base_url}{path}"
        
        req_headers = {
            "authorization": f"Bearer {token}",
            "Content-Type": "application/json;charset=UTF-8"
        }
        
        if headers:
            for k, v in headers.items():
                if v:
                    req_headers[k] = v
                    
        def _do_request(current_token):
            req_headers["authorization"] = f"Bearer {current_token}"
            self._wait_for_rate_limit()
            return requests.request(method=method, url=url, headers=req_headers, **kwargs)

        try:
            resp = _do_request(token)
            
            body_for_check = resp.json() if resp.text else {}
            is_token_invalid = (
                str(body_for_check.get("return_code")) == "3" or 
                "인증에 실패" in str(body_for_check.get("return_msg", "")) or
                "Token이 유효하지 않습니다" in str(body_for_check.get("return_msg", ""))
            )
            
            if is_token_invalid:
                self._token = None
                self._token_expires_at = None
                new_token = self._get_token()
                resp = _do_request(new_token)
                
            body = self._check_kiwoom_error(resp)
            
            return {
                "headers": dict(resp.headers),
                "body": body
            }
        except KiwoomException:
            raise
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")

    def get(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """GET 요청 래퍼"""
        return self.request("GET", path, headers=headers, params=params, **kwargs)

    def post(self, path: str, headers: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """POST 요청 래퍼"""
        return self.request("POST", path, headers=headers, json=json_data, **kwargs)

    def call(self, api_id: str, **kwargs) -> Dict[str, Any]:
        """
        API ID(예: ka10001)와 파라미터들만 전달받아, apis.json 스펙을 참조하여 
        알아서 header와 param(혹은 json)으로 분리하여 호출해주는 고수준(High-level) 메서드입니다.
        """
        if api_id not in self.apis_spec:
            raise ValueError(f"Unknown API ID: {api_id}. Please ensure apis.json is loaded properly or check the ID.")
            
        spec = self.apis_spec[api_id]
        method = spec["method"].upper()
        path = spec["path"]
        
        spec_header_map = {}
        req_headers = {}
        for h in spec.get("headers", []):
            orig_key = h["key"]
            lower_key = orig_key.lower()
            spec_header_map[lower_key] = orig_key
            spec_header_map[lower_key.replace("-", "_")] = orig_key
            req_headers[orig_key] = str(h.get("default", ""))
            
        spec_param_map = {}
        req_params = {}
        for p in spec.get("params", []):
            orig_key = p["key"]
            lower_key = orig_key.lower()
            spec_param_map[lower_key] = orig_key
            spec_param_map[lower_key.replace("-", "_")] = orig_key
            req_params[orig_key] = p.get("default", "")
        
        for k, v in kwargs.items():
            k_lower = k.lower()
            
            if k_lower in spec_header_map:
                req_headers[spec_header_map[k_lower]] = str(v)
            elif k_lower in spec_param_map:
                req_params[spec_param_map[k_lower]] = v
            else:
                req_params[k] = v
                
        if "api-id" in spec_header_map:
            orig_api_id_key = spec_header_map["api-id"]
            if not req_headers.get(orig_api_id_key):
                req_headers[orig_api_id_key] = api_id
            
        if method == "GET":
            raw_resp = self.request("GET", path, headers=req_headers, params=req_params)
        else:
            raw_resp = self.request(method, path, headers=req_headers, json=req_params)
            
        final_res = raw_resp["body"]
        
        for h_key, h_val in raw_resp["headers"].items():
            h_lower = h_key.lower()
            if h_lower in spec_header_map:
                final_res[spec_header_map[h_lower]] = h_val
                
        return final_res
