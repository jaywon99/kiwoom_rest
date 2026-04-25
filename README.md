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

### 2. 🚦 통신 안정성 (Auto-Token & Rate Limit)
- **토큰 자동 갱신**: 첫 호출 시 Access Token을 발급받고, 만료 시 백그라운드에서 자동으로 갱신(Renew)하여 요청을 이어나갑니다.
- **API 호출 빈도 제한(Rate Limiting)**: 실전투자(초당 5회 미만), 모의투자(초당 1회 미만) 제약에 걸리지 않도록 내부적으로 `Lock`과 `Sleep`을 통해 호출 속도를 안전하게 조절해 줍니다.

### 3. 🖥️ 웹 기반 API 플레이그라운드
- **자동 폼(Form) 생성**: API를 선택하면 해당 API에 필요한 **요청 파라미터**와 **헤더** 입력 창이 알아서 렌더링됩니다.
- **편리한 세션 로그인**: 서버의 `.env` 파일을 수정할 필요 없이, 웹 화면의 **⚙️ 환경 설정**에서 `App Key`와 `Secret Key`를 한 번만 입력하고 즉시 테스트를 진행할 수 있습니다.

---

## 🚀 시작하기 (How to run)

### 1. 요구 사항
- Python 3.9 이상
- 키움증권 OpenAPI App Key 및 Secret Key (키움증권 개발자 포털에서 발급)

### 2. 설치 및 실행

```bash
# 1. 저장소 클론 및 이동
git clone <repository-url>
cd kiwoom-playground

# 2. 파이썬 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # Windows의 경우: .venv\Scripts\activate

# 3. 의존성 패키지 설치
pip install -r requirements.txt

# 4. 서버 실행 (플레이그라운드 구동 시)
./run.sh
```

### 3. 웹 플레이그라운드 접속
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
├── 📂 kiwoom/                 # 💎 핵심 파이썬 SDK 패키지 (이것만 복사해 사용 가능)
│   ├── client.py              # 통신, 토큰 갱신, 빈도 제한 제어
│   ├── typed_api.py           # 207개 API의 Pydantic 입출력 객체 및 Client
│   ├── apis.json              # 크롤링된 API 명세 데이터베이스
│   └── docs.md                # SDK 상세 사용 가이드
│
├── 📂 tools/                  # 🛠️ 개발 도구 (업데이트용)
│   ├── scrape_apis.py         # 키움증권 가이드 페이지 크롤러
│   └── generate_api_code.py   # apis.json을 바탕으로 typed_api.py 코드를 찍어내는 제너레이터
│
├── 📂 templates/              # 플레이그라운드 프론트엔드 UI 화면
├── main.py                    # 플레이그라운드를 구동하기 위한 FastAPI 서버
└── example.py                 # SDK 사용 예제 스크립트
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
