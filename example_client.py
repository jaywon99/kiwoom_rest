import os
import json
from dotenv import load_dotenv
from kiwoom_client import KiwoomClient, KiwoomException

# ==========================================
# 1. 환경변수(.env) 로드 및 설정
# ==========================================
# 프로젝트 폴더에 있는 .env 파일에서 정보를 읽어옵니다.
# .env 파일 예시:
# KIWOOM_APP_KEY=나의_앱키
# KIWOOM_SECRET_KEY=나의_시크릿키
# KIWOOM_ACC_ID=12345678
# KIWOOM_BASE_URL=https://openapi.kiwoom.com:8282  (실전투자용)
load_dotenv()

APP_KEY = os.getenv("KIWOOM_APP_KEY")
SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY")
ACC_ID = os.getenv("KIWOOM_ACC_ID", "") 
BASE_URL = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com") # 기본 모의투자 URL

if not APP_KEY or not SECRET_KEY:
    print("❌ 오류: .env 파일에 KIWOOM_APP_KEY 와 KIWOOM_SECRET_KEY 를 설정해주세요.")
    exit(1)


# ==========================================
# 2. KiwoomClient 초기화
# ==========================================
# 첫 API 호출 시 알아서 토큰을 발급받고, 만료 시 자동 갱신합니다.
print("🚀 KiwoomClient 초기화 중...")
client = KiwoomClient(
    appkey=APP_KEY,
    secretkey=SECRET_KEY,
    base_url=BASE_URL,
    acc_id=ACC_ID
)


# ==========================================
# 3. [예제 1] 주식 기본정보(현재가 등) 조회 (GET/POST)
# ==========================================
print("\n📊 [예제 1] 삼성전자(005930) 정보 조회 중...")
try:
    # API ID: ka10001 (주식기본정보요청)
    # 헤더나 파라미터를 구분할 필요 없이, 마법의 call() 메서드에 다 던지면 됩니다.
    res_price = client.call(
        api_id="ka10001", 
        stk_cd="039490"  # 종목코드 (키움증권 예시 종목코드)
    )
    
    # 키움증권의 응답 포맷은 API(TR)마다 배열, 딕셔너리 등 다양하게 내려옵니다.
    # 성공적으로 호출되었다면, 전체 응답을 그대로 출력하여 구조를 확인해봅니다.
    print(f"✅ 성공! 정보 조회 완료")
    print(json.dumps(res_price, indent=2, ensure_ascii=False))
    print(f"   (API ID: {res_price.get('api-id')})")
        
except KiwoomException as ke:
    print(f"❌ 키움증권 에러 발생: [{ke.return_code}] {ke.return_msg}")
except Exception as e:
    print(f"❌ 기타 에러 발생: {e}")


# ==========================================
# 4. [예제 2] 주식 매수 주문
# ==========================================
print(f"\n💰 [예제 2] 주식 매수 주문 테스트 중...")
try:
    # API ID: kt10000 (주식 매수주문)
    res_order = client.call(
        api_id="kt10000",
        dmst_stex_tp="KRX",    # 국내거래소구분
        stk_cd="005930",       # 종목코드
        ord_qty="10",          # 주문수량
        ord_uv="0",            # 주문단가 (시장가의 경우 0)
        trde_tp="3"            # 매매구분 (3: 시장가)
    )
    
    print(f"✅ 성공! 주문 결과 확인")
    print(res_order)
        
except KiwoomException as ke:
    print(f"❌ 키움증권 에러 발생: [{ke.return_code}] {ke.return_msg}")
except Exception as e:
    print(f"❌ 기타 에러 발생: {e}")


# (선택) 보안을 위해 로그아웃하여 즉시 토큰을 폐기합니다.
# client.revoke_token()
print("\n👋 모든 예제 실행 완료!")
