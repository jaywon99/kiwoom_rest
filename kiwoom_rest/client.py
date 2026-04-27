from typing import Optional, Dict, Any, Callable
from .core import KiwoomCore
from .generated import KiwoomGeneratedClient

class KiwoomClient(KiwoomGeneratedClient):
    """
    사용자가 직접 import 하여 사용하는 키움증권 최종 메인 클라이언트입니다.
    자동 생성된 모든 API 메서드를 직접 호출할 수 있으며, 
    필요에 따라 자주 쓰는 기능을 수동으로 래핑(Facade)할 수 있습니다.
    """
    def __init__(self, appkey: str, secretkey: str, base_url: str = "https://api.kiwoom.com", ws_url: str = "wss://api.kiwoom.com:10000", acc_id: str = "", apis_spec_path: str = None):
        core = KiwoomCore(appkey, secretkey, base_url, ws_url, acc_id, apis_spec_path)
        super().__init__(core)
        self.core = core

    # =================================================================================
    # 고수준 수동 래핑 API (Facade)
    # 이곳에 사용자가 가장 많이 사용하는 필수 기능(잔고조회, 주문 등)을 추후 추가할 수 있습니다.
    # =================================================================================
    # def get_balance(self): ...
    # def buy_stock(self, ticker: str, qty: int, price: int): ...
