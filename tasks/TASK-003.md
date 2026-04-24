# TASK-003: KiwoomClient 응답 포맷 통일 및 에러 핸들링 고도화

## 상태
- 상태: 완료
- commit_approval: status: approved

## 개요
- 라이브러리 응답에서 무의미한 HTTP 상태코드를 제거하고, 헤더와 바디를 통합하여 사용 편의성 증대
- 한국투자증권(KIS) API의 잔재 코드 및 설명(rt_cd, FHKST01010100 등) 완벽 제거
- 서버 논리 에러(return_code != 0) 발생 시 `KiwoomException`을 발생시키는 구조로 통일

## 작업 내역
- `KiwoomException` 커스텀 예외 클래스 도입
- `kiwoom_client.py` 내 `_check_kiwoom_error` 공통 에러 검증 함수 추가
- `client.call()`의 응답을 헤더+바디 병합 딕셔너리로 변경하고, `apis.json` 스펙 기반의 헤더만 필터링
- `example_client.py` 및 `kiwoom_client_docs.md` 문서 내 한국투자증권 잔재 제거 및 예외 처리 가이드 추가
- `main.py` 라우터 에러 캐치 로직 개선