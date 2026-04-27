import os
import json
from dotenv import load_dotenv
from kiwoom_rest import KiwoomClient, KiwoomException

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
# 2. KiwoomClient (Facade) 초기화
# ==========================================
print("🚀 KiwoomClient 초기화 중...")
client = KiwoomClient(
    appkey=APP_KEY,
    secretkey=SECRET_KEY,
    base_url=BASE_URL,
    acc_id=ACC_ID
)

# ==========================================
# 3. [예제 1] 주식 일봉차트 조회
# ==========================================
print("\n📊 [예제 1] 삼성전자(005930) 정보 조회 중...")
try:
    # Request 객체를 만들지 않고 명시적 파라미터로 직접 값을 넘깁니다.
    res_price = client.stock_daily_chart(
         stk_cd="005930",
         base_dt="20260425",
         upd_stkpc_tp="1"
    )
    
    print("✅ 성공! 정보 조회 완료")
    print(f"최근 종가: {res_price.stk_dt_pole_chart_qry[0].cur_prc}")
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
#     res_order = client.stock_purchase_order(
#         dmst_stex_tp="KRX",    
#         stk_cd="005930",       
#         ord_qty="10",          
#         ord_uv="0",            
#         trde_tp="3"            
#     )
#     
#     print(f"✅ 성공! 주문 결과 확인")
#     print(res_order.model_dump())
#         
# except KiwoomException as ke:
#     print(f"❌ 키움증권 에러 발생: [{ke.return_code}] {ke.return_msg}")
# except Exception as e:
#     print(f"❌ 기타 에러 발생: {e}")

print("\n👋 모든 예제 실행 완료!")
