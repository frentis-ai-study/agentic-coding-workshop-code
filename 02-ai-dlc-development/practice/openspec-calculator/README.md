# 실습 2: OpenSpec으로 계산기 히스토리 기능 추가

이 실습에서는 OpenSpec의 3단계 워크플로우를 활용하여 기존 계산기 앱에 히스토리 기능을 추가합니다.

## 학습 목표

- ✅ OpenSpec의 3단계 워크플로우 실행
- ✅ Proposal → Apply → Archive 사이클 이해
- ✅ Spec Delta 형식 (ADDED/MODIFIED/REMOVED) 작성 능력
- ✅ Claude Code 슬래시 명령어 활용

## 예상 소요 시간

**10-15분**

## 선수 지식

- Python 기초
- OpenSpec 설치 완료 ([설치 가이드](../../tools/openspec/))
- Git 기본 명령어 (선택)

## 실습 시나리오

**프로젝트**: 기존 계산기 앱 개선

**현재 기능**: 기본 사칙연산 (덧셈, 뺄셈, 곱셈, 나눗셈)

**추가 기능**: 계산 히스토리
- 계산 기록 저장
- 기록 조회
- 기록 삭제
- CSV 내보내기

## 실습 단계

### 준비 단계

1. **작업 디렉토리 생성 및 초기화**
   ```bash
   mkdir openspec-calculator-practice
   cd openspec-calculator-practice

   # Git 초기화
   git init

   # OpenSpec 초기화
   openspec init
   ```

2. **기본 계산기 코드 생성 (간단한 예시)**
   ```bash
   mkdir src
   cat > src/calculator.py << 'EOF'
def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
EOF
   ```

3. **project.md 작성**
   ```bash
   cat > openspec/project.md << 'EOF'
# Project: Calculator App

## Overview
Simple calculator with basic arithmetic operations.

## Tech Stack
- Python 3.12
- CLI interface

## Current Features
- Add, subtract, multiply, divide operations
- Input validation (division by zero)
EOF
   ```

---

### Step 1: Proposal 작성 (4분)

**목표**: 변경 제안 및 델타 명세 작성

**명령어**:
```bash
# Claude Code 사용 (권장)
/openspec:proposal "계산기에 히스토리 기능 추가. 계산 기록을 저장하고 조회, 삭제, CSV 내보내기 기능 제공."
```

**생성되는 파일**:
- `openspec/changes/add-calculator-history/proposal.md`
- `openspec/changes/add-calculator-history/tasks.md`
- `openspec/changes/add-calculator-history/specs/calculator/spec.md`

**확인 사항**:
- [ ] Proposal 파일이 생성되었는가?
- [ ] 동기, 목표, 범위가 명확한가?
- [ ] Spec Delta에 ADDED Requirements가 있는가?

**참고**: `examples/proposal.md` 파일을 확인하세요.

---

### Step 2: Spec Delta 작성 (3분)

**목표**: 추가되는 요구사항을 델타 형식으로 작성

**파일**: `openspec/changes/add-calculator-history/specs/calculator/spec.md`

**작성 내용**:
```markdown
# Spec Delta: Calculator History

## ADDED Requirements

### Requirement: History Storage
- Calculator must save calculation history
- Each entry: operation, operands, result, timestamp
- Maximum 100 entries

### Requirement: History Display
- View history in reverse chronological order
- Format: `<timestamp>: <a> <op> <b> = <result>`

### Requirement: History Management
- Clear all history
- Delete specific entry
- Export to CSV

## MODIFIED Requirements

(없음)

## REMOVED Requirements

(없음)
```

**확인 사항**:
- [ ] ADDED Requirements가 명확한가?
- [ ] 각 요구사항이 검증 가능한가?

---

### Step 3: Apply - 구현 (5분)

**목표**: AI를 활용하여 히스토리 기능 구현

**명령어**:
```bash
# Claude Code 사용
/openspec:apply
```

**AI가 생성할 파일**:
- `src/history.py` - CalculatorHistory 클래스
- `tests/test_history.py` - 단위 테스트

**개발자가 할 일**:
1. 생성된 코드 검토
2. 테스트 실행: `pytest tests/`
3. Tasks 체크리스트 업데이트

**확인 사항**:
- [ ] `src/history.py` 생성 및 동작 확인
- [ ] 테스트 통과
- [ ] Tasks의 체크리스트 업데이트

---

### Step 4: Archive - 완료 (2분)

**목표**: 변경 확정 및 스펙 통합

**명령어**:
```bash
# Claude Code 사용
/openspec:archive
```

**OpenSpec이 수행**:
- 델타 명세를 `openspec/specs/calculator/spec.md`에 병합
- 변경 폴더를 `archive/`로 이동
- `project.md` 업데이트 (Current Features에 히스토리 추가)

**확인 사항**:
- [ ] 변경이 아카이브되었는가?
- [ ] `openspec/specs/calculator/spec.md`에 히스토리 요구사항 추가됨?
- [ ] `project.md`의 Current Features 업데이트됨?

---

## 산출물 확인

완료 후 폴더 구조:

```
openspec-calculator-practice/
├── src/
│   ├── calculator.py       (기존)
│   └── history.py          (신규)
├── tests/
│   └── test_history.py     (신규)
├── openspec/
│   ├── project.md          (업데이트)
│   ├── changes/
│   │   └── archive/
│   │       └── add-calculator-history/    (아카이브됨)
│   │           ├── proposal.md
│   │           ├── tasks.md
│   │           └── specs/
│   │               └── calculator/
│   │                   └── spec.md
│   └── specs/
│       └── calculator/
│           └── spec.md     (델타 병합됨)
```

## 자가 평가 질문

1. **Proposal과 Spec Delta의 차이는 무엇인가요?**
   - Proposal: 변경의 동기, 목표, 범위
   - Spec Delta: 구체적 요구사항 변경 (ADDED/MODIFIED/REMOVED)

2. **Archive 단계는 왜 중요한가요?**
   - 변경을 확정하고 프로젝트 전체 스펙에 통합
   - 변경 이력 보존

3. **OpenSpec과 spec-kit의 가장 큰 차이는?**
   - OpenSpec: 변경 중심, 델타 기반
   - spec-kit: 전체 명세, 0→1 프로젝트에 적합

## 문제 해결

### Q: Proposal이 자동 생성되지 않습니다.

**해결 방법**:
```bash
# 수동으로 Proposal 작성
openspec propose add-calculator-history

# 또는 파일 직접 생성
mkdir -p openspec/changes/add-calculator-history
touch openspec/changes/add-calculator-history/proposal.md
```

### Q: Archive 후 스펙이 병합되지 않았습니다.

**해결 방법**:
```bash
# 스펙 확인
cat openspec/specs/calculator/spec.md

# 수동 병합 (필요시)
# 델타 명세를 전체 스펙에 복사
```

## 다음 단계

OpenSpec 실습을 완료했다면:

1. **비교 학습**: spec-kit과 OpenSpec의 차이 정리
2. **도구 선택**: 본인 프로젝트에 적합한 도구 선택
3. **실전 적용**: 실제 프로젝트에 적용

💻 [spec-kit 실습 복습](../../spec-kit-todo-app/)
📚 [도구 비교 문서](../../concepts/tools-comparison.md)

---

**실습 시작 시간**: _________
**실습 완료 시간**: _________
**소요 시간**: _________
