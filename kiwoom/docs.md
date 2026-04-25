# Kiwoom Python SDK 사용 가이드

`kiwoom/` 패키지는 키움증권 OpenAPI (REST 방식)를 파이썬에서 가장 안전하고 직관적으로 사용할 수 있도록 설계된 독립적인 SDK 모듈입니다. 

기존의 단순 딕셔너리(`**kwargs`) 기반 호출을 넘어, **Pydantic(Type Hinting) 기반의 강력한 모델 시스템**을 도입하여 IDE 자동완성과 타입 검증을 완벽하게 지원합니다. 이 `kiwoom/` 폴더 전체를 본인의 프로젝트로 복사해 가면 다른 어떤 봇이나 웹 서버에서도 즉시 활용할 수 있습니다.

## ✨ 핵심 기능 (Features)

1. **강력한 Type Hinting & IDE 자동완성 (`typed_api.py`)**
   모든 200여 개 API의 요청(Request)과 응답(Response)이 Pydantic 객체로 정의되어 있습니다. API 문서를 뒤적일 필요 없이 IDE의 `.`(점) 자동완성을 통해 어떤 필드를 보내고 받을 수 있는지 즉시 확인할 수 있습니다.
2. **완벽한 계층 구조(Nested Model) 파싱**
   평면(Flat) 구조로 파싱하기 까다로운 키움증권의 배열 응답 데이터(예: 일봉차트, 체결내역 등)를 완벽하게 분석하여, **리스트(List) 안의 하위 객체(Sub Model)까지 깊이 있는 구조로 자동 변환**하여 응답합니다.
3. **안전한 타입 호환 (Pydantic Alias)**
   `20stk_ord_alow_amt`처럼 파이썬 변수명 규칙에 어긋나거나(`n_20stk...`), 문서상 오타가 포함된 원본 JSON 키값들도 내부적으로 찰떡같이 파이썬 문법에 맞게 매핑해 줍니다.
4. **완전 자동화된 토큰 관리 (`client.py`)**
   첫 호출 시 알아서 Access Token을 발급받으며, 만료되거나 세션이 끊어지면 백그라운드에서 자동으로 새 토큰을 갱신(Renew)하여 기존 요청을 재시도합니다.

---

## 🚀 퀵 스타트 (Quick Start)

### 1. 모듈 임포트 및 초기화
`kiwoom` 패키지에서 저수준 통신을 담당하는 `KiwoomClient`와, 타입 보장을 담당하는 `KiwoomTypedClient`를 함께 불러와 결합합니다.

```python
from kiwoom.client import KiwoomClient, KiwoomException
from kiwoom.typed_api import KiwoomTypedClient
from kiwoom.typed_api import RequestForBasicStockInformationRequest, StockPurchaseOrderRequest

# 1. 저수준 통신 클라이언트 초기화
raw_client = KiwoomClient(
    appkey="본인의_APP_KEY", 
    secretkey="본인의_SECRET_KEY",
    base_url="https://api.kiwoom.com"  # 실전투자 URL
)

# 2. 강력한 타입이 보장되는 클라이언트로 래핑
typed_client = KiwoomTypedClient(raw_client)
```

### 2. 완벽한 자동완성과 함께 API 호출하기
더 이상 `api_id`("ka10001")를 외울 필요가 없습니다. 직관적인 영문 메서드와 모델을 활용하세요.

```python
# [예시 1] 주식 기본정보 조회 (단일 객체 응답)
try:
    # 1. Pydantic 요청 모델 생성 (필수 파라미터 체크 및 자동완성 지원)
    req_model = RequestForBasicStockInformationRequest(
        stk_cd="005930"
    )
    
    # 2. 메서드를 통해 안전하게 호출 -> Response 객체 반환
    res_price = typed_client.request_for_basic_stock_information(req_model)
    
    # 3. 딕셔너리['키'] 방식이 아닌, 객체 속성(.)으로 안전하게 접근!
    print(f"종목명: {res_price.stk_nm}")
    print(f"현재가: {res_price.cur_prc}")
    print(f"전일대비: {res_price.pred_pre}")
    
except KiwoomException as e:
    print(f"키움 에러: {e.return_msg}")
```

### 3. 복잡한 배열(List) 객체 다루기
키움증권이 반환하는 복잡한 차트 데이터 배열 등도 리스트와 내부 Pydantic 모델로 아름답게 변환됩니다.

```python
from kiwoom.typed_api import StockDailyChartInquiryRequestRequest

req_chart = StockDailyChartInquiryRequestRequest(
    stk_cd="005930",
    base_dt="20240425"
)
res_chart = typed_client.stock_daily_chart_inquiry_request(req_chart)

# '주식일봉차트조회' 배열(List) 데이터를 순회하며 내부 객체에 접근
for chart_data in res_chart.stk_dt_pole_chart_qry:
    print(f"일자: {chart_data.dt} / 종가: {chart_data.cur_prc} / 거래량: {chart_data.trde_qty}")
```

---

## 🛠 저수준 (Low-Level) 동적 제어 및 예외 처리

만약 Pydantic 모델을 사용하지 않고 기존 방식처럼 `**kwargs`로 딕셔너리 통신을 하고 싶거나, 동적으로 API를 제어해야 한다면 `API_ID_TO_METHOD` 레지스트리나 기존 `client.call()`을 활용할 수 있습니다.

### 1. 예외(Exception) 핸들링
서버가 정상 응답(200 OK)을 주었더라도 인증 실패나 장 종료, 잔고 부족 등 비즈니스 로직 에러로 인해 `return_code` 값이 `"0"`이 아닌 경우, 결괏값을 반환하지 않고 즉시 **`KiwoomException`을 발생(raise)**시킵니다.

```python
try:
    res = typed_client.stock_purchase_order(req)
except KiwoomException as e:
    print(f"에러코드: {e.return_code}") # 예: OPW00004
    print(f"에러메시지: {e.return_msg}")
    print(f"HTTP상태: {e.status_code}")
```

### 2. 동적 라우팅 (API ID 기반)
웹 서버 프록시처럼 `api_id` 문자열 값만 가지고 유동적으로 타입 체크와 호출을 해야 할 경우, 제공되는 `API_ID_TO_METHOD`, `API_ID_TO_REQ_MODEL` 딕셔너리를 활용합니다.

```python
from kiwoom.typed_api import API_ID_TO_METHOD, API_ID_TO_REQ_MODEL

api_id = "ka10081"
method_name = API_ID_TO_METHOD[api_id]
RequestModelClass = API_ID_TO_REQ_MODEL[api_id]

# 딕셔너리 기반으로 모델 생성
req_model = RequestModelClass(**my_raw_json_data)

# 동적 메서드 호출
method = getattr(typed_client, method_name)
response_model = method(req_model)
```

---

## 🔒 로그아웃 (토큰 즉시 폐기)

사용이 끝난 후 보안을 위해 발급된 토큰을 즉시 폐기하고 싶을 때 사용합니다. Pydantic 클라이언트의 내부 `client` 객체를 통해 직접 호출합니다.

```python
typed_client.client.revoke_token()
```
