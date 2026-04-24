import os
import json
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Optional

class KiwoomClient:
    """
    키움증권 OpenAPI (REST) 사용을 위한 파이썬 클라이언트 모듈.
    토큰 발급/자동 갱신 및 기본 헤더 주입을 처리하며, 재사용 가능합니다.
    """
    def __init__(self, appkey: str, secretkey: str, base_url: str = "https://api.kiwoom.com", acc_id: str = "", apis_spec_path: str = None):
        self.appkey = appkey
        self.secretkey = secretkey
        self.base_url = base_url.rstrip("/")
        self.acc_id = acc_id
        
        self._token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        
        self.apis_spec = {}
        self._load_apis_spec(apis_spec_path)

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

    def _get_token(self) -> str:
        """
        토큰이 없거나 만료된 경우 새로 발급받고, 유효하면 캐시된 토큰을 반환합니다.
        """
        if self._token and self._token_expires_at and datetime.now() < self._token_expires_at:
            return self._token
            
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
        if resp.status_code == 200:
            data = resp.json()
            self._token = data.get("token")
            expires_dt = data.get("expires_dt")
            if expires_dt:
                self._token_expires_at = datetime.strptime(expires_dt, "%Y%m%d%H%M%S")
            return self._token
        raise Exception(f"Failed to get token: {resp.text}")

    def revoke_token(self) -> Dict[str, Any]:
        """
        현재 발급된 토큰을 즉시 폐기(로그아웃)합니다.
        """
        if not self._token:
            return {"status": "ok", "msg": "No active token found"}
            
        try:
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
            self._token = None
            self._token_expires_at = None
            return {"status": "ok", "kiwoom_response": resp.json() if resp.text else {}}
        except Exception as e:
            self._token = None
            self._token_expires_at = None
            return {"status": "error", "msg": str(e)}

    def request(self, method: str, path: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        API를 호출합니다.
        **kwargs를 통해 json, params 등 requests 라이브러리가 지원하는 인자를 유연하게 전달할 수 있습니다.
        자동으로 토큰을 갱신하고 필수 인증 헤더를 주입합니다.
        
        Returns:
            Dict: {
                "status": HTTP Status Code (int),
                "headers": Response Headers (dict),
                "body": Response Body (dict)
            }
        """
        token = self._get_token()
        url = f"{self.base_url}{path}"
        
        req_headers = {
            "authorization": f"Bearer {token}",
            "appkey": self.appkey,
            "secretkey": self.secretkey,
            "Content-Type": "application/json;charset=UTF-8"
        }
        
        if headers:
            for k, v in headers.items():
                if v:
                    req_headers[k] = v
                    
        def _do_request(current_token):
            req_headers["authorization"] = f"Bearer {current_token}"
            return requests.request(method=method, url=url, headers=req_headers, **kwargs)

        try:
            resp = _do_request(token)
            body = resp.json() if resp.text else {}
            
            is_token_invalid = (
                str(body.get("return_code")) == "3" or 
                "인증에 실패" in str(body.get("return_msg", "")) or
                "Token이 유효하지 않습니다" in str(body.get("return_msg", ""))
            )
            
            if is_token_invalid:
                self._token = None
                self._token_expires_at = None
                new_token = self._get_token()
                resp = _do_request(new_token)
                body = resp.json() if resp.text else {}
                
            return {
                "status": resp.status_code,
                "headers": dict(resp.headers),
                "body": body
            }
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
        API ID(예: FHKST01010100)와 파라미터들만 전달받아, apis.json 스펙을 참조하여 
        알아서 header와 param(혹은 json)으로 분리하여 호출해주는 고수준(High-level) 메서드입니다.
        
        계좌번호(CANO 등)를 별도로 입력하지 않았다면, 클래스 생성 시 받은 self.acc_id로 자동 할당합니다.
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
                
        is_tr_id_required_but_missing = "tr_id" in spec_header_map and "tr_id" not in [k.lower() for k in req_headers.keys()]
        if is_tr_id_required_but_missing:
            req_headers["tr_id"] = api_id
            
        if self.acc_id:
            for account_key in ["cano", "acntno"]:
                if account_key in spec_param_map:
                    original_key = spec_param_map[account_key]
                    if original_key not in req_params:
                        req_params[original_key] = self.acc_id

        if method == "GET":
            return self.request("GET", path, headers=req_headers, params=req_params)
        else:
            return self.request(method, path, headers=req_headers, json=req_params)
