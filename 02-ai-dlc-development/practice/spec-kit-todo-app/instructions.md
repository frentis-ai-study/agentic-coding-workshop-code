# spec-kit TODO 앱 실습 - 상세 지침

이 문서는 spec-kit 실습의 각 단계를 더 상세히 안내합니다.

## 사전 준비

### 1. spec-kit 설치 확인

```bash
# spec-kit 버전 확인
specify --version

# 예상 출력: specify-cli 0.x.x 또는 유사
```

설치되지 않았다면 [설치 가이드](../../tools/spec-kit/)를 참고하세요.

### 2. 작업 환경 준비

```bash
# 작업 디렉토리 생성
mkdir spec-kit-todo-app-practice
cd spec-kit-todo-app-practice

# spec-kit 초기화
specify init

# 초기화 확인
ls -la .specify
```

**예상 출력**:
```
.specify/
├── memory/
└── config.yaml
```

---

## Step 1: Constitution 작성

### 목표

프로젝트의 기본 원칙을 정의합니다. AI는 이 원칙을 참고하여 일관된 코드를 생성합니다.

### 실행 명령어

**옵션 A: CLI 사용**
```bash
specify constitution "프로젝트는 Python 3.12를 사용합니다. CLI 기반 TODO 앱으로, SQLite 데이터베이스를 사용합니다. 코드는 PEP 8을 따르고, 타입 힌트를 필수로 작성합니다. 함수는 단일 책임 원칙을 따릅니다. 테스트는 pytest를 사용하며 커버리지는 80% 이상입니다."
```

**옵션 B: Claude Code 사용 (권장)**
```
/speckit.constitution "프로젝트는 Python 3.12, SQLite를 사용하는 CLI 기반 TODO 앱입니다. PEP 8 준수, 타입 힌트 필수, pytest로 80% 커버리지."
```

### 생성 파일 확인

```bash
# Constitution 파일 확인
cat .specify/memory/constitution.md
```

### 기대 산출물

Constitution 파일에 다음 내용이 포함되어야 합니다:

- Python 버전 (3.12)
- 프로젝트 유형 (CLI 기반 TODO 앱)
- 데이터베이스 (SQLite)
- 코드 스타일 (PEP 8, 타입 힌트)
- 테스트 요구사항 (pytest, 80% 커버리지)

### 샘플 Constitution

`examples/constitution.md` 파일의 내용:
```markdown
# Project Constitution

## Project Overview
CLI-based TODO application for managing daily tasks.

## Technical Stack
- **Language**: Python 3.12+
- **Database**: SQLite
- **CLI Framework**: argparse or click

## Code Standards
- **Style Guide**: PEP 8
- **Type Hints**: Required for all functions
- **Docstrings**: Required for public functions
- **Function Design**: Single Responsibility Principle

## Testing
- **Framework**: pytest
- **Coverage**: Minimum 80%
- **Test Naming**: test_<function>_<scenario>

## Architecture Principles
- **Layered Architecture**:
  - CLI Layer (argument parsing, user interaction)
  - Service Layer (business logic)
  - Data Layer (database operations)
- **Separation of Concerns**: Each module has a single purpose
```

---

## Step 2: Specification 작성

### 목표

TODO 앱의 기능 요구사항을 상세히 작성합니다.

### 실행 명령어

**옵션 A: CLI 사용**
```bash
specify specify "TODO 앱은 다음 기능을 제공합니다:

1. TODO 추가 (add): 사용자가 새 TODO를 추가할 수 있습니다. 제목은 필수, 설명은 선택입니다.

2. TODO 목록 조회 (list): 모든 TODO를 조회하거나, 완료/미완료 상태로 필터링할 수 있습니다.

3. TODO 완료 표시 (complete): TODO ID를 입력하여 완료 상태로 변경할 수 있습니다.

4. TODO 삭제 (delete): TODO ID를 입력하여 삭제할 수 있습니다.

CLI 명령어:
- todo add <title> [--description DESC]
- todo list [--status all|completed|pending]
- todo complete <id>
- todo delete <id>"
```

**옵션 B: Claude Code 사용 (권장)**
```
/speckit.specify "TODO CRUD 기능: add (제목 필수, 설명 선택), list (필터링 가능), complete (ID로 완료), delete (ID로 삭제). CLI 명령어: todo add/list/complete/delete"
```

### 생성 파일 확인

```bash
cat .specify/memory/specification.md
```

### 기대 산출물

Specification 파일에 다음 내용이 포함되어야 합니다:

- 4가지 주요 기능 (add, list, complete, delete)
- 각 기능의 요구사항
- CLI 명령어 인터페이스
- Acceptance Criteria

### 샘플 Specification

`examples/specification.md` 파일 일부:
```markdown
# Specification: TODO App

## Feature 1: Add TODO

**As a user**, I want to add a new TODO item.

### Requirements
- User provides a title (required, max 100 chars)
- User can optionally provide a description (max 500 chars)
- TODO is automatically assigned a unique ID
- TODO is created with status "pending"
- Created timestamp is automatically recorded

### CLI Command
```bash
todo add "Buy groceries" --description "Milk, bread, eggs"
```

### Acceptance Criteria
- ✅ TODO is saved to database
- ✅ Unique ID is generated
- ✅ Success message is displayed
- ✅ Title is validated (required, max 100 chars)

## Feature 2: List TODOs

**As a user**, I want to view my TODO items.

### Requirements
- User can view all TODOs
- User can filter by status: all, completed, pending
- TODOs are displayed with: ID, Title, Status, Created Date
- TODOs are sorted by created date (newest first)

### CLI Command
```bash
todo list
todo list --status completed
todo list --status pending
```

### Acceptance Criteria
- ✅ All TODOs are displayed
- ✅ Filtering by status works correctly
- ✅ Display format is clear and readable

(... 나머지 기능도 유사하게 작성됨)
```

---

## Step 3: Plan 작성

### 목표

기술 스택, 아키텍처, 데이터베이스 스키마를 정의합니다.

### 실행 명령어

```bash
# CLI 사용
specify plan

# Claude Code 사용
/speckit.plan
```

**참고**: Plan 단계는 Constitution과 Specification을 기반으로 AI가 자동 생성하므로, 추가 인자 없이 실행합니다.

### 생성 파일 확인

```bash
cat .specify/memory/plan.md
```

### 기대 산출물

Plan 파일에 다음 내용이 포함되어야 합니다:

- 기술 스택 (Python 3.12, SQLite, argparse/click)
- 폴더 구조
- 데이터베이스 스키마
- CLI 명령어 파싱 구조

### 샘플 Plan

`examples/plan.md` 파일 일부:
```markdown
# Technical Plan: TODO App

## Tech Stack

### Core
- **Python**: 3.12+
- **Database**: SQLite (single file database)
- **CLI Framework**: argparse (Python standard library)

### Development Tools
- **Package Manager**: uv
- **Testing**: pytest
- **Type Checker**: mypy

## Folder Structure

```
todo-app/
├── src/
│   ├── __init__.py
│   ├── cli.py           # CLI argument parsing
│   ├── service.py       # Business logic
│   ├── database.py      # Database operations
│   └── models.py        # Data models
├── tests/
│   ├── test_cli.py
│   ├── test_service.py
│   └── test_database.py
├── pyproject.toml
└── README.md
```

## Database Schema

### TODO Table

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(length(title) <= 100),
    description TEXT CHECK(length(description) <= 500),
    is_completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## CLI Command Structure

```
todo
├── add <title> [--description DESC]
├── list [--status STATUS]
├── complete <id>
└── delete <id>
```

### Implementation Strategy

1. **Database Setup** (`database.py`)
   - SQLite connection management
   - Table creation
   - CRUD operations

2. **Service Layer** (`service.py`)
   - add_todo(title, description)
   - list_todos(status_filter)
   - complete_todo(id)
   - delete_todo(id)

3. **CLI Layer** (`cli.py`)
   - Argument parsing with argparse
   - Command routing
   - Output formatting
```

---

## Step 4: Tasks 생성

### 목표

Plan을 실행 가능한 작업으로 분해합니다.

### 실행 명령어

```bash
# CLI 사용
specify tasks

# Claude Code 사용
/speckit.tasks
```

### 생성 파일 확인

```bash
cat .specify/memory/tasks.md
```

### 기대 산출물

Tasks 파일에 다음 내용이 포함되어야 합니다:

- Phase별로 그룹화된 작업 목록
- 각 작업의 우선순위, 예상 시간, 의존성
- Acceptance Criteria

### 샘플 Tasks

`examples/tasks.md` 파일 일부:
```markdown
# Task Breakdown: TODO App

## Phase 1: Setup

### Task 1.1: Project Setup
**Priority**: P0
**Time**: 10 minutes

**Description**: Create project structure and install dependencies.

**Steps**:
1. Create folder structure
2. Create pyproject.toml
3. Run `uv sync`

**Acceptance Criteria**:
- [ ] Folders created
- [ ] Dependencies installed

---

### Task 1.2: Database Setup
**Priority**: P0
**Time**: 15 minutes
**Dependencies**: Task 1.1

**Description**: Create SQLite database and TODO table.

**File**: `src/database.py`

**Functions**:
- `init_db()`: Create database and table
- `get_connection()`: Get database connection

**Acceptance Criteria**:
- [ ] Database file created
- [ ] TODO table exists
- [ ] Can insert and query TODOs

---

## Phase 2: Service Layer

### Task 2.1: TODO Service
**Priority**: P0
**Time**: 20 minutes
**Dependencies**: Task 1.2

**Description**: Implement TODO business logic.

**File**: `src/service.py`

**Functions**:
- `add_todo(title, description)`
- `list_todos(status_filter)`
- `complete_todo(id)`
- `delete_todo(id)`

**Acceptance Criteria**:
- [ ] All functions implemented
- [ ] Unit tests pass (80% coverage)

(... 나머지 Task도 유사)
```

---

## Step 5: Implement (선택 사항)

### 목표

AI를 활용하여 Tasks를 실제로 구현합니다.

### 실행 명령어

```bash
# 전체 구현
specify implement

# 특정 작업만 구현
specify implement --task "Task 1.1"
```

**참고**: 이 단계는 시간이 소요되므로, 워크샵에서는 건너뛰고 개인적으로 시도해볼 것을 권장합니다.

### 구현 프로세스

1. **AI 코드 생성**:
   - AI가 Tasks를 읽고 코드 자동 생성
   - 파일 생성 및 함수 구현

2. **개발자 검토**:
   - 생성된 코드 확인
   - 로직 검증
   - 필요 시 수정

3. **테스트 실행**:
   ```bash
   uv run pytest tests/
   ```

4. **다음 작업**:
   - 현재 작업 완료 후 다음 작업 진행

---

## 실습 완료 체크리스트

- [ ] Constitution 파일 생성 및 확인
- [ ] Specification 파일 생성 및 확인
- [ ] Plan 파일 생성 및 확인
- [ ] Tasks 파일 생성 및 확인
- [ ] (선택) 코드 구현 완료

## 다음 단계

실습을 완료했다면:

1. **자가 평가**: AI가 생성한 명세의 품질 평가
2. **개선 제안**: 부족한 부분을 스스로 찾아 수정
3. **OpenSpec 실습**: 다른 도구도 경험해보기

---

**작성**: 2025-11-22
