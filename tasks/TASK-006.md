# TASK-006: 스펙 문서 기반 자동 타입 매핑 및 예제 고도화

## 1. 개요
- **상태**: approved
- **작업자**: Sisyphus
- **목표**: 
  - 키움증권 OpenAPI 공식 문서의 데이터 타입을 파싱하여 Pydantic 모델에 동적으로 반영
  - 4가지 SDK 사용 시나리오별 튜토리얼 예제 코드 작성

## 2. 작업 내용
- `tools/scrape_apis.py` 수정: 공식 문서의 3번째 컬럼(타입 정보)을 파싱하여 `apis.json`에 저장
- `tools/generate_api_code.py` 수정: 
  - 하드코딩된 타입 추론 로직 제거
  - `String[]`, `int`, `String` 등 원본 타입 명세를 `SafeListStr`, `SafeInt`, `SafeStr` 방어형 타입으로 1:1 매핑
- SDK 사용자를 위한 상세 주석이 포함된 4개의 예제 스크립트 작성
  - `example.py` (Raw REST)
  - `example_typed.py` (Typed REST)
  - `example_ws.py` (Raw WS)
  - `example_typed_ws.py` (Typed WS)
- 불필요한 임시 크롤링 테스트 파일 삭제

## 3. 검증 (QA)
- [x] Pydantic 제너레이터 정상 빌드 및 `apis.json` 타입 컬럼 반영 확인
- [x] 4종 예제 스크립트 구문(Syntax) 오류 검사 및 동작 로직 점검 완료

## 4. 커밋 승인 (Commit Approval)
- **commit_approval**: status: approved
- **예상 커밋 메시지**: `refactor: 스펙 시트 기반 동적 타입 매핑 적용 및 예제 코드 추가 (TASK-006)`