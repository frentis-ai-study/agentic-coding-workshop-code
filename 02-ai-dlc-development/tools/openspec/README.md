# OpenSpec 설치 및 설정

OpenSpec은 Fission AI에서 개발한 경량화된 spec-driven 프레임워크로, 기존 프로젝트의 변경 관리에 최적화되어 있습니다.

## OpenSpec이란?

OpenSpec은 Git-like 워크플로우로 변경 제안을 관리하는 명세 도구입니다. Proposal → Apply → Archive의 3단계로 기능 추가 및 개선을 체계적으로 추적합니다.

### 주요 기능

- **3단계 워크플로우**: Proposal → Apply → Archive
- **변경 중심(Change-Driven)**: 기존 프로젝트에 새 기능 추가 또는 개선
- **델타 기반**: 추가/수정/삭제되는 부분만 명시 (ADDED/MODIFIED/REMOVED)
- **Claude Code 네이티브 지원**: `/openspec:*` 슬래시 명령어

## 설치 방법

### 1. npm을 사용한 설치 (권장)

```bash
# OpenSpec 설치
npm install -g @fission-ai/openspec@latest

# 설치 확인
openspec --version
```

### 2. Node.js 버전 요구사항

OpenSpec은 Node.js 18 이상이 필요합니다.

```bash
# Node.js 버전 확인
node --version

# Node.js 18+ 아닌 경우, nvm으로 설치
nvm install 18
nvm use 18
```

### 3. 설치 문제 해결

**Q: `npm install -g` 시 권한 오류 발생**
```bash
# macOS/Linux: sudo 사용
sudo npm install -g @fission-ai/openspec@latest

# 또는 nvm 사용 (권한 문제 회피)
nvm install 18
nvm use 18
npm install -g @fission-ai/openspec@latest
```

**Q: Node.js가 설치되지 않음**
```bash
# macOS (Homebrew)
brew install node

# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# Windows (Chocolatey)
choco install nodejs
```

## 프로젝트 초기화

### 1. 기존 프로젝트 디렉토리로 이동

```bash
# 프로젝트 폴더로 이동
cd my-existing-project

# Git 초기화되어 있어야 함 (권장)
git init  # Git이 없다면
```

### 2. OpenSpec 초기화

```bash
# OpenSpec 초기화
openspec init

# 생성된 폴더 확인
ls -la openspec
```

**생성되는 폴더 구조:**
```
openspec/
├── project.md           # 프로젝트 개요
├── changes/             # 변경 제안 폴더 (처음에는 비어있음)
└── specs/               # 아카이브된 스펙 폴더
```

### 3. project.md 작성

OpenSpec은 `openspec/project.md` 파일로 프로젝트를 정의합니다.

**`openspec/project.md` 예시:**
```markdown
# Project: Calculator App

## Overview
Simple calculator application with basic arithmetic operations.

## Tech Stack
- Python 3.12
- CLI interface

## Architecture
- Single file application
- Functions for add, subtract, multiply, divide

## Development Guidelines
- PEP 8 code style
- Type hints required
- pytest for testing
```

### 4. 환경 검증

```bash
# OpenSpec 설치 및 설정 확인
openspec list

# 예상 출력 (아직 변경사항 없음):
# No changes found.
```

## AI 코딩 어시스턴트 통합

### Claude Code 통합 (네이티브 지원)

OpenSpec은 Claude Code에 네이티브로 통합되어 있어 별도 설정 없이 슬래시 명령어를 사용할 수 있습니다.

#### 슬래시 명령어

```bash
# Claude Code에서 사용
/openspec:proposal "계산기에 히스토리 기능 추가"
/openspec:apply
/openspec:archive
```

**사용 가능한 명령어:**
- `/openspec:proposal` - 변경 제안 작성
- `/openspec:apply` - 승인된 제안 구현
- `/openspec:archive` - 완료된 변경 아카이브

### Cursor 통합

Cursor에서는 Rules 기능으로 OpenSpec을 사용할 수 있습니다.

**`.cursorrules` 설정:**
```
When working with OpenSpec:
1. Use `openspec propose` to create a new change proposal
2. Use `openspec apply` to implement approved changes
3. Use `openspec archive` to finalize completed changes

Always follow the 3-step workflow:
- Proposal: Define the change (motivation, goals, scope)
- Apply: Implement the change with AI assistance
- Archive: Update specs and close the change

Spec delta format:
- ADDED Requirements: New features or requirements
- MODIFIED Requirements: Changes to existing features
- REMOVED Requirements: Deprecated features
```

## OpenSpec 기본 명령어

### 필수 명령어 (3단계)

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `openspec propose` | 변경 제안 작성 | `openspec propose add-history` |
| `openspec apply` | 변경 구현 | `openspec apply add-history` |
| `openspec archive` | 변경 아카이브 | `openspec archive add-history` |

### 조회 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `openspec list` | 모든 변경 목록 조회 | `openspec list` |
| `openspec show` | 특정 변경 상세 조회 | `openspec show add-history` |
| `openspec validate` | 변경 제안 검증 | `openspec validate add-history` |

### 유틸리티 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `openspec init` | 프로젝트 초기화 | `openspec init` |
| `openspec status` | 현재 상태 확인 | `openspec status` |
| `openspec view` | 프로젝트 전체 스펙 보기 | `openspec view` |

## 설정 파일

### `openspec/project.md`

프로젝트의 전반적인 정보를 정의합니다.

```markdown
# Project: [프로젝트명]

## Overview
[프로젝트 개요 및 목적]

## Tech Stack
- [사용 기술 나열]

## Architecture
[시스템 아키텍처 개요]

## Development Guidelines
[코드 스타일, 테스트 요구사항 등]

## Current Features
[현재 구현된 기능 목록]
```

## 다음 단계

OpenSpec 설치 및 설정을 완료했다면, 워크플로우를 학습하세요:

📚 [OpenSpec 워크플로우 가이드](./workflow-guide.md)
💻 [실습: 계산기 히스토리 기능 추가](../../practice/openspec-calculator/)

## 참고 자료

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec README (공식 문서)](https://github.com/Fission-AI/OpenSpec/blob/main/README.md)
- [OpenSpec Cursor 통합 (Forum)](https://forum.cursor.com/t/openspec-lightweight-portable-spec-driven-framework-for-ai-coding-assistants/134052)

---

**업데이트**: 2025-11-22
