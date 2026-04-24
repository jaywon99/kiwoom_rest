# TASK-002: 재사용 가능한 KiwoomClient 라이브러리 개발 및 문서화

## 상태
- 상태: 완료
- commit_approval: status: approved

## 개요
- 다른 프로젝트에서 쉽게 가져다 쓸 수 있도록 키움 OpenAPI 호출 로직을 독립된 클래스 모듈로 분리

## 작업 내역
- `kiwoom_client.py` 생성 및 `KiwoomClient` 클래스 구현
- 토큰 자동 갱신 로직, 하이픈 키워드 매핑 및 빈 파라미터 기본값(default) 채우기 기능 추가
- `main.py` 라우터가 새로 분리된 모듈을 사용하도록 리팩토링
- `kiwoom_client_docs.md` 문서 작성