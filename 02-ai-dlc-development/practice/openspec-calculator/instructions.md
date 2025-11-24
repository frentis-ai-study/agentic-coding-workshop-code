# OpenSpec 계산기 실습 - 상세 지침

이 문서는 OpenSpec 실습의 각 단계를 더 상세히 안내합니다.

## 사전 준비

### 1. OpenSpec 설치 확인

```bash
# OpenSpec 버전 확인
openspec --version

# 예상 출력: @fission-ai/openspec v0.x.x
```

### 2. 작업 환경 준비

```bash
# 작업 디렉토리 생성
mkdir openspec-calculator-practice
cd openspec-calculator-practice

# Git 및 OpenSpec 초기화
git init
openspec init

# 초기화 확인
ls -la openspec
```

### 3. 기본 계산기 코드 생성

```bash
# src 폴더 생성
mkdir src

# calculator.py 생성
cat > src/calculator.py << 'EOF'
"""
Simple calculator module with basic arithmetic operations.
"""

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

if __name__ == "__main__":
    print(f"10 + 5 = {add(10, 5)}")
    print(f"10 - 5 = {subtract(10, 5)}")
    print(f"10 * 5 = {multiply(10, 5)}")
    print(f"10 / 5 = {divide(10, 5)}")
EOF

# 동작 확인
python src/calculator.py
```

**예상 출력**:
```
10 + 5 = 15.0
10 - 5 = 5.0
10 * 5 = 50.0
10 / 5 = 2.0
```

---

## Step 1: Proposal 작성 (상세)

### 1.1 Proposal 생성

```bash
# Claude Code 사용
/openspec:proposal "계산기에 히스토리 기능 추가"

# 또는 CLI 사용
openspec propose add-calculator-history
```

### 1.2 Proposal 파일 작성

`openspec/changes/add-calculator-history/proposal.md`:

```markdown
# Proposal: Add Calculator History

## 개요
- **변경 ID**: add-calculator-history
- **제안 일자**: 2025-11-22
- **예상 소요 시간**: 1시간

## 배경 및 동기

사용자가 계산기를 사용할 때, 이전 계산 결과를 다시 확인하고 싶어하는 경우가 많습니다. 현재는 매 계산마다 결과를 수동으로 기록해야 하므로 불편합니다.

## 목표

- 모든 계산을 자동으로 기록
- 사용자가 계산 히스토리 조회 가능
- 히스토리 관리 기능 제공 (삭제, 내보내기)

## 범위

### 포함 사항
- 히스토리 저장 (최대 100개)
- 히스토리 조회 (최신순)
- 히스토리 삭제 (전체 또는 개별)
- CSV 내보내기

### 제외 사항
- 히스토리 검색 기능
- 히스토리 통계 분석
- 클라우드 동기화

## 영향받는 컴포넌트

### 신규 생성
- `src/history.py` - CalculatorHistory 클래스

### 수정
- `src/calculator.py` - 히스토리 통합 (선택 사항)

## 성공 기준

- [ ] 히스토리 저장 기능 동작
- [ ] 히스토리 조회 기능 동작
- [ ] 히스토리 삭제 기능 동작
- [ ] CSV 내보내기 기능 동작
- [ ] 단위 테스트 80% 커버리지
```

### 1.3 Tasks 파일 작성

`openspec/changes/add-calculator-history/tasks.md`:

```markdown
# Tasks: Add Calculator History

## Task 1: Create CalculatorHistory Class
- [ ] Create `src/history.py`
- [ ] Define CalculatorHistory class
- [ ] Initialize history list

## Task 2: Implement add_entry
- [ ] Add entry with timestamp
- [ ] Enforce max 100 entries

## Task 3: Implement get_history
- [ ] Return history in reverse chronological order

## Task 4: Implement clear_history
- [ ] Clear all history entries

## Task 5: Implement delete_entry
- [ ] Delete specific entry by index

## Task 6: Implement export_to_csv
- [ ] Export history to CSV file

## Task 7: Write Unit Tests
- [ ] Test add_entry
- [ ] Test get_history
- [ ] Test clear_history
- [ ] Test delete_entry
- [ ] Test export_to_csv
```

### 1.4 Spec Delta 작성

`openspec/changes/add-calculator-history/specs/calculator/spec.md`:

```markdown
# Spec Delta: Calculator History

## ADDED Requirements

### Requirement: History Storage
- Calculator must save all calculations
- Each entry includes: operand1, operation, operand2, result, timestamp
- Maximum 100 entries (FIFO deletion when exceeded)

### Requirement: History Display
- User can retrieve calculation history
- History displayed in reverse chronological order (newest first)
- Display format: `YYYY-MM-DD HH:MM:SS: <a> <op> <b> = <result>`

### Requirement: History Clear
- User can clear all history entries
- Confirmation required (optional, in future)

### Requirement: History Delete
- User can delete a specific entry by index
- Index validation required

### Requirement: History Export
- User can export history to CSV file
- CSV columns: timestamp, operand1, operation, operand2, result

## MODIFIED Requirements

(없음)

## REMOVED Requirements

(없음)
```

---

## Step 2 & 3: Apply - 구현

### 2.1 Apply 실행

```bash
/openspec:apply
```

### 2.2 AI가 생성할 코드 예시

**`src/history.py`**:
```python
from datetime import datetime
from typing import List, Dict
import csv

class CalculatorHistory:
    """Manages calculation history."""

    def __init__(self, max_entries: int = 100):
        self.history: List[Dict] = []
        self.max_entries = max_entries

    def add_entry(
        self, operand1: float, operation: str, operand2: float, result: float
    ):
        """Add a calculation to history."""
        entry = {
            "timestamp": datetime.now(),
            "operand1": operand1,
            "operation": operation,
            "operand2": operand2,
            "result": result,
        }
        self.history.insert(0, entry)  # Newest first
        if len(self.history) > self.max_entries:
            self.history.pop()  # Remove oldest

    def get_history(self) -> List[Dict]:
        """Get all history entries."""
        return self.history

    def clear_history(self):
        """Clear all history entries."""
        self.history.clear()

    def delete_entry(self, index: int):
        """Delete a specific history entry."""
        if 0 <= index < len(self.history):
            del self.history[index]
        else:
            raise IndexError("Invalid history index")

    def export_to_csv(self, filename: str):
        """Export history to CSV file."""
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['timestamp', 'operand1', 'operation', 'operand2', 'result']
            )
            writer.writeheader()
            writer.writerows(self.history)
```

**`tests/test_history.py`**:
```python
import pytest
from src.history import CalculatorHistory

def test_add_entry():
    hist = CalculatorHistory()
    hist.add_entry(10, '+', 5, 15)
    assert len(hist.get_history()) == 1

def test_max_entries():
    hist = CalculatorHistory(max_entries=2)
    hist.add_entry(10, '+', 5, 15)
    hist.add_entry(20, '-', 10, 10)
    hist.add_entry(30, '*', 2, 60)  # Should remove oldest
    assert len(hist.get_history()) == 2

def test_clear_history():
    hist = CalculatorHistory()
    hist.add_entry(10, '+', 5, 15)
    hist.clear_history()
    assert len(hist.get_history()) == 0

def test_delete_entry():
    hist = CalculatorHistory()
    hist.add_entry(10, '+', 5, 15)
    hist.add_entry(20, '-', 10, 10)
    hist.delete_entry(0)
    assert len(hist.get_history()) == 1
```

### 2.3 테스트 실행

```bash
# pytest 설치 (필요시)
pip install pytest

# 테스트 실행
pytest tests/test_history.py -v
```

---

## Step 4: Archive

### 4.1 Archive 실행

```bash
/openspec:archive
```

### 4.2 확인 사항

```bash
# 아카이브된 변경 확인
ls openspec/changes/archive/

# 병합된 스펙 확인
cat openspec/specs/calculator/spec.md

# 업데이트된 project.md 확인
cat openspec/project.md
```

---

## 실습 완료 체크리스트

- [ ] Proposal 작성 완료
- [ ] Spec Delta 작성 완료
- [ ] Tasks 작성 완료
- [ ] 코드 구현 완료 (`src/history.py`)
- [ ] 테스트 작성 및 통과
- [ ] Archive 완료
- [ ] 스펙 병합 확인

---

**작성**: 2025-11-22
