# spec-kit 설치 및 설정

spec-kit은 GitHub에서 개발한 AI 기반 명세 도구로, 프로젝트 전체 생명주기를 체계적으로 관리하는 5단계 워크플로우를 제공합니다.

## spec-kit이란?

spec-kit은 AI-DLC 방법론을 실제 프로젝트에 적용할 수 있도록 돕는 명세 관리 도구입니다. Constitution(프로젝트 헌법)부터 Implementation(구현)까지 체계적인 프로세스를 제공합니다.

### 주요 기능

- **5단계 워크플로우**: Constitution → Specify → Plan → Tasks → Implement
- **AI 통합**: GitHub Copilot, Claude, Cursor 등 다양한 AI 어시스턴트 지원
- **메모리 시스템**: `.specify/memory/` 폴더에 모든 명세 자동 저장
- **AI 코딩 어시스턴트 연동**: 슬래시 명령어를 통한 편리한 사용

## 설치 방법

### 1. uv를 사용한 설치 (권장)

```bash
# spec-kit 설치
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 설치 확인
specify --version
```

### 2. pip을 사용한 설치 (대안)

```bash
# spec-kit 설치
pip install git+https://github.com/github/spec-kit.git

# 설치 확인
specify --version
```

### 3. 설치 문제 해결

**Q: `uv tool install` 시 권한 오류 발생**
```bash
# uv 업데이트
curl -LsSf https://astral.sh/uv/install.sh | sh

# 재시도
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

**Q: Python 버전 오류**
```bash
# Python 3.12 설치 (spec-kit 권장 버전)
uv python install 3.12

# 프로젝트에 Python 3.12 고정
uv python pin 3.12
```

## 프로젝트 초기화

### 1. 새 프로젝트 디렉토리 생성

```bash
# 프로젝트 폴더 생성
mkdir my-todo-app
cd my-todo-app

# Git 초기화 (선택 사항, 권장)
git init
```

### 2. spec-kit 초기화

```bash
# spec-kit 초기화
specify init

# 생성된 폴더 확인
ls -la .specify
```

**생성되는 폴더 구조:**
```
.specify/
├── memory/              # 명세 저장 폴더
│   ├── constitution.md  # 프로젝트 헌법 (초기에는 빈 파일)
│   ├── specification.md # 요구사항 명세
│   ├── plan.md          # 기술 계획
│   └── tasks.md         # 작업 목록
└── config.yaml          # spec-kit 설정 파일
```

### 3. 환경 검증

```bash
# spec-kit 설치 및 설정 확인
specify check

# 예상 출력:
# ✅ spec-kit installed correctly
# ✅ .specify/ directory exists
# ✅ memory/ folder initialized
```

## AI 코딩 어시스턴트 통합

### Claude Code 통합

spec-kit은 Claude Code에서 슬래시 명령어로 사용할 수 있습니다.

#### 1. 슬래시 명령어 설정

`.claude/commands/` 폴더에 spec-kit 명령어를 추가합니다.

```bash
# .claude/commands 폴더 생성
mkdir -p .claude/commands

# spec-kit 명령어 파일 생성
```

**`.claude/commands/speckit-constitution.md`:**
```markdown
Run the spec-kit constitution step to define project principles, coding standards, and architectural guidelines.

Execute: specify constitution $ARGUMENTS
```

**`.claude/commands/speckit-specify.md`:**
```markdown
Run the spec-kit specify step to write detailed requirements and specifications.

Execute: specify specify $ARGUMENTS
```

**`.claude/commands/speckit-plan.md`:**
```markdown
Run the spec-kit plan step to create a technical plan including tech stack and architecture.

Execute: specify plan $ARGUMENTS
```

**`.claude/commands/speckit-tasks.md`:**
```markdown
Run the spec-kit tasks step to break down the project into actionable units of work.

Execute: specify tasks $ARGUMENTS
```

**`.claude/commands/speckit-implement.md`:**
```markdown
Run the spec-kit implement step to execute the tasks using AI assistance.

Execute: specify implement $ARGUMENTS
```

#### 2. 슬래시 명령어 사용

```bash
# Claude Code에서 사용
/speckit.constitution "프로젝트는 Python 3.12, FastAPI, SQLAlchemy를 사용합니다."
/speckit.specify "TODO 앱의 CRUD 기능을 구현합니다."
/speckit.plan
/speckit.tasks
/speckit.implement
```

### Cursor 통합

Cursor에서는 `--ai cursor-agent` 옵션을 사용합니다.

```bash
# Cursor에서 실행
specify constitution --ai cursor-agent
specify specify --ai cursor-agent "TODO 앱 요구사항"
specify plan --ai cursor-agent
specify tasks --ai cursor-agent
specify implement --ai cursor-agent
```

**Cursor Rules 설정 (`.cursorrules`):**
```
When working with spec-kit:
1. Use `specify constitution` to define project principles
2. Use `specify specify` to write requirements
3. Use `specify plan` for technical planning
4. Use `specify tasks` to break down work
5. Use `specify implement` to execute tasks

Always read .specify/memory/ files before making changes.
```

## spec-kit 기본 명령어

### 필수 명령어 (5단계)

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `specify constitution` | 프로젝트 헌법 작성 | `specify constitution "Use Python 3.12, FastAPI"` |
| `specify specify` | 요구사항 명세 | `specify specify "TODO CRUD operations"` |
| `specify plan` | 기술 계획 수립 | `specify plan` |
| `specify tasks` | 작업 분해 | `specify tasks` |
| `specify implement` | 구현 실행 | `specify implement` |

### 선택적 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `specify clarify` | 명세 불명확 부분 질문 | `specify clarify` |
| `specify analyze` | 명세 분석 및 개선 제안 | `specify analyze` |
| `specify checklist` | 체크리스트 생성 | `specify checklist` |

### 유틸리티 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `specify init` | 프로젝트 초기화 | `specify init` |
| `specify check` | 설치 및 설정 확인 | `specify check` |
| `specify status` | 현재 진행 상태 확인 | `specify status` |

## 설정 파일

### `.specify/config.yaml`

```yaml
# spec-kit 설정 파일

# AI 어시스턴트 설정
ai:
  provider: claude  # claude, copilot, cursor 등
  model: claude-sonnet-4.5

# 메모리 폴더 위치
memory_path: .specify/memory

# 워크플로우 설정
workflow:
  skip_steps: []  # 건너뛸 단계 (예: [constitution])
  auto_save: true

# 출력 형식
output:
  format: markdown
  verbose: true
```

## 다음 단계

spec-kit 설치 및 설정을 완료했다면, 워크플로우를 학습하세요:

📚 [spec-kit 워크플로우 가이드](./workflow-guide.md)
💻 [실습: TODO 앱 명세 작성](../../practice/spec-kit-todo-app/)

## 참고 자료

- [spec-kit GitHub](https://github.com/github/spec-kit)
- [spec-kit Discussions](https://github.com/github/spec-kit/discussions)
- [Spec-Driven Development with Cursor](https://maddevs.io/writeups/project-creation-using-spec-kit-and-cursor/)

---

**업데이트**: 2025-11-22
