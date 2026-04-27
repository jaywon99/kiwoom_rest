# TASK-008: API 명칭 생성 규칙 개선 (번역 오류 및 축약어 정상화)

## 상태
- [x] 완료

## 목적
- `tools/generate_api_code.py` 의 `clean_base_name` 함수에서 단어의 일부(Substring)를 잘못 지워서(`StockPurchaseOrder` -> `stock_purchaseder` 등) 영문법이 파괴되는 현상 수정.
- 구글 번역기에 의해 파편화된 용어 통일 (`ForEachAccount`, `ByAccount` -> `ByAccount`).

## 작업 내역
1. **정규식 리팩토링**: `clean_base_name` 로직을 CamelCase 단어 쪼개기(split) 기반으로 변경하여 정확히 일치하는 불필요한 단어(`request`, `for`, `of` 등)만 제거하도록 수정.
2. **Context 유지**: `details`(상세) 같은 의미론적으로 중요한 단어는 `stopwords`에서 제외하여 API 뉘앙스를 보존.
3. **용어 통일**: `EachAccount` -> `ByAccount` 변환 로직 추가.
4. **수동 오버라이드 지원**: `AccessTokenIssuance` -> `IssueAccessToken` 처럼 자연스러운 동사형 작명을 위해 수동 매핑(`overrides` dict) 기능 추가.
5. **결과 문서화**: 자동 생성된 API 이름 전후 비교표(`api_names_comparison.md`) 생성 로직 분리.

## Commit Approval
commit_approval: status: approved
