# TASK-007: 오픈소스 릴리즈를 위한 최종 패키징 완료

## 1. 개요
- **상태**: approved
- **작업자**: Sisyphus
- **목표**: 오픈소스 배포(PyPI 및 GitHub)를 위한 프로젝트 메타데이터 및 라이선스 최종 정비

## 2. 작업 내용
- `LICENSE` (MIT License) 파일 생성 및 명시
- `pyproject.toml`에 라이선스 정보 및 배포용 메타데이터(classifiers) 추가
- `README.md` 문서 내 옛날 패키지명(`kiwoom`)의 오타 잔재들을 `kiwoom_rest`로 전면 교정 및 라이선스 배지 추가

## 3. 커밋 승인
- **commit_approval**: status: approved
- **예상 커밋 메시지**: `chore: 오픈소스 릴리즈를 위한 라이선스 추가 및 문서 최종 교정 (TASK-007)`