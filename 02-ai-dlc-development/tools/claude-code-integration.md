# Claude Code 슬래시 명령어 활용 가이드

Claude Code에서 spec-kit 및 OpenSpec을 효과적으로 활용하는 방법을 안내합니다.

## Claude Code 슬래시 명령어 개요

Claude Code는 슬래시 명령어를 통해 spec-kit과 OpenSpec을 지원합니다. 이를 활용하면 AI-DLC 워크플로우를 더욱 효율적으로 수행할 수 있습니다.

## OpenSpec 슬래시 명령어 (네이티브 지원)

OpenSpec은 Claude Code에 네이티브로 통합되어 있어, 별도 설정 없이 바로 사용할 수 있습니다.

### 사용 가능한 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `/openspec:proposal` | 변경 제안 작성 | `/openspec:proposal "히스토리 기능 추가"` |
| `/openspec:apply` | 승인된 제안 구현 | `/openspec:apply` |
| `/openspec:archive` | 완료된 변경 아카이브 | `/openspec:archive` |

### 사용 예시

```
# 1. 새 기능 제안
/openspec:proposal "계산기에 히스토리 기능 추가. 계산 기록 저장, 조회, 삭제, CSV 내보내기."

# 2. 구현
/openspec:apply

# 3. 완료 및 아카이브
/openspec:archive
```

## spec-kit 슬래시 명령어 (커스텀 설정 필요)

spec-kit은 커스텀 슬래시 명령어로 설정하여 사용할 수 있습니다.

### 설정 방법

1. **`.claude/commands/` 폴더 생성**
   ```bash
   mkdir -p .claude/commands
   ```

2. **각 단계별 명령어 파일 생성**

**`.claude/commands/speckit-constitution.md`:**
```markdown
Run the spec-kit constitution step to define project principles.

Execute: specify constitution $ARGUMENTS
```

**`.claude/commands/speckit-specify.md`:**
```markdown
Run the spec-kit specify step to write requirements.

Execute: specify specify $ARGUMENTS
```

**`.claude/commands/speckit-plan.md`:**
```markdown
Run the spec-kit plan step to create technical plan.

Execute: specify plan
```

**`.claude/commands/speckit-tasks.md`:**
```markdown
Run the spec-kit tasks step to break down work.

Execute: specify tasks
```

**`.claude/commands/speckit-implement.md`:**
```markdown
Run the spec-kit implement step to execute tasks.

Execute: specify implement $ARGUMENTS
```

### 사용 예시

```
# 1. Constitution 작성
/speckit.constitution "Python 3.12, FastAPI, SQLAlchemy 사용"

# 2. Specification 작성
/speckit.specify "TODO CRUD 기능: add, list, complete, delete"

# 3. Plan 생성
/speckit.plan

# 4. Tasks 생성
/speckit.tasks

# 5. Implementation
/speckit.implement
```

## 인자 전달 방법 ($ARGUMENTS)

### 기본 인자 전달

```
/speckit.constitution "프로젝트는 Python 3.12를 사용합니다."
```

→ `specify constitution "프로젝트는 Python 3.12를 사용합니다."`로 실행됩니다.

### 복잡한 인자 전달

```
/speckit.specify "TODO 앱 기능:
1. TODO 추가 (제목 필수)
2. TODO 목록 조회
3. TODO 완료 표시
4. TODO 삭제"
```

→ 여러 줄도 전달 가능합니다.

## Best Practices

### 1. OpenSpec vs spec-kit 선택

- **새 프로젝트**: spec-kit 사용 (`/speckit.constitution`부터 시작)
- **기존 프로젝트 개선**: OpenSpec 사용 (`/openspec:proposal`로 시작)

### 2. 단계별 실행

한 번에 모든 단계를 실행하지 말고, 각 단계를 확인하며 진행하세요.

```
# ❌ 나쁜 예
한 번에 모든 명령어 실행

# ✅ 좋은 예
/speckit.constitution "..."
→ 결과 확인
/speckit.specify "..."
→ 결과 확인
...
```

### 3. 산출물 검토

AI가 생성한 명세를 항상 검토하고, 필요 시 수정하세요.

```
# 명세 확인
cat .specify/memory/constitution.md

# 필요 시 직접 수정
nano .specify/memory/constitution.md

# 또는 다시 실행
/speckit.constitution "수정된 내용..."
```

## 참고 자료

- [Claude Code 문서](https://code.claude.com/docs/en/slash-commands)
- [spec-kit GitHub](https://github.com/github/spec-kit)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)

---

**업데이트**: 2025-11-22
