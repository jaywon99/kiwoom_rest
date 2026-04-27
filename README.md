# Kiwoom REST API Playground & Python SDK

키움증권 OpenAPI (REST 방식)를 웹 브라우저에서 손쉽게 테스트해 볼 수 있는 **샌드박스 웹 애플리케이션(Playground)**이자, 파이썬(Python) 환경에서 완벽한 타입 힌팅과 자동완성을 지원하는 **강력한 SDK 패키지**입니다.

![Kiwoom API Playground](https://img.shields.io/badge/Kiwoom-REST_API-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.8-009688)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063)

## 🌟 주요 기능 (Features)

### 1. 🛡️ 완벽한 타입 보장 Python SDK (`kiwoom/` 패키지)
- **Pydantic 기반 객체화**: 200여 개의 모든 키움 API 요청/응답 스펙이 순수 파이썬 객체로 정의되어 있습니다. IDE의 자동완성(`.`)을 통해 개발 속도를 압도적으로 단축시킵니다.
- **다중 계층(Nested Tree) 자동 파싱**: 키움 API 특유의 까다로운 응답 배열 구조(예: 일봉차트, 거래내역)를 완벽하게 분석해 하위 리스트(List) 객체로 매핑해 줍니다.
- **스마트한 타입 예외 처리**: 키움증권 서버가 스펙과 다르게 빈 문자열(`""`)이나 빈 배열(`[]`)을 내려보내도 에러 없이 처리하는 자체 방어 로직(`BeforeValidator`)이 탑재되어 있습니다.

### 2. 🚦 통신 안정성 및 WebSocket 실시간 지원
- **토큰 자동 갱신**: 첫 호출 시 Access Token을 발급받고, 만료 시 백그라운드에서 자동으로 갱신(Renew)하여 요청을 이어나갑니다.
- **API 호출 빈도 제한(Rate Limiting)**: 실전투자(초당 5회 미만), 모의투자(초당 1회 미만) 제약에 걸리지 않도록 내부적으로 `Lock`과 `Sleep`을 통해 호출 속도를 안전하게 조절해 줍니다.
- **WebSocket 실시간 연동 지원**: REST API 뿐만 아니라 `websockets` 기반의 비동기 클라이언트(`KiwoomWsClient`)를 내장하여, 실시간 시세 및 조건검색 데이터를 Pydantic 타입으로 안전하게 구독하고 수신할 수 있습니다.

### 3. 🖥️ 웹 기반 API 플레이그라운드
- **자동 폼(Form) 생성**: API를 선택하면 해당 API에 필요한 **요청 파라미터**와 **헤더** 입력 창이 알아서 렌더링됩니다.
- **편리한 세션 로그인**: 서버의 `.env` 파일을 수정할 필요 없이, 웹 화면의 **⚙️ 환경 설정**에서 `App Key`와 `Secret Key`를 한 번만 입력하고 즉시 테스트를 진행할 수 있습니다.

---

## 🚀 시작하기 (How to run)

### 1. 패키지 설치

용도에 따라 두 가지 방식으로 설치할 수 있습니다.

**A. 봇 개발자 (순수 SDK만 필요한 경우)**
```bash
pip install .
```
웹 관련 라이브러리가 제외된 가벼운 코어 통신 모듈만 설치됩니다.

**B. 테스터 및 입문자 (웹 플레이그라운드가 필요한 경우)**
```bash
pip install ".[playground]"
```
API를 브라우저에서 테스트할 수 있도록 FastAPI 및 로컬 웹 서버 환경이 함께 설치됩니다.

### 2. 웹 플레이그라운드 구동 (B 옵션 설치 시)

터미널에 아래 명령어를 입력하면 로컬 서버가 시작됩니다.
```bash
kiwoom-playground
# 또는 ./run.sh 실행
```

브라우저를 열고 `http://localhost:8000` 에 접속합니다. 좌측 하단의 **⚙️ 환경 설정 (OAuth 로그인)** 버튼을 눌러 본인의 키움증권 Key를 입력한 뒤 실험해 보세요!

---

## 💻 Python SDK 사용법 (예제)

웹 서버를 띄우지 않고, 봇이나 데이터 수집 파이프라인에서 `kiwoom` 패키지만 단독으로 떼어다 사용할 수 있습니다.
자세한 사용법은 [kiwoom/docs.md](kiwoom/docs.md) 가이드 문서를 참고하세요.

```python
from kiwoom.client import KiwoomClient
from kiwoom.typed_api import KiwoomTypedClient, StockDailyChartInquiryRequestRequest

# 1. 저수준 통신을 담당하는 Raw Client 초기화
raw_client = KiwoomClient(
    appkey="본인의_APP_KEY", 
    secretkey="본인의_SECRET_KEY",
    base_url="https://api.kiwoom.com"  # 실전투자 URL
)

# 2. 타입 보장을 담당하는 Typed Client 래핑
typed_client = KiwoomTypedClient(raw_client)

# 3. Pydantic 모델을 통한 자동완성 및 API 호출
req = StockDailyChartInquiryRequestRequest(
    stk_cd="005930",
    base_dt="20240425",
    upd_stkpc_tp="1"
)

# 4. 완벽한 타입 힌팅을 지원하는 중첩 응답 객체 반환!
res = typed_client.stock_daily_chart_inquiry_request(req)

for chart_data in res.stk_dt_pole_chart_qry:
    print(f"일자: {chart_data.dt}, 종가: {chart_data.cur_prc}")
```

---

## 📁 프로젝트 구조 (Project Structure)

```text
.
├── 📂 kiwoom_rest/            # 💎 핵심 파이썬 SDK 코어 패키지
│   ├── client.py              # 통신, 토큰 갱신, 웹소켓 등 코어
│   ├── typed_api.py           # 207개 API의 Pydantic 객체 모음
│   └── apis.json              # 크롤링된 API 명세 데이터베이스
│
├── 📂 kiwoom_playground/      # 🖥️ 웹 서버 & CLI 패키지 (Optional)
│   ├── cli.py                 # kiwoom-playground CLI 진입점
│   ├── server.py              # 플레이그라운드 구동 FastAPI 백엔드
│   └── 📂 templates/          # 프론트엔드 UI 화면
│
├── 📂 tools/                  # 🛠️ 스펙 크롤링 및 제너레이터 (업데이트용)
├── 📂 examples/               # 💡 SDK 사용 예제 스크립트 모음
├── pyproject.toml             # 패키지 설정 파일
└── run.sh                     # 간편 실행 쉘 스크립트
```

---

## 🛠 컨트리뷰터 / 스펙 업데이트 (Development)

키움증권에서 새로운 API를 출시했거나 응답 구조가 변경되었다면, 제공된 Tool을 활용하여 Pydantic 모델을 100% 자동 업데이트할 수 있습니다.

```bash
# 1. 키움증권 공식 가이드라인 문서를 긁어와 apis.json에 계층 구조로 저장합니다 (약 5분 소요).
python tools/scrape_apis.py

# 2. 새로 파싱된 apis.json을 바탕으로 kiwoom/typed_api.py 파일을 재생성합니다.
python tools/generate_api_code.py
```
