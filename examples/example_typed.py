import os
import json
from dotenv import load_dotenv
from kiwoom_rest.client import KiwoomClient, KiwoomException
from kiwoom_rest.typed_api import KiwoomTypedClient, RequestForBasicStockInformationRequest, StockPurchaseOrderRequest, StockDailyChartInquiryRequestRequest

# ==========================================
# 1. 환경변수(.env) 로드 및 설정
# ==========================================
load_dotenv()

APP_KEY = os.getenv("KIWOOM_APP_KEY")
SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY")
ACC_ID = os.getenv("KIWOOM_ACC_ID", "") 
# 실전투자: https://api.kiwoom.com / 모의투자: https://mockapi.kiwoom.com
BASE_URL = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com")

if not APP_KEY or not SECRET_KEY:
    print("❌ 오류: .env 파일에 KIWOOM_APP_KEY 와 KIWOOM_SECRET_KEY 를 설정해주세요.")
    exit(1)

# ==========================================
# 2. KiwoomTypedClient 초기화
# ==========================================
print("🚀 KiwoomTypedClient 초기화 중...")
client = KiwoomClient(
    appkey=APP_KEY,
    secretkey=SECRET_KEY,
    base_url=BASE_URL,
    acc_id=ACC_ID
)
typed_client = KiwoomTypedClient(client)

# ==========================================
# 3. [예제 1] 주식 기본정보(현재가 등) 조회
# ==========================================
print("\n📊 [예제 1] 삼성전자(005930) 정보 조회 중...")
try:
    # req = RequestForBasicStockInformationRequest(
    #     stk_cd="005930"
    # )
    #
    # res_price = typed_client.request_for_basic_stock_information(req)
    req = StockDailyChartInquiryRequestRequest(
         stk_cd="005930",
         base_dt="20260425",
         upd_stkpc_tp="1"
            )
    
    res_price = typed_client.stock_daily_chart_inquiry_request(req)
    print("✅ 성공! 정보 조회 완료")
    print(res_price.stk_dt_pole_chart_qry[0].cur_prc)
    print(json.dumps(res_price.model_dump(), indent=2, ensure_ascii=False))
        
except KiwoomException as ke:
    print(f"❌ 키움증권 에러 발생: [{ke.return_code}] {ke.return_msg}")
except Exception as e:
    print(f"❌ 기타 에러 발생: {e}")


# ==========================================
# 4. [예제 2] 주식 매수 주문
# ==========================================
# print(f"\n💰 [예제 2] 주식 매수 주문 테스트 중...")
# try:
#     req_order = StockPurchaseOrderRequest(
#         dmst_stex_tp="KRX",    
#         stk_cd="005930",       
#         ord_qty="10",          
#         ord_uv="0",            
#         trde_tp="3"            
#     )
#     res_order = typed_client.stock_purchase_order(req_order)
    
#     print(f"✅ 성공! 주문 결과 확인")
#     print(res_order.model_dump())
        
# except KiwoomException as ke:
#     print(f"❌ 키움증권 에러 발생: [{ke.return_code}] {ke.return_msg}")
# except Exception as e:
#     print(f"❌ 기타 에러 발생: {e}")

print("\n👋 모든 예제 실행 완료!")
