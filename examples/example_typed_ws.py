import os
import asyncio
from dotenv import load_dotenv
from kiwoom_rest import (
    KiwoomClient, 
    KiwoomException,
    API_ID_TO_RES_MODEL
)
from kiwoom_rest.generated import (
    StockSigningRequest_Data
)

# ==============================================================================
# 1. 환경 설정 로드
# ==============================================================================
load_dotenv()
APP_KEY = os.getenv("KIWOOM_APP_KEY")
SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY")
BASE_URL = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com")

if not APP_KEY or not SECRET_KEY:
    print("❌ 오류: .env 파일에 KIWOOM_APP_KEY 와 KIWOOM_SECRET_KEY 를 설정해주세요.")
    exit(1)


async def main():
    # ==============================================================================
    # 2. 메인 Client 초기화
    # ==============================================================================
    print("🚀 KiwoomClient 초기화 중...")
    client = KiwoomClient(appkey=APP_KEY, secretkey=SECRET_KEY, base_url=BASE_URL)

    # ==============================================================================
    # 3. 실시간 데이터 수신 콜백 (자동 타입 캐스팅 패턴)
    # ==============================================================================
    async def on_event(raw_data: dict):
        """
        수신된 원시 JSON 딕셔너리를 자동으로 Pydantic 객체로 변환하여 출력하는 마법의 함수입니다.
        """
        data_list = raw_data.get("data", [])
        if not data_list:
            return
            
        # 1. 메시지의 종류(TR 명)를 파악합니다. (예: "0B" -> 주식체결)
        tr_type = data_list[0].get("type")
        
        # 2. 동적 레지스트리(API_ID_TO_RES_MODEL)에서 해당 TR에 맞는 Pydantic 응답 클래스를 찾습니다.
        ResponseClass = API_ID_TO_RES_MODEL.get(tr_type)
        
        if ResponseClass:
            # 3. 딕셔너리를 해당 클래스로 언패킹하여 객체화합니다.
            res_obj = ResponseClass(**raw_data)
            print(f"\n[자동 파싱 완료 - TR: {tr_type}]")
            
            # 이후에는 res_obj.data[0].values.n_10 (현재가) 처럼 안전하게 접근할 수 있습니다.
            print(res_obj)
        else:
            print("\n[알 수 없는 타입]", raw_data)

    # ==============================================================================
    # 4. 웹소켓 연결 및 서버 로그인 대기
    # ==============================================================================
    print("\n🔗 웹소켓 연결 중...")
    await client.connect_ws(on_message=on_event)
    print("✅ 웹소켓 연결 완료! (서버 로그인 처리 대기 중...)")
    
    # [중요] 연결 직후 서버 인증 시간을 위해 반드시 1초 이상 대기합니다.
    await asyncio.sleep(1.0)

    # ==============================================================================
    # 5. 실시간 구독 요청 전송
    # ==============================================================================
    print("\n📡 구독 요청 전송 중...")
    # Request 객체를 만들지 않고 인자로 직접 넘깁니다. 
    # (data 파라미터는 Pydantic 객체 리스트를 넘겨도 내부에서 직렬화됩니다)
    await client.stock_signing(
        trnm="REG",
        grp_no="g123",
        refresh="1",
        data=[
            StockSigningRequest_Data(item=["005930"], type=["0B"])
        ]
    )
    print("✅ 전송 완료! 실시간 수신 대기 중... (10초 후 자동 종료됩니다)")
    
    # ==============================================================================
    # 6. 메인 루프 유지 및 종료
    # ==============================================================================
    await asyncio.sleep(10)
    
    print("👋 웹소켓 연결을 종료합니다.")
    await client.disconnect_ws()

if __name__ == "__main__":
    asyncio.run(main())
