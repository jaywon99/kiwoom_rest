# TASK-004: API 응답 객체화(Pydantic) 및 패키지 구조 리팩토링

## 상태
- 상태: 완료
- commit_approval: status: approved

## 개요
- API 호출 시 `**kwargs`에 의존하던 방식을 개선하여, Pydantic 기반의 강력한 타입 시스템(Type Hinting)을 도입
- 키움증권 OpenAPI 명세의 Flat Table 구조를 분석하여 `- ` 기호를 기반으로 List 내부 객체(Nested Tree)까지 파싱하도록 자동화 로직 고도화
- 프로젝트 구조를 SDK 형태로 분리하여 타 프로젝트 이식성 증대

## 작업 내역
- `kiwoom/` 패키지 신설: `kiwoom/client.py`, `kiwoom/typed_api.py`, `kiwoom/apis.json`, `kiwoom/docs.md`
- `tools/` 스크립트 모음 폴더 신설: `scrape_apis.py`, `generate_api_code.py`
- 크롤러(`scrape_apis.py`): `- ` 접두사를 분석하여 계층 구조(Tree) 파싱 기능 추가 및 한국어 API명 영문 번역(`deep-translator`) 추가
- 생성기(`generate_api_code.py`): 동적 Request/Response Pydantic 모델 자동 생성 및 `KiwoomTypedClient` 래퍼 코드 작성
- `main.py` 및 `templates/index.html`: `/api/apis_spec` 엔드포인트 신설을 통한 스펙 로드 로직 변경 및 동적 Proxy 호출 시 TypedClient 적용
- `example.py`: `KiwoomTypedClient`를 사용하는 모범 예제로 최신화