# TASK-005: WebSocket 실시간 시세 연동 및 패키지 분리

## 1. 개요
- **상태**: 완성 (검증 완료)
- **작업자**: Sisyphus
- **목표**: 
  - 기존 REST API 외에 WebSocket(실시간시세, 조건검색) 연동 지원
  - SDK 코어(`kiwoom_rest`)와 웹/CLI(`kiwoom_playground`)를 별도의 패키지로 분리
  - `setuptools_scm`을 도입하여 Git 태그 기반의 자동 버전 관리 구성

## 2. 작업 내용
- `kiwoom_rest/client.py` 내부에 `websockets` 기반의 실시간 통신 로직 및 `connect_ws`, `send_ws` 구현
- `tools/generate_api_code.py` 제너레이터 업데이트
  - WebSocket API를 위한 `async def` 기반 메서드 자동 생성
  - `item` 등 배열 입력 필드의 `List[str]` 강제 타입 적용 (포맷 충돌 버그 해결)
  - 콜백 내부 캐스팅을 위한 `API_ID_TO_RES_MODEL` 동적 레지스트리 추가
- 단일 패키지(`kiwoom-rest`) 및 Optional Dependency(`[playground]`) 구성 (`pyproject.toml`)
- `kiwoom-playground` CLI 진입점 스크립트 작성
- 프로젝트 루트 정리 (`examples/`, 폴더 구조화)

## 3. 검증 (QA)
- [x] CLI (`kiwoom-playground`) 정상 구동 확인
- [x] 웹소켓 URL 커스텀 파라미터 오버라이딩 확인
- [x] Pydantic 모델의 `List[str]` 파싱 및 문자열 방어 로직 검증

## 4. 커밋 승인 (Commit Approval)
- **commit_approval**: status: approved
- **예상 커밋 메시지**: `feat: 웹소켓 실시간 데이터 연동 및 패키지 구조 전면 개편 (TASK-005)`
