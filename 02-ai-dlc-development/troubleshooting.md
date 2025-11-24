# 문제 해결 및 FAQ

AI-DLC 워크샵에서 자주 발생하는 문제와 해결 방법을 정리했습니다.

## 설치 관련 문제

### spec-kit 설치 오류

**Q: `uv tool install` 시 권한 오류 발생**

```bash
# uv 업데이트
curl -LsSf https://astral.sh/uv/install.sh | sh

# 재시도
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

**Q: Python 버전 오류**

```bash
# Python 3.12 설치
uv python install 3.12
uv python pin 3.12
```

### OpenSpec 설치 오류

**Q: `npm install -g` 시 권한 오류**

```bash
# macOS/Linux
sudo npm install -g @fission-ai/openspec@latest

# 또는 nvm 사용 (권장)
nvm install 18
nvm use 18
npm install -g @fission-ai/openspec@latest
```

**Q: Node.js 버전 부족**

```bash
# Node.js 18+ 설치
# macOS
brew install node

# Ubuntu
sudo apt update && sudo apt install nodejs npm
```

## 초기화 관련 문제

### spec-kit 초기화 문제

**Q: `specify init` 후 폴더가 생성되지 않음**

```bash
# 수동으로 폴더 생성
mkdir -p .specify/memory
touch .specify/memory/constitution.md
touch .specify/memory/specification.md
touch .specify/memory/plan.md
touch .specify/memory/tasks.md
```

### OpenSpec 초기화 문제

**Q: `openspec init` 실행 오류**

```bash
# Git 초기화 여부 확인
git status

# Git이 없다면 초기화
git init

# OpenSpec 재시도
openspec init
```

## 명령어 실행 관련 문제

### Claude Code 슬래시 명령어 인식 안 됨

**Q: `/openspec:proposal` 명령어가 동작하지 않음**

```bash
# OpenSpec이 설치되어 있는지 확인
openspec --version

# 프로젝트가 초기화되어 있는지 확인
ls openspec/

# Claude Code 재시작
```

**Q: `/speckit.*` 명령어가 인식되지 않음**

```bash
# .claude/commands/ 폴더 및 파일 확인
ls -la .claude/commands/

# 명령어 파일이 없다면 생성
# (설치 가이드 참조)
```

### spec-kit 명령어 오류

**Q: `specify constitution` 실행 시 오류**

```bash
# 프로젝트 초기화 확인
specify init

# 다시 시도
specify constitution "프로젝트 원칙..."
```

### OpenSpec 명령어 오류

**Q: `openspec propose` 실행 시 오류**

```bash
# openspec/project.md 존재 여부 확인
cat openspec/project.md

# 파일이 없다면 생성
cat > openspec/project.md << 'EOF'
# Project: My Project

## Overview
Project description

## Tech Stack
- Technology list
EOF
```

## 명세 작성 관련 문제

### Constitution이 너무 간단함

**해결 방법:**

더 상세한 Constitution을 작성하거나, 파일을 직접 수정하세요.

```bash
# 파일 직접 수정
nano .specify/memory/constitution.md

# 또는 더 상세한 내용으로 재실행
specify constitution --verbose "상세한 원칙..."
```

### Specification에 원하는 기능이 빠짐

**해결 방법:**

1. 파일 직접 수정:
   ```bash
   nano .specify/memory/specification.md
   ```

2. 또는 명령어 재실행:
   ```bash
   specify specify "추가 요구사항 포함..."
   ```

### OpenSpec Proposal이 자동 생성되지 않음

**해결 방법:**

```bash
# 수동으로 폴더 및 파일 생성
mkdir -p openspec/changes/my-change
touch openspec/changes/my-change/proposal.md
touch openspec/changes/my-change/tasks.md

# 또는 Claude Code에서 재시도
/openspec:proposal "변경 내용..."
```

## AI 생성 코드 품질 문제

### AI가 생성한 코드에 버그가 있음

**해결 방법:**

1. **명세 개선**: 더 상세하고 명확한 명세 작성
2. **코드 리뷰**: AI 코드를 반드시 검토
3. **테스트 작성**: 단위 테스트로 검증
4. **피드백 제공**: AI에게 명확한 피드백

```
# 예시
"생성된 코드에서 division by zero 처리가 누락되었습니다. validate_input 함수를 추가하여 0으로 나누기를 방지해주세요."
```

### AI가 명세를 제대로 이해하지 못함

**해결 방법:**

명세를 더 구체적으로 작성하세요.

**❌ 나쁜 예:**
```
"좋은 TODO 앱을 만들어주세요."
```

**✅ 좋은 예:**
```
"TODO 앱은 다음 기능을 제공합니다:
1. TODO 추가: 제목(필수, 최대 100자), 설명(선택, 최대 500자)
2. TODO 목록: 완료/미완료 필터링, 최신순 정렬
3. TODO 완료: ID로 완료 상태 변경
4. TODO 삭제: ID로 삭제 (소프트 삭제)

데이터베이스: SQLite
테이블 스키마: id(INTEGER), title(TEXT), description(TEXT), is_completed(BOOLEAN), created_at(TIMESTAMP)"
```

## 테스트 및 검증 문제

### 테스트가 실패함

**해결 방법:**

1. **오류 메시지 확인**:
   ```bash
   pytest tests/ -v
   ```

2. **명세와 구현 비교**: Acceptance Criteria 충족 여부 확인

3. **AI에게 수정 요청**:
   ```
   "test_add_todo가 실패합니다. 테스트 로그: [로그 내용]. 코드를 수정해주세요."
   ```

### 커버리지가 80% 미만

**해결 방법:**

```bash
# 커버리지 확인
pytest tests/ --cov=src --cov-report=html

# 누락된 부분 확인
open htmlcov/index.html

# 테스트 추가 요청
"src/calculator.py의 divide 함수에 대한 테스트가 누락되었습니다. test_divide_by_zero 테스트를 추가해주세요."
```

## 도구 선택 문제

### spec-kit vs OpenSpec 어떤 것을 선택해야 하나요?

**간단한 결정 기준:**

```
새 프로젝트? (0→1)
├─ Yes ──> spec-kit 권장
└─ No (기존 프로젝트 개선) ──> OpenSpec 권장

팀 규모 5명 이상?
├─ Yes ──> spec-kit 권장
└─ No ──> OpenSpec 권장
```

자세한 비교는 [도구 비교 문서](./concepts/tools-comparison.md)를 참조하세요.

## 추가 도움 받는 방법

### 공식 문서

- [spec-kit GitHub](https://github.com/github/spec-kit)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [Claude Code 문서](https://code.claude.com/docs/)

### 커뮤니티

- [spec-kit Discussions](https://github.com/github/spec-kit/discussions)
- [OpenSpec Forum](https://forum.cursor.com/t/openspec-lightweight-portable-spec-driven-framework-for-ai-coding-assistants/134052)

### 이슈 제기

문제가 해결되지 않으면 GitHub Issues에 제기하세요:
- [워크샵 저장소 Issues](https://github.com/frentis-ai-study/agentic-coding-workshop/issues)

---

**업데이트**: 2025-11-22
