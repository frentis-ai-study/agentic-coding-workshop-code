# Cursor 커스텀 명령어 활용 가이드

Cursor에서 spec-kit 및 OpenSpec을 효과적으로 활용하는 방법을 안내합니다.

## Cursor 커스텀 명령어 개요

Cursor는 Rules 기능을 통해 spec-kit과 OpenSpec을 사용할 수 있습니다.

## spec-kit Cursor 통합

### 1. `--ai cursor-agent` 옵션 사용

spec-kit은 Cursor Agent 모드를 지원합니다.

```bash
# Cursor에서 실행
specify constitution --ai cursor-agent "Python 3.12, FastAPI 사용"
specify specify --ai cursor-agent "TODO CRUD 기능"
specify plan --ai cursor-agent
specify tasks --ai cursor-agent
specify implement --ai cursor-agent
```

### 2. `.cursorrules` 파일 설정

프로젝트 루트에 `.cursorrules` 파일을 생성하여 spec-kit 워크플로우를 정의합니다.

**`.cursorrules` 예시:**
```
# spec-kit Workflow

When using spec-kit for development:

1. **Constitution**: Define project principles first
   - Command: `specify constitution --ai cursor-agent "<principles>"`
   - Output: `.specify/memory/constitution.md`

2. **Specification**: Write requirements
   - Command: `specify specify --ai cursor-agent "<requirements>"`
   - Output: `.specify/memory/specification.md`

3. **Plan**: Create technical plan
   - Command: `specify plan --ai cursor-agent`
   - Output: `.specify/memory/plan.md`

4. **Tasks**: Break down into tasks
   - Command: `specify tasks --ai cursor-agent`
   - Output: `.specify/memory/tasks.md`

5. **Implement**: Execute tasks
   - Command: `specify implement --ai cursor-agent`

Always read `.specify/memory/` files before making code changes.
```

## OpenSpec Cursor 통합

### 1. Rules 기능으로 워크플로우 정의

**`.cursorrules` 추가:**
```
# OpenSpec Workflow

When using OpenSpec for changes:

1. **Proposal**: Create change proposal
   - Command: `openspec propose <change-id>`
   - Files: `openspec/changes/<change-id>/proposal.md`, `tasks.md`, `specs/*/spec.md`

2. **Apply**: Implement the change
   - Command: `openspec apply <change-id>`

3. **Archive**: Finalize the change
   - Command: `openspec archive <change-id>`

Spec Delta Format:
- ADDED Requirements: New features
- MODIFIED Requirements: Changes to existing features
- REMOVED Requirements: Deprecated features

Always read `openspec/project.md` and relevant specs before proposing changes.
```

### 2. Cursor Composer 활용

Cursor의 Composer 기능과 OpenSpec을 함께 사용하면 더욱 효율적입니다.

```
# Composer에서
@openspec/project.md @openspec/changes/add-history/proposal.md
"계산기 히스토리 기능을 구현해주세요."
```

## Claude Code vs Cursor 비교

| 구분 | Claude Code | Cursor |
|------|-------------|--------|
| **OpenSpec** | 네이티브 슬래시 명령어 | Rules + CLI |
| **spec-kit** | 커스텀 슬래시 명령어 | `--ai cursor-agent` |
| **사용성** | 슬래시 명령어로 간편 | CLI 명령어 입력 |
| **통합 수준** | 높음 (네이티브) | 중간 (Rules 필요) |

## Best Practices

### 1. Rules 파일 유지보수

프로젝트마다 `.cursorrules` 파일을 작성하여 팀 전체가 동일한 워크플로우를 따르도록 합니다.

### 2. Composer와 함께 사용

```
# Composer에서 관련 파일 참조
@.specify/memory/constitution.md @src/calculator.py
"Constitution을 참고하여 calculator.py를 개선해주세요."
```

### 3. 산출물 자동 참조

```
# 명세 파일을 자동으로 참조
@openspec/changes/*/proposal.md
"현재 진행 중인 변경사항을 구현해주세요."
```

## 참고 자료

- [Cursor Features](https://cursor.com/features)
- [Cursor Custom Commands](https://github.com/hamzafer/cursor-commands)
- [Spec-Driven Development with Cursor](https://maddevs.io/writeups/project-creation-using-spec-kit-and-cursor/)

---

**업데이트**: 2025-11-22
