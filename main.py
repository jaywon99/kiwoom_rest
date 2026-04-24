import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from kiwoom_client import KiwoomClient, KiwoomException

load_dotenv()

APP_KEY = os.getenv("KIWOOM_APP_KEY", os.getenv("KEY", ""))
SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY", os.getenv("SECRET", ""))
ACC_ID = os.getenv("KIWOOM_ACC_ID", os.getenv("ACC_ID", ""))
BASE_URL = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com").rstrip("/")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

CLIENT_CACHE: Dict[str, KiwoomClient] = {}

def get_client(appkey: str, secretkey: str, base_url: str) -> KiwoomClient:
    if appkey not in CLIENT_CACHE:
        CLIENT_CACHE[appkey] = KiwoomClient(appkey=appkey, secretkey=secretkey, base_url=base_url)
    else:
        client = CLIENT_CACHE[appkey]
        if client.secretkey != secretkey or client.base_url != base_url.rstrip("/"):
            CLIENT_CACHE[appkey] = KiwoomClient(appkey=appkey, secretkey=secretkey, base_url=base_url)
            
    return CLIENT_CACHE[appkey]

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
        
    if req_appkey in CLIENT_CACHE:
        client = CLIENT_CACHE[req_appkey]
        res = client.revoke_token()
        CLIENT_CACHE.pop(req_appkey, None)
        return res
    
    return {"status": "ok", "msg": "No active token found"}

@app.post("/api/proxy")
async def proxy_request(req: ApiRequest):
    req_appkey = req.appkey if req.appkey else APP_KEY
    req_secretkey = req.secretkey if req.secretkey else SECRET_KEY
    req_base_url = req.base_url.rstrip('/') if req.base_url else BASE_URL
    
    if not req_appkey or not req_secretkey:
        return {"error": "App Key and Secret Key are required (either in Settings or .env)", "status": 401}

    try:
        client = get_client(req_appkey, req_secretkey, req_base_url)
        
        kwargs = {}
        if req.method.upper() == "GET":
            kwargs["params"] = req.params
        else:
            kwargs["json"] = req.params
            
        resp_data = client.request(req.method, req.path, headers=req.headers, **kwargs)
        
        return {
            "status": 200,
            "headers": resp_data["headers"], 
            "body": resp_data["body"]
        }
    except KiwoomException as ke:
        return {
            "error": f"[{ke.return_code}] {ke.return_msg}",
            "status": ke.status_code,
            "body": {}
        }
    except Exception as e:
        return {"error": str(e), "status": 500, "body": {}}
