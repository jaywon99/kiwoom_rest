# Kiwoom REST API Playground

키움증권 OpenAPI (REST 방식)를 웹 브라우저에서 손쉽게 테스트해 볼 수 있는 샌드박스 웹 애플리케이션입니다. 

Postman이나 Swagger와 유사한 **세로 3단 레이아웃**을 제공하며, 키움증권 가이드 페이지를 분석하여 **200여 개의 모든 API 명세를 자동으로 구성**해 두었습니다.

![Kiwoom API Playground](https://img.shields.io/badge/Kiwoom-REST_API-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.8-009688)

## 🌟 주요 기능 (Features)

- **207개 API 스펙 기본 내장**: `국내주식 (시세, 차트, 주문 등)` 등 키움 API 전체 항목을 카테고리별로 묶어 두었습니다.
- **자동 폼(Form) 생성**: API를 클릭하면 해당 API에 필요한 **요청 파라미터**와 **헤더** 입력 창이 알아서 렌더링됩니다.
- **편리한 브라우저 세션 로그인**: 서버의 `.env` 파일을 수정할 필요 없이, 브라우저 화면의 **⚙️ 환경 설정**에서 `App Key`와 `Secret Key`를 입력하고 즉시 테스트할 수 있습니다. (입력한 정보는 브라우저 로컬스토리지에 Base64로 난독화되어 보관됩니다.)
- **토큰 자동 관리 및 캐싱**: 키움증권 OAuth2 접근 토큰(Access Token)을 백엔드가 알아서 발급받고 갱신하며, 사용자의 App Key별로 캐싱합니다.
- **철저한 로그아웃(토큰 폐기)**: 로그아웃 시 브라우저 정보를 지울 뿐만 아니라, 키움 서버(`au10002`)를 호출하여 실제 접근 토큰을 무효화(Revoke)시켜 보안을 챙겼습니다.
- **공인 IP 실시간 표기**: 키움증권 포털에 '내 IP'를 등록하기 편하도록 툴 하단에 실시간으로 접속 공인 IP를 띄워줍니다.
- **계좌번호 자동 완성**: 환경 설정에 `Account ID`를 등록해두면, API 중 `acctNo` 등의 계좌번호 파라미터가 자동으로 채워집니다.

## 🚀 시작하기 (How to run)

### 1. 요구 사항 (Prerequisites)
- Python 3.9 이상
- 키움증권 OpenAPI App Key 및 Secret Key (키움증권 개발자 포털에서 발급)

### 2. 설치 및 실행 (Installation)

```bash
# 1. 저장소 클론 및 이동
git clone <repository-url>
cd kiwoom-playground

# 2. 파이썬 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # Windows의 경우: .venv\Scripts\activate

# 3. 의존성 패키지 설치
pip install -r requirements.txt

# 4. 서버 실행
./run.sh
# (또는 uvicorn main:app --reload)
```

### 3. 접속
브라우저를 열고 `http://localhost:8000` 에 접속합니다.
좌측 하단의 **⚙️ 환경 설정 (OAuth 로그인)** 버튼을 눌러 본인의 키움증권 Key를 입력한 뒤 마음껏 실험해 보세요!

## 📁 프로젝트 구조 (Project Structure)
```text
.
├── main.py                # FastAPI 백엔드 메인 로직 및 API Proxy (토큰 발급 포함)
├── scrape_apis.py         # 키움증권 가이드 페이지 크롤링 스크립트
├── run.sh                 # 서버 구동 쉘 스크립트
├── requirements.txt       # 파이썬 의존성
├── static/
│   └── apis.json          # 스크래퍼가 생성한 200여개의 API 명세 DB
└── templates/
    └── index.html         # 3-Pane 레이아웃의 프론트엔드 UI 화면
```

## 🛠 문제 해결 (Troubleshooting)
- **실행(Execute)을 눌렀을 때 401 또는 오류가 난다면?**
  - 키움증권 포털에 현재 표시되고 있는 **접속 공인 IP**가 화이트리스트에 정상적으로 등록되어 있는지 확인해주세요.
  - 모의투자/실전투자 Base URL 설정이 올바른지 확인해주세요.
- **API 목록을 최신화하고 싶다면?**
  - 터미널에서 `python scrape_apis.py` 를 실행하시면 키움 웹사이트에서 최신 파라미터 규격을 다시 스크래핑하여 `static/apis.json`을 덮어씁니다.