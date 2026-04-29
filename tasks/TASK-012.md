# TASK-012: 토큰 발급 API 파라미터명 오류 수정

## 📌 기본 정보
- **상태**: `done`
- **목표**: 토큰 발급 API(`/oauth2/token`) 호출 시 시크릿 키 파라미터명이 `appsecret`으로 오기입된 것을 `secretkey`로 수정하여 [8020] 에러 해결.
- **브랜치**: `fix/TASK-012-fix-token-param`

### 📝 계획 및 진행 (Plan & Progress)
- [x] kiwoom_rest/core.py 파일에서 `appsecret`을 `secretkey`로 수정
- [x] examples/example.py를 통해 정상 발급 테스트

### 🔍 검증 (Verification)
- 관련 파일 및 영향도 파악 완료 여부: [x]
- 테스트 또는 빌드 결과: `tools/check.sh` 통과 완료

### 🚀 커밋 승인 (Commit Approval)
- **상태**: `approved`
- **예상 커밋 메시지**: `fix: 토큰 발급 API 파라미터명 오류(appsecret -> secretkey) 수정 (TASK-012)`
