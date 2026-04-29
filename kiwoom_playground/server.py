import os
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from kiwoom_rest import KiwoomClient, KiwoomException, API_ID_TO_METHOD, API_ID_TO_REQ_MODEL

load_dotenv()

APP_KEY = os.getenv("KIWOOM_APP_KEY", os.getenv("KEY", ""))
SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY", os.getenv("SECRET", ""))
ACC_ID = os.getenv("KIWOOM_ACC_ID", os.getenv("ACC_ID", ""))
BASE_URL = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com").rstrip("/")
WS_URL = os.getenv("KIWOOM_BASE_WS_URL", os.getenv("WS_URL", "wss://api.kiwoom.com:10000")).rstrip("/")

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(CURRENT_DIR, "templates"))

CLIENT_CACHE: Dict[str, KiwoomClient] = {}


def get_client(appkey: str, secretkey: str, base_url: str, ws_url: str = "") -> KiwoomClient:
    ws_url = ws_url or WS_URL
    if appkey not in CLIENT_CACHE:
        CLIENT_CACHE[appkey] = KiwoomClient(appkey=appkey, secretkey=secretkey, base_url=base_url, ws_url=ws_url)
    else:
        client = CLIENT_CACHE[appkey]
        if (
            client.core.secretkey != secretkey
            or client.core.base_url != base_url.rstrip("/")
            or client.core.ws_url != ws_url.rstrip("/")
        ):
            CLIENT_CACHE[appkey] = KiwoomClient(appkey=appkey, secretkey=secretkey, base_url=base_url, ws_url=ws_url)

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
    import kiwoom_rest

    apis_path = os.path.join(os.path.dirname(kiwoom_rest.__file__), "apis.json")
    return FileResponse(apis_path)


@app.post("/api/logout")
async def logout(req: LogoutRequest):
    req_appkey = req.appkey if req.appkey else APP_KEY
    req_secretkey = req.secretkey if req.secretkey else SECRET_KEY

    if not req_appkey or not req_secretkey:
        return {"status": "ok", "msg": "No keys provided to logout"}

    if req_appkey in CLIENT_CACHE:
        client = CLIENT_CACHE[req_appkey]
        res = client.core.revoke_token()
        CLIENT_CACHE.pop(req_appkey, None)
        return res

    return {"status": "ok", "msg": "No active token found"}


@app.post("/api/proxy")
async def proxy_request(req: ApiRequest):
    req_appkey = req.appkey if req.appkey else APP_KEY
    req_secretkey = req.secretkey if req.secretkey else SECRET_KEY
    req_base_url = req.base_url.rstrip("/") if req.base_url else BASE_URL

    if not req_appkey or not req_secretkey:
        return {"error": "App Key and Secret Key are required (either in Settings or .env)", "status": 401}

    try:
        client = get_client(req_appkey, req_secretkey, req_base_url)

        api_id = req.api_id
        if api_id in API_ID_TO_METHOD and api_id in API_ID_TO_REQ_MODEL:
            method_name = API_ID_TO_METHOD[api_id]
            RequestModelClass = API_ID_TO_REQ_MODEL[api_id]

            combined_data = {**req.headers, **req.params}
            req_model = RequestModelClass(**combined_data)

            method = getattr(client, method_name)
            import inspect

            if inspect.iscoroutinefunction(method):
                return {"error": "This is a WebSocket API. Please use /api/ws_proxy.", "status": 400}

            # Request 객체의 필드를 언패킹하여 전달
            response_model = method(**req_model.model_dump(by_alias=False, exclude_none=True))

            return {"status": 200, "body": response_model.model_dump()}
        else:
            return {"error": f"Unknown API ID: {api_id}", "status": 400}

    except KiwoomException as ke:
        return {"error": f"[{ke.return_code}] {ke.return_msg}", "status": ke.status_code, "body": {}}
    except Exception as e:
        return {"error": str(e), "status": 500, "body": {}}


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, list[WebSocket]] = {}
        self.kiwoom_clients: Dict[str, KiwoomClient] = {}

    async def connect(
        self,
        websocket: WebSocket,
        appkey: str,
        secretkey: str,
        base_url: str,
        ws_url: str = "wss://api.kiwoom.com:10000",
    ):
        if appkey not in self.active_connections:
            self.active_connections[appkey] = []
        self.active_connections[appkey].append(websocket)

        if appkey not in self.kiwoom_clients or not self.kiwoom_clients[appkey].core._is_ws_connected:
            rest_client = get_client(appkey, secretkey, base_url, ws_url=ws_url)
            self.kiwoom_clients[appkey] = rest_client

            async def on_message(data: dict):
                to_remove = []
                for ws in self.active_connections.get(appkey, []):
                    try:
                        await ws.send_json(data)
                    except Exception:
                        to_remove.append(ws)
                for ws in to_remove:
                    self.disconnect(ws, appkey)

            try:
                await rest_client.connect_ws(on_message)
            except Exception as e:
                await websocket.send_json({"error": f"Kiwoom WS connect failed: {e}"})
                self.disconnect(websocket, appkey)
                await websocket.close()
                return

    def disconnect(self, websocket: WebSocket, appkey: str):
        if appkey in self.active_connections:
            if websocket in self.active_connections[appkey]:
                self.active_connections[appkey].remove(websocket)
            if not self.active_connections[appkey]:
                client = self.kiwoom_clients.pop(appkey, None)
                if client:
                    asyncio.create_task(client.disconnect_ws())

    async def send_to_kiwoom(self, appkey: str, payload: dict):
        client = self.kiwoom_clients.get(appkey)
        if client and client.core._is_ws_connected:
            await client.core.send_ws(payload)


ws_manager = ConnectionManager()


@app.websocket("/api/ws_proxy")
async def websocket_proxy(websocket: WebSocket):
    await websocket.accept()

    try:
        init_data = await websocket.receive_json()
        appkey = init_data.get("appkey") or APP_KEY
        secretkey = init_data.get("secretkey") or SECRET_KEY
        base_url = init_data.get("base_url") or BASE_URL
        base_url = base_url.rstrip("/")

        ws_url = init_data.get("ws_url")
        if not ws_url:
            ws_url = WS_URL
        ws_url = ws_url.rstrip("/")

        if not appkey or not secretkey:
            await websocket.send_json({"error": "App Key and Secret Key are required"})
            await websocket.close(code=1008)
            return

        await ws_manager.connect(websocket, appkey, secretkey, base_url, ws_url)
        await websocket.send_json({"status": "connected", "msg": "WebSocket proxy connected"})

        while True:
            payload = await websocket.receive_json()
            if payload.get("action") == "send":
                await ws_manager.send_to_kiwoom(appkey, payload.get("data", {}))

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WS proxy error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass
    finally:
        try:
            if "appkey" in locals() and appkey:
                ws_manager.disconnect(websocket, appkey)
        except Exception:
            pass
