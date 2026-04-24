import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import urllib.parse
from datetime import datetime

load_dotenv()

APP_KEY = os.getenv("KIWOOM_APP_KEY", os.getenv("KEY", ""))
SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY", os.getenv("SECRET", ""))
ACC_ID = os.getenv("KIWOOM_ACC_ID", os.getenv("ACC_ID", ""))
BASE_URL = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com").rstrip("/")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

TOKEN_CACHE = {}

def get_token(appkey: str, secretkey: str, base_url: str):
    cache = TOKEN_CACHE.get(appkey)
    if cache and cache["token"] and cache["expires_at"]:
        if datetime.now() < cache["expires_at"]:
            return cache["token"]
            
    resp = requests.post(
        f"{base_url}/oauth2/token",
        json={
            "grant_type": "client_credentials",
            "appkey": appkey,
            "secretkey": secretkey
        },
        headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json"
        }
    )
    if resp.status_code == 200:
        data = resp.json()
        token = data.get("token")
        expires_dt = data.get("expires_dt")
        expires_at = None
        if expires_dt:
            expires_at = datetime.strptime(expires_dt, "%Y%m%d%H%M%S")
        TOKEN_CACHE[appkey] = {"token": token, "expires_at": expires_at}
        return token
    raise Exception(f"Failed to get token: {resp.text}")

class ApiRequest(BaseModel):
    api_id: str
    path: str
    method: str
    headers: Dict[str, str] = {}
    params: Dict[str, Any] = {}
    appkey: Optional[str] = None
    secretkey: Optional[str] = None
    acc_id: Optional[str] = None
    base_url: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")

class LogoutRequest(BaseModel):
    appkey: Optional[str] = None
    secretkey: Optional[str] = None
    base_url: Optional[str] = None

@app.post("/api/logout")
async def logout(req: LogoutRequest):
    req_appkey = req.appkey if req.appkey else APP_KEY
    req_secretkey = req.secretkey if req.secretkey else SECRET_KEY
    req_base_url = req.base_url.rstrip('/') if req.base_url else BASE_URL
    
    if not req_appkey or not req_secretkey:
        return {"status": "ok", "msg": "No keys provided to logout"}
        
    cache = TOKEN_CACHE.get(req_appkey)
    if cache and cache.get("token"):
        token = cache["token"]
        try:
            resp = requests.post(
                f"{req_base_url}/oauth2/revoke",
                json={
                    "appkey": req_appkey,
                    "secretkey": req_secretkey,
                    "token": token
                },
                headers={
                    "Content-Type": "application/json;charset=UTF-8"
                }
            )
            TOKEN_CACHE.pop(req_appkey, None)
            return {"status": "ok", "kiwoom_response": resp.json() if resp.text else {}}
        except Exception as e:
            TOKEN_CACHE.pop(req_appkey, None)
            return {"status": "error", "msg": str(e)}
    
    return {"status": "ok", "msg": "No active token found"}

@app.post("/api/proxy")
async def proxy_request(req: ApiRequest):
    req_appkey = req.appkey if req.appkey else APP_KEY
    req_secretkey = req.secretkey if req.secretkey else SECRET_KEY
    req_base_url = req.base_url.rstrip('/') if req.base_url else BASE_URL
    
    if not req_appkey or not req_secretkey:
        return {"error": "App Key and Secret Key are required (either in Settings or .env)", "status": 401}

    try:
        token = get_token(req_appkey, req_secretkey, req_base_url)
    except Exception as e:
        return {"error": str(e), "status": 500}

    url = f"{req_base_url}{req.path}"
    
    def _do_request(current_token):
        headers = {
            "authorization": f"Bearer {current_token}",
            "appkey": req_appkey,
            "secretkey": req_secretkey,
            "Content-Type": "application/json;charset=UTF-8"
        }
        
        for k, v in req.headers.items():
            if v:
                headers[k] = v

        if req.method.upper() == "GET":
            query_string = urllib.parse.urlencode(req.params)
            req_url = f"{url}?{query_string}" if query_string else url
            return requests.get(req_url, headers=headers)
        else:
            return requests.post(url, headers=headers, json=req.params)

    try:
        resp = _do_request(token)
        body = resp.json() if resp.text else {}
        
        # 만료되거나 유효하지 않은 토큰인 경우 (예: return_code=3, 8005 에러) 자동 갱신 및 재시도
        is_token_invalid = (
            str(body.get("return_code")) == "3" or 
            "인증에 실패" in str(body.get("return_msg", "")) or
            "Token이 유효하지 않습니다" in str(body.get("return_msg", ""))
        )
        
        if is_token_invalid:
            TOKEN_CACHE.pop(req_appkey, None)
            new_token = get_token(req_appkey, req_secretkey, req_base_url)
            resp = _do_request(new_token)
            body = resp.json() if resp.text else {}
            
        return {
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "body": body
        }
    except Exception as e:
        return {"error": str(e), "status": 500}
