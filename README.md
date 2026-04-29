# Kiwoom REST API Playground & Python SDK

키움증권 OpenAPI (REST 방식)를 웹 브라우저에서 테스트할 수 있는 **웹 애플리케이션(Playground)**과, 파이썬(Python) 환경에서 타입 힌팅을 제공하는 **SDK 패키지**입니다.

![Kiwoom API Playground](https://img.shields.io/badge/Kiwoom-REST_API-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.8-009688)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 주요 기능 (Features)

### 1. 타입 힌팅 지원 Python SDK (`kiwoom_rest/` 패키지)
- **직관적인 함수형 호출**: Request 객체를 별도로 생성할 필요 없이, IDE 자동완성 기능을 통해 명시적 파라미터(Named arguments)로 직접 API를 호출할 수 있습니다.
- **Pydantic 기반 객체화**: 200여 개의 키움 API 응답 스펙이 파이썬 객체로 정의되어 있습니다.
- **다중 계층(Nested Tree) 파싱**: 일봉차트, 거래내역 등 계층 구조를 가진 응답 배열을 파이썬 리스트(List) 객체로 자동 매핑합니다.
- **예외 처리 보완**: 서버 응답 중 스펙과 다른 빈 문자열(`""`)이나 빈 배열(`[]`)이 포함된 경우, 런타임 에러를 방지하기 위한 정제 로직(`BeforeValidator`)이 적용되어 있습니다.

### 2. API 호출 제어 및 WebSocket 지원
- **토큰 자동 갱신**: Access Token 발급 후 만료 주기에 맞춰 백그라운드에서 자동으로 갱신(Renew)을 시도합니다.
- **호출 빈도 제한(Rate Limiting)**: 실전투자(초당 5회 미만) 및 모의투자(초당 1회 미만) 기준에 맞추어 내부적으로 `Lock`과 `Sleep`을 통해 호출 간격을 조절합니다.
- **WebSocket 연동**: `websockets` 기반의 비동기 클라이언트를 포함하고 있어, 실시간 시세 및 조건검색 데이터를 구독할 수 있습니다.

### 3. 웹 기반 API 플레이그라운드
- **자동 폼(Form) 렌더링**: 선택한 API 스펙에 맞추어 필요한 파라미터와 헤더 입력 폼이 자동으로 생성됩니다.
- **웹 UI 기반 환경 설정**: 로컬 `.env` 파일을 수정하지 않고도, 웹 화면의 설정 메뉴에서 API Key를 입력하여 테스트 환경을 구성할 수 있습니다.

---

## 시작하기 (How to run)

### 1. 패키지 설치

용도에 따라 다음 방식으로 설치할 수 있습니다.

**A. SDK 코어 모듈만 필요한 경우**
```bash
pip install kiwoom-playground
```
웹 관련 의존성을 제외한 통신 모듈만 설치됩니다.

**B. 웹 플레이그라운드 포함 설치**
```bash
pip install "kiwoom-playground[playground]"
```
브라우저 테스트를 위한 FastAPI 및 웹 서버 환경이 함께 설치됩니다.

### 2. 웹 플레이그라운드 구동 (B 옵션 설치 시)

터미널에서 아래 명령어를 실행하여 로컬 서버를 시작합니다.
```bash
kiwoom-playground
# 또는 ./run.sh 실행
```

브라우저에서 `http://localhost:8000`에 접속한 뒤, 좌측 하단의 환경 설정에서 키움증권 Key를 입력하여 테스트할 수 있습니다.

---

## Python SDK 사용 예제

별도의 웹 서버 구동 없이 파이썬 스크립트에서 `kiwoom_rest` 패키지를 단독으로 사용할 수 있습니다.
상세한 사용법은 `examples/` 폴더 및 `kiwoom_rest/docs.md` 문서를 참고하세요.

### 방법 1. 자동완성을 지원하는 객체 기반 호출 (추천)
모든 응답이 파이썬 객체로 매핑되어, 오타 없이 안전하게 개발할 수 있습니다.

```python
from kiwoom_rest import KiwoomClient, KiwoomException

# 1. KiwoomClient 초기화
client = KiwoomClient(
    appkey="본인의_APP_KEY",
    secretkey="본인의_SECRET_KEY",
    base_url="https://api.kiwoom.com"  # 실전투자 URL
)

try:
    # 2. 명시적 파라미터를 통한 직관적인 API 호출 (IDE 자동완성 지원)
    res_price = client.stock_daily_chart(
        stk_cd="005930",
        base_dt="20240425",
        upd_stkpc_tp="1"
    )

    # 3. Pydantic을 통해 파싱된 중첩 응답 객체 사용
    recent_data = res_price.stk_dt_pole_chart_qry[0]
    print(f"일자: {recent_data.dt}, 종가: {recent_data.cur_prc}")

except KiwoomException as ke:
    print(f"키움증권 에러 발생: [{ke.return_code}] {ke.return_msg}")
```

### 방법 2. 유연한 확장을 위한 Core 직접 호출 (Dictionary 기반)
스펙이 변경되었거나 Pydantic 모델을 거치지 않고 Raw Dictionary(`dict`) 형태로 직접 파라미터를 넘기고 응답을 받고 싶은 경우, `.core.call` 메서드를 사용할 수 있습니다.

```python
from kiwoom_rest import KiwoomClient, KiwoomException

# 1. KiwoomClient 초기화
client = KiwoomClient(
    appkey="본인의_APP_KEY",
    secretkey="본인의_SECRET_KEY",
    base_url="https://api.kiwoom.com"
)

try:
    # 2. .core.call()에 API ID와 파라미터만 던지면 Header/Query/Body를 자동 분류하여 호출
    res_raw = client.core.call(
        api_id="ka10001",  # 주식기본정보조회 (apis.json 참고)
        stk_cd="005930",
    )

    # 3. 순수 파이썬 Dictionary 형식으로 데이터 접근
    print(f"종목명: {res_raw.get('stk_nm')}")
    print(f"현재가: {res_raw.get('cur_prc')}")

except KiwoomException as ke:
    print(f"키움증권 에러 발생: [{ke.return_code}] {ke.return_msg}")
```

---

## 프로젝트 구조

```text
.
├── kiwoom_rest/            # 파이썬 SDK 코어 패키지
│   ├── client.py           # 통합 클라이언트 래퍼
│   ├── core.py             # 통신, 토큰 관리, 웹소켓 코어 모듈
│   ├── generated.py        # API Pydantic 모델 및 메서드 정의 (자동 생성됨)
│   └── apis.json           # 크롤링된 API 명세 데이터
│
├── kiwoom_playground/      # 웹 서버 & CLI 패키지 (Optional)
│   ├── cli.py              # CLI 진입점
│   ├── server.py           # FastAPI 백엔드
│   └── templates/          # 프론트엔드 UI 화면
│
├── tools/                  # 스펙 크롤링 및 코드 제너레이터
├── examples/               # SDK 사용 예제 스크립트
├── pyproject.toml          # 패키지 설정 파일
└── run.sh                  # 실행 쉘 스크립트
```

---

## 스펙 업데이트 (Development)

키움증권 API 구조가 변경되었을 경우, 내장된 스크립트를 통해 Pydantic 모델을 업데이트할 수 있습니다.

```bash
# 1. 최신 API 문서를 크롤링하여 apis.json에 저장 (약 5분 소요)
python tools/scrape_apis.py

# 2. 갱신된 apis.json을 바탕으로 kiwoom_rest/generated.py 재생성
python tools/generate_api_code.py
```
