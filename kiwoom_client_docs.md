# KiwoomClient 라이브러리 사용 가이드

`kiwoom_client.py`는 키움증권 OpenAPI (REST 방식)를 파이썬에서 가장 직관적이고 편리하게 사용할 수 있도록 설계된 독립적인 SDK 모듈입니다. 이 파일 하나만 본인의 프로젝트로 복사해 가면 언제 어디서든 강력한 기능들을 활용할 수 있습니다.

## ✨ 핵심 기능 (Features)

1. **완전 자동화된 토큰 관리**: 첫 호출 시 알아서 Access Token을 발급받으며, 만료되거나 세션이 끊어지면 백그라운드에서 자동으로 새 토큰을 갱신(Renew)하여 기존 요청을 재시도합니다.
2. **High-Level API 호출 (`call` 메서드)**: `apis.json` 스펙을 참조하여 Header와 Body/Param을 개발자가 구분할 필요 없이, 파라미터만 쭉 나열하면 라이브러리가 알아서 분류하고 통신합니다.
3. **하이픈(`-`) 키워드 자동 매핑**: 파이썬 문법상 불가능한 `cont-yn` 같은 키움증권 특유의 파라미터들을 `cont_yn`으로 입력해도 알아서 원래 스펙에 맞게 변환해 줍니다.
4. **빈 값(Default) 자동 채움**: 키움 API 특성상 모든 파라미터를 누락 없이 보내야 합니다. 사용자가 입력하지 않은 파라미터는 스펙을 참조하여 기본값(`""`)으로 빈 공간을 꽉 채워서 전송해 줍니다.
5. **계좌번호 자동 주입**: 인스턴스 생성 시 계좌번호를 넣어두면, `CANO`, `acntNo` 등 계좌번호가 필요한 API 호출 시 파라미터를 생략해도 알아서 내 계좌번호를 주입합니다.

---

## 🚀 퀵 스타트 (Quick Start)

### 1. 모듈 임포트 및 초기화
`kiwoom_client.py` 와 `static/apis.json` 파일을 본인 프로젝트에 복사한 뒤 임포트합니다.

```python
from kiwoom_client import KiwoomClient

# 클라이언트 초기화 (토큰은 API 첫 호출 시점에 알아서 발급받습니다)
client = KiwoomClient(
    appkey="본인의_APP_KEY", 
    secretkey="본인의_SECRET_KEY",
    base_url="https://openapi.kiwoom.com:8282", # 실전투자 URL (모의투자는 https://openapivts.kiwoom.com:29443)
    acc_id="12345678"  # 내 계좌번호 (선택사항, 자동 주입용)
)
```

### 2. 마법의 `call` 메서드 사용법
가장 추천하는 사용법입니다. API ID와 필요한 값만 던지면 끝납니다.

```python
# [예시 1] 현재가 조회 (GET 방식 파라미터)
# - API ID : FHKST01010100
# - 스펙상 'tr_id'는 필수 헤더지만, call()에서는 api_id를 던졌으므로 생략해도 자동 주입됩니다.
res_price = client.call(
    api_id="FHKST01010100", 
    FID_COND_MRKT_DIV_CODE="J", 
    FID_INPUT_ISCD="005930"      # 삼성전자
)
print(res_price["body"]["output"])

# [예시 2] 파이썬 친화적인 하이픈 변환 (cont_yn)
# 스펙의 'cont-yn'을 파이썬 문법에 맞게 'cont_yn'으로 던지면 알아서 'cont-yn' Header로 변환됩니다.
res_account = client.call(
    api_id="ka10085",
    cont_yn="N",          
    next_key="",          
    stex_tp="0"           
)

# [예시 3] 현금 매수 주문 (POST 방식 및 계좌번호 자동 주입)
# - CANO 파라미터를 생략했지만, KiwoomClient 초기화 시 넘긴 acc_id("12345678")가 자동으로 주입됩니다.
# - 생략된 나머지 파라미터들도 빈 문자열("")로 알아서 채워져 전송됩니다.
res_order = client.call(
    api_id="TTTC0802U",  
    ACNT_PRDT_CD="01",
    PDNO="005930",
    ORD_DVSN="01",       # 01: 시장가
    ORD_QTY="10",        # 10주
    ORD_UNPR="0"         # 시장가이므로 0원
)
```

---

## 🛠 저수준 (Low-Level) 수동 제어

가이드 문서에 없는 커스텀 API를 호출하거나, Header와 Param을 직접 엄격하게 통제하고 싶을 때는 `get`, `post` 래퍼 메서드를 사용합니다.

```python
# GET 요청 수동 제어
response = client.get(
    path="/uapi/domestic-stock/v1/quotations/inquire-price",
    headers={"tr_id": "FHKST01010100"},
    params={"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": "005930"}
)

# POST 요청 수동 제어
response = client.post(
    path="/uapi/domestic-stock/v1/trading/order-cash",
    headers={"tr_id": "TTTC0802U"},
    json_data={
        "CANO": "12345678",
        "ACNT_PRDT_CD": "01",
        "PDNO": "005930",
        "ORD_DVSN": "01",
        "ORD_QTY": "10",
        "ORD_UNPR": "0"
    }
)
```

---

## 📦 응답 (Response) 포맷

모든 호출 메서드(`call`, `get`, `post`, `request`)는 아래와 같이 통일된 형태의 딕셔너리를 반환합니다. 헤더에 포함된 유용한 정보(연속조회 키 등)를 쉽게 꺼내 쓸 수 있습니다.

```python
{
    "status": 200,                # HTTP 상태 코드 (int)
    "headers": {                  # 응답 헤더 딕셔너리
        "tr_id": "FHKST01010100",
        "tr_cont": "N",
        ...
    },
    "body": {                     # 파싱된 JSON 바디 (dict)
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "output": { ... }
    }
}
```

---

## 🔒 로그아웃 (토큰 즉시 폐기)

사용이 끝난 후 보안을 위해 발급된 토큰을 즉시 폐기하고 싶을 때 사용합니다.

```python
client.revoke_token()
```