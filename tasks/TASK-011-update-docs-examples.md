# TASK-011: 변경된 패키지 구조에 따른 문서 및 예제 코드 갱신

## 1. 개요
- 변경된 `kiwoom_rest` 구조(`typed_api.py` 병합 등)를 반영하여 가이드 문서와 예제 소스 코드 수정

## 2. 작업 목록
- [x] `kiwoom_rest/docs.md` 내용 최신화 (병합된 `KiwoomClient` 사용법 위주로 재작성)
- [x] 웹소켓 예제(`example_ws.py`, `example_typed_ws.py`) 에러 핸들링 보강

## 3. 작업 결과
- 모든 문서가 현재 아키텍처와 일치함
- 웹소켓 예제 구동 시 설정값 누락에도 크래시 없이 정상 에러 출력됨
