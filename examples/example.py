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
BASE_URL = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com")

if not APP_KEY or not SECRET_KEY:
    print("❌ 오류: .env 파일에 KIWOOM_APP_KEY 와 KIWOOM_SECRET_KEY 를 설정해주세요.")
    exit(1)

# ==========================================
# 2. 메인 Client 초기화
# ==========================================
print("🚀 KiwoomClient 초기화 중...")
client = KiwoomClient(appkey=APP_KEY, secretkey=SECRET_KEY, base_url=BASE_URL, acc_id=ACC_ID)

# ==========================================
# 3. [예제] 주식 기본정보 조회 (REST - Dictionary 기반)
# ==========================================
print("\n📊 삼성전자(005930) 정보 조회 중... (Raw Dictionary 호출)")
try:
    # .core.call을 사용해 api_id와 파라미터만 던지면 알아서 Header/Query/Body로 분류하여 호출합니다.
    res_raw = client.core.call(
        api_id="ka10001",  # 주식기본정보조회 (apis.json 참고)
        stk_cd="005930",
    )

    print("✅ 성공! 정보 조회 완료")
    print(f"종목명: {res_raw.get('stk_nm')}")
    print(f"현재가: {res_raw.get('cur_prc')}")
    print("\n[전체 응답 데이터]")
    print(json.dumps(res_raw, indent=2, ensure_ascii=False))

except KiwoomException as ke:
    print(f"❌ 키움증권 에러 발생: [{ke.return_code}] {ke.return_msg}")
except Exception as e:
    print(f"❌ 기타 에러 발생: {e}")

print("\n👋 실행 완료!")
