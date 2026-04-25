import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from kiwoom.client import KiwoomClient, KiwoomException
from kiwoom.typed_api import KiwoomTypedClient, API_ID_TO_METHOD, API_ID_TO_REQ_MODEL

load_dotenv()

APP_KEY = os.getenv("KIWOOM_APP_KEY", os.getenv("KEY", ""))
SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY", os.getenv("SECRET", ""))
ACC_ID = os.getenv("KIWOOM_ACC_ID", os.getenv("ACC_ID", ""))
BASE_URL = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com").rstrip("/")

app = FastAPI()

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

class LogoutRequest(BaseModel):
    appkey: Optional[str] = None
    secretkey: Optional[str] = None
    base_url: Optional[str] = None

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

@app.get("/api/apis_spec")
async def get_apis_spec():
    return FileResponse("kiwoom/apis.json")

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
        typed_client = KiwoomTypedClient(client)
        
        api_id = req.api_id
        if api_id in API_ID_TO_METHOD and api_id in API_ID_TO_REQ_MODEL:
            method_name = API_ID_TO_METHOD[api_id]
            RequestModelClass = API_ID_TO_REQ_MODEL[api_id]
            
            # headers와 params를 하나로 병합하여 Pydantic 모델 검증
            combined_data = {**req.headers, **req.params}
            req_model = RequestModelClass(**combined_data)
            
            # TypedClient의 명시적 메서드 동적 호출
            method = getattr(typed_client, method_name)
            response_model = method(req_model)
            
            return {
                "status": 200,
                "body": response_model.model_dump()
            }
        else:
            return {"error": f"Unknown API ID: {api_id}", "status": 400}

    except KiwoomException as ke:
        return {
            "error": f"[{ke.return_code}] {ke.return_msg}",
            "status": ke.status_code,
            "body": {}
        }
    except Exception as e:
        return {"error": str(e), "status": 500, "body": {}}
