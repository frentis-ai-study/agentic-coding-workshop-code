# 실습 1: spec-kit으로 TODO 앱 명세 작성

이 실습에서는 spec-kit의 5단계 워크플로우를 활용하여 간단한 TODO 앱의 명세를 작성하고 구현합니다.

## 학습 목표

- ✅ spec-kit의 5단계 워크플로우를 직접 실행
- ✅ Constitution, Specification, Plan, Tasks의 차이 이해
- ✅ AI가 생성한 산출물의 품질 평가 능력 향상
- ✅ Claude Code 슬래시 명령어 활용 경험

## 예상 소요 시간

**10-15분**

## 선수 지식

- Python 기초
- CLI(터미널) 사용 경험
- spec-kit 설치 완료 ([설치 가이드](../../tools/spec-kit/))

## 실습 시나리오

**프로젝트**: 간단한 TODO 앱 (CLI 기반)

**주요 기능**:
- TODO 추가
- TODO 목록 조회
- TODO 완료 표시
- TODO 삭제

**기술 스택**: Python 3.12, SQLite

## 실습 단계

### 준비 단계

1. **작업 디렉토리 생성**
   ```bash
   mkdir spec-kit-todo-app-practice
   cd spec-kit-todo-app-practice
   ```

2. **spec-kit 초기화**
   ```bash
   specify init
   ```

3. **Git 초기화 (선택)**
   ```bash
   git init
   ```

### Step 1: Constitution 작성 (3분)

**목표**: 프로젝트 원칙 정의

**명령어**:
```bash
# CLI 사용
specify constitution "프로젝트는 Python 3.12를 사용합니다. CLI 기반 TODO 앱으로, SQLite 데이터베이스를 사용합니다. 코드는 PEP 8을 따르고, 타입 힌트를 필수로 작성합니다. 함수는 단일 책임 원칙을 따릅니다."

# 또는 Claude Code 사용
/speckit.constitution "프로젝트는 Python 3.12, SQLite를 사용하는 CLI 기반 TODO 앱입니다."
```

**생성 파일**: `.specify/memory/constitution.md`

**확인 사항**:
- [ ] Constitution 파일이 생성되었는가?
- [ ] Python 버전, 데이터베이스, 코드 스타일이 명시되었는가?

**예상 산출물**:
`examples/constitution.md` 파일을 참고하세요.

---

### Step 2: Specification 작성 (3분)

**목표**: 기능 요구사항 명세

**명령어**:
```bash
# CLI 사용
specify specify "TODO 앱은 다음 기능을 제공합니다: 1) TODO 추가 (제목 필수), 2) TODO 목록 조회 (전체 또는 완료/미완료 필터), 3) TODO 완료 표시, 4) TODO 삭제. CLI 명령어는 'add', 'list', 'complete', 'delete'를 사용합니다."

# 또는 Claude Code 사용
/speckit.specify "TODO CRUD 기능: add, list, complete, delete 명령어"
```

**생성 파일**: `.specify/memory/specification.md`

**확인 사항**:
- [ ] Specification 파일이 생성되었는가?
- [ ] 4가지 주요 기능이 모두 명시되었는가?
- [ ] CLI 명령어 인터페이스가 정의되었는가?

**예상 산출물**:
`examples/specification.md` 파일을 참고하세요.

---

### Step 3: Plan 작성 (2분)

**목표**: 기술 계획 수립

**명령어**:
```bash
# CLI 사용
specify plan

# 또는 Claude Code 사용
/speckit.plan
```

**생성 파일**: `.specify/memory/plan.md`

**확인 사항**:
- [ ] Plan 파일이 생성되었는가?
- [ ] 데이터베이스 스키마가 정의되었는가?
- [ ] 폴더 구조가 명시되었는가?

**예상 산출물**:
`examples/plan.md` 파일을 참고하세요.

---

### Step 4: Tasks 생성 (2분)

**목표**: 작업 분해

**명령어**:
```bash
# CLI 사용
specify tasks

# 또는 Claude Code 사용
/speckit.tasks
```

**생성 파일**: `.specify/memory/tasks.md`

**확인 사항**:
- [ ] Tasks 파일이 생성되었는가?
- [ ] 작업이 순서대로 나열되었는가?
- [ ] 각 작업의 Acceptance Criteria가 명시되었는가?

**예상 산출물**:
`examples/tasks.md` 파일을 참고하세요.

---

### Step 5: Implement (선택 사항, 5-10분)

**목표**: AI를 활용한 구현

**명령어**:
```bash
# CLI 사용
specify implement

# 또는 Claude Code 사용
/speckit.implement
```

**참고**: 이 단계는 시간이 소요되므로, 워크샵에서는 건너뛰고 나중에 개인적으로 시도해볼 수 있습니다.

**구현 시 체크리스트**:
- [ ] `src/` 폴더 및 파일 생성
- [ ] SQLite 데이터베이스 초기화
- [ ] CLI 명령어 동작 확인
- [ ] 테스트 실행

---

## 산출물 확인

모든 단계를 완료하면 다음과 같은 폴더 구조가 생성됩니다:

```
spec-kit-todo-app-practice/
├── .specify/
│   └── memory/
│       ├── constitution.md
│       ├── specification.md
│       ├── plan.md
│       └── tasks.md
├── src/                   (Implement 단계에서 생성)
│   ├── database.py
│   ├── models.py
│   ├── cli.py
│   └── main.py
└── tests/                 (Implement 단계에서 생성)
    └── test_cli.py
```

## 자가 평가 질문

1. **Constitution의 역할은 무엇인가요?**
   - 프로젝트 원칙, 코드 스타일, 기술 스택 정의

2. **Specification과 Plan의 차이는 무엇인가요?**
   - Specification: "무엇을" (요구사항)
   - Plan: "어떻게" (기술 설계)

3. **Tasks의 Acceptance Criteria는 왜 중요한가요?**
   - 작업 완료 여부를 명확히 판단할 수 있음

4. **AI가 생성한 명세에서 개선할 점은 무엇인가요?**
   - (실습 후 스스로 평가)

## 문제 해결

### Q: Constitution 파일이 너무 간단합니다.

**해결 방법**:
```bash
# 더 상세한 Constitution 작성
specify constitution --verbose "프로젝트는 Python 3.12를 사용합니다. ..."
```

### Q: Specification에 원하는 기능이 빠졌습니다.

**해결 방법**:
1. `.specify/memory/specification.md` 파일을 직접 수정
2. 또는 `specify specify` 명령어를 다시 실행하여 추가

### Q: Tasks가 너무 많아서 부담됩니다.

**해결 방법**:
- 우선순위 P0, P1 작업만 선택하여 구현
- 나머지는 나중에 추가

## 다음 단계

spec-kit 실습을 완료했다면, OpenSpec 실습도 진행해보세요:

💻 [실습 2: OpenSpec으로 계산기 기능 개선](../../openspec-calculator/)

## 참고 자료

- [spec-kit 워크플로우 가이드](../../tools/spec-kit/workflow-guide.md)
- [spec-kit GitHub](https://github.com/github/spec-kit)

---

**실습 시작 시간**: _________
**실습 완료 시간**: _________
**소요 시간**: _________
