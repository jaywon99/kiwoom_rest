# Kiwoom Python SDK 사용 가이드

`kiwoom/` 패키지는 키움증권 OpenAPI (REST 방식)를 파이썬에서 가장 안전하고 직관적으로 사용할 수 있도록 설계된 독립적인 SDK 모듈입니다. 

기존의 단순 딕셔너리(`**kwargs`) 기반의 **동적(Dynamic) 호출 방식**과, 새롭게 도입된 Pydantic 기반의 **엄격한 타입(Typed) 호출 방식**을 모두 완벽하게 지원합니다. 본인의 프로젝트 성격에 맞게 두 가지 방식을 섞어서 사용할 수 있습니다.

## ✨ 핵심 기능 (Features)

1. **완전 자동화된 토큰 관리 (`client.py`)**
   첫 호출 시 알아서 Access Token을 발급받으며, 만료되거나 세션이 끊어지면 백그라운드에서 자동으로 새 토큰을 갱신(Renew)하여 기존 요청을 재시도합니다.
2. **강력한 Type Hinting & IDE 자동완성 (`typed_api.py`)**
   모든 200여 개 API의 요청(Request)과 응답(Response)이 Pydantic 객체로 정의되어 있습니다. API 문서를 뒤적일 필요 없이 IDE의 `.`(점) 자동완성을 통해 어떤 필드를 보내고 받을 수 있는지 즉시 확인할 수 있습니다.
3. **완벽한 계층 구조(Nested Model) 파싱**
   평면(Flat) 구조로 파싱하기 까다로운 키움증권의 배열 응답 데이터(예: 일봉차트, 체결내역 등)를 완벽하게 분석하여, **리스트(List) 안의 하위 객체(Sub Model)까지 깊이 있는 구조로 자동 변환**하여 응답합니다.
4. **안전한 타입 호환 (Pydantic Alias)**
   `20stk_ord_alow_amt`처럼 파이썬 변수명 규칙에 어긋나거나(`n_20stk...`), 문서상 오타가 포함된 원본 JSON 키값들도 내부적으로 찰떡같이 파이썬 문법에 맞게 매핑해 줍니다.

---

## 🚀 퀵 스타트: 두 가지 호출 방식

`kiwoom` 패키지는 개발자의 취향에 따라 **기존의 유연한 딕셔너리 방식**과 **새로운 엄격한 객체 방식**을 모두 제공합니다.

### 공통: 클라이언트 초기화
```python
from kiwoom.client import KiwoomClient, KiwoomException
from kiwoom.typed_api import KiwoomTypedClient

# 1. 저수준 통신을 담당하는 Raw Client 초기화
raw_client = KiwoomClient(
    appkey="본인의_APP_KEY", 
    secretkey="본인의_SECRET_KEY",
    base_url="https://api.kiwoom.com"  # 실전투자 URL
)

# 2. 타입 보장을 담당하는 Typed Client 래핑 (선택사항)
typed_client = KiwoomTypedClient(raw_client)
```

---

### 방식 A: [권장] Pydantic 기반 Typed Client 사용법
IDE의 자동완성과 오타 방지 기능을 극대화하고 싶을 때 사용하는 최신 방식입니다.

```python
from kiwoom.typed_api import RequestForBasicStockInformationRequest

try:
    # 1. Pydantic 요청 모델 생성 (자동완성 지원)
    req_model = RequestForBasicStockInformationRequest(
        stk_cd="005930"
    )
    
    # 2. 메서드를 통해 안전하게 호출 -> Response 객체 반환
    res_price = typed_client.request_for_basic_stock_information(req_model)
    
    # 3. 객체 속성(.)으로 안전하게 접근
    print(f"종목명: {res_price.stk_nm}")
    print(f"현재가: {res_price.cur_prc}")
    
except KiwoomException as e:
    print(f"키움 에러: {e.return_msg}")
```

#### 중첩 배열(List) 데이터 다루기
키움증권이 반환하는 복잡한 차트 배열 등은 리스트 내부의 객체 구조까지 타입이 힌팅됩니다.
```python
from kiwoom.typed_api import StockDailyChartInquiryRequestRequest

req_chart = StockDailyChartInquiryRequestRequest(stk_cd="005930", base_dt="20240425")
res_chart = typed_client.stock_daily_chart_inquiry_request(req_chart)

# '주식일봉차트조회' 배열(List) 데이터를 순회
for chart_data in res_chart.stk_dt_pole_chart_qry:
    print(f"일자: {chart_data.dt} / 종가: {chart_data.cur_prc}")
```

---

### 방식 B: [기존] 딕셔너리(`**kwargs`) 기반 Raw Client 사용법
객체를 import 하기 귀찮거나, 동적으로 여러 API를 빠르게 호출하고 싶을 때 사용하는 기존의 유연한 방식입니다.

```python
# API ID와 파라미터만 던지면, 스펙을 참조하여 Header와 Body를 알아서 분류하여 전송합니다.
try:
    res_raw = raw_client.call(
        api_id="ka10001",    # 주식기본정보조회
        stk_cd="005930"      # 파라미터를 kwargs로 무한정 나열 가능
    )
    
    # 응답은 HTTP 헤더와 바디가 합쳐진 평범한 Python 딕셔너리로 반환됩니다.
    print(f"종목명: {res_raw.get('stk_nm')}")
    print(f"현재가: {res_raw.get('cur_prc')}")
    
except KiwoomException as e:
    print(f"키움 에러: {e.return_msg}")
```

#### 동적 라우팅 (API ID 기반 객체 변환)
만약 `**kwargs` 방식의 동적 장점과 Pydantic의 검증 장점을 섞고 싶다면 제공되는 레지스트리를 활용할 수 있습니다.
```python
from kiwoom.typed_api import API_ID_TO_METHOD, API_ID_TO_REQ_MODEL

api_id = "ka10081"
method_name = API_ID_TO_METHOD[api_id]
RequestModelClass = API_ID_TO_REQ_MODEL[api_id]

# 딕셔너리 데이터를 Pydantic으로 자동 캐스팅 & 검증
req_model = RequestModelClass(**my_dynamic_json_dict)
response_model = getattr(typed_client, method_name)(req_model)
```

---

## 🔒 로그아웃 (토큰 즉시 폐기)

사용이 끝난 후 보안을 위해 발급된 토큰을 즉시 폐기하고 싶을 때 사용합니다. 

```python
# 방식 A, B 상관없이 내부 client 객체를 통해 호출
raw_client.revoke_token()
```
