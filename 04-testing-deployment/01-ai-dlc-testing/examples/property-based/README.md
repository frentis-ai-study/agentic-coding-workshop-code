# Property-Based Testing with Hypothesis

**Property-Based Testing (PBT)**은 특정 입력 케이스 대신 **불변 속성(properties)**을 정의하고, 라이브러리가 자동으로 수백~수천 개의 테스트 케이스를 생성하여 검증하는 테스트 기법입니다.

## 왜 Property-Based Testing인가?

전통적인 테스트의 한계:

```python
# 전통적인 예제 기반 테스트
def test_addition():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    # 놓친 경계값? 큰 숫자? 오버플로우?
```

Property-Based Testing의 장점:

```python
# Property-Based Testing
@given(st.integers(), st.integers())
def test_addition_is_commutative(a, b):
    """속성: 덧셈은 교환법칙을 만족한다."""
    assert add(a, b) == add(b, a)
    # Hypothesis가 자동으로 100개 이상의 (a, b) 조합 테스트!
```

**핵심 이점:**
- ✅ **자동 케이스 생성**: 수작업으로 만들기 어려운 경계값 자동 발견
- ✅ **반례 축소 (Shrinking)**: 테스트 실패 시 최소 반례 제시
- ✅ **높은 커버리지**: 수백 개의 케이스를 자동 실행
- ✅ **회귀 방지**: 이전 실패 케이스 자동 재테스트

---

## Hypothesis 기본 사용법

### 1. 설치

```bash
uv add hypothesis  # 또는 pip install hypothesis
```

### 2. 첫 번째 속성 테스트

```python
from hypothesis import given
from hypothesis import strategies as st

@given(st.text())
def test_reverse_twice_is_original(s):
    """속성: 문자열을 두 번 뒤집으면 원래대로."""
    assert s == s[::-1][::-1]
```

**실행 결과:**
```bash
$ pytest test_properties.py -v

Hypothesis가 자동으로 100개의 무작위 문자열 생성 및 테스트!
✓ "" (빈 문자열)
✓ "a"
✓ "한글도테스트"
✓ "🚀emoji"
✓ "\n\t특수문자"
...
```

---

## 핵심 개념

### 1. Strategies (생성 전략)

Hypothesis는 다양한 타입의 데이터를 생성하는 **전략(strategies)**을 제공합니다.

| Strategy | 설명 | 예시 |
|----------|------|------|
| `st.integers()` | 정수 생성 | `-1000, 0, 42, 99999` |
| `st.floats()` | 부동소수점 생성 | `0.0, -3.14, NaN, Infinity` |
| `st.text()` | 문자열 생성 | `"", "abc", "한글", "🎉"` |
| `st.booleans()` | 불린 생성 | `True, False` |
| `st.lists()` | 리스트 생성 | `[], [1], [1, 2, 3]` |
| `st.emails()` | 이메일 생성 | `user@example.com` |
| `st.sampled_from()` | 특정 값에서 선택 | `["red", "green", "blue"]` |

### 2. 제약 조건

```python
# 1에서 100 사이의 정수만
@given(st.integers(min_value=1, max_value=100))
def test_positive_square(n):
    assert n * n > 0

# 최소 길이 1의 비어있지 않은 리스트
@given(st.lists(st.integers(), min_size=1))
def test_max_in_nonempty_list(items):
    assert max(items) in items
```

### 3. 복합 전략 (Composite Strategies)

```python
from hypothesis import strategies as st

@st.composite
def user_data(draw):
    """사용자 객체 생성 전략."""
    return {
        "name": draw(st.text(min_size=1)),
        "age": draw(st.integers(min_value=0, max_value=150)),
        "email": draw(st.emails()),
    }

@given(user_data())
def test_user_validation(user):
    assert validate_user(user)
```

---

## 주요 속성 패턴

### 1. 항등성 (Identity)

**정의**: 특정 연산을 적용해도 값이 변하지 않음.

```python
@given(st.integers())
def test_addition_identity(n):
    """n + 0 == n"""
    assert n + 0 == n

@given(st.integers())
def test_multiplication_identity(n):
    """n * 1 == n"""
    assert n * 1 == n
```

### 2. 역원 (Inverse)

**정의**: 연산의 역연산이 존재함.

```python
@given(st.text())
def test_reverse_inverse(s):
    """reverse(reverse(s)) == s"""
    assert s[::-1][::-1] == s

@given(st.lists(st.integers()))
def test_sort_unsort_inverse(items):
    """정렬 후 원본과 집합으로는 동일"""
    assert set(sorted(items)) == set(items)
```

### 3. 교환법칙 (Commutativity)

**정의**: 피연산자 순서를 바꿔도 결과가 동일.

```python
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """a + b == b + a"""
    assert a + b == b + a

@given(st.integers(), st.integers())
def test_multiplication_commutative(a, b):
    """a * b == b * a"""
    assert a * b == b * a
```

### 4. 결합법칙 (Associativity)

**정의**: 연산 순서를 바꿔도 결과가 동일.

```python
@given(st.integers(), st.integers(), st.integers())
def test_addition_associative(a, b, c):
    """(a + b) + c == a + (b + c)"""
    assert (a + b) + c == a + (b + c)
```

### 5. 멱등성 (Idempotence)

**정의**: 여러 번 적용해도 한 번 적용한 것과 동일.

```python
@given(st.lists(st.integers()))
def test_sort_idempotent(items):
    """sorted(sorted(items)) == sorted(items)"""
    assert sorted(sorted(items)) == sorted(items)

@given(st.text())
def test_lowercase_idempotent(s):
    """s.lower().lower() == s.lower()"""
    assert s.lower().lower() == s.lower()
```

### 6. 불변성 (Invariant)

**정의**: 특정 조건이 항상 유지됨.

```python
@given(st.lists(st.integers(), min_size=1))
def test_sorted_first_is_min(items):
    """정렬 후 첫 번째는 최솟값"""
    sorted_items = sorted(items)
    assert sorted_items[0] == min(items)

@given(st.lists(st.integers()))
def test_sorted_preserves_length(items):
    """정렬 후 길이 유지"""
    assert len(sorted(items)) == len(items)
```

---

## 실전 적용: MCP 서버 테스트

### 계산기 MCP 도구 테스트

```python
from fastmcp import FastMCP

mcp = FastMCP("calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b

# Property-Based Tests
from hypothesis import given
from hypothesis import strategies as st

@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    """덧셈 교환법칙"""
    assert add(a, b) == add(b, a)

@given(st.integers(), st.integers(), st.integers())
def test_add_associative(a, b, c):
    """덧셈 결합법칙"""
    assert add(add(a, b), c) == add(a, add(b, c))

@given(st.integers())
def test_multiply_by_zero(n):
    """0 곱셈"""
    assert multiply(n, 0) == 0

@given(st.integers())
def test_multiply_identity(n):
    """1 곱셈"""
    assert multiply(n, 1) == n
```

### 날씨 API MCP 도구 테스트

```python
@mcp.tool()
async def get_weather(city: str, units: str = "celsius") -> dict:
    """날씨 정보 조회."""
    # 외부 API 호출
    return {
        "city": city,
        "temperature": 25,
        "units": units,
    }

@given(st.text(min_size=1))
async def test_weather_returns_requested_city(city):
    """요청한 도시를 반환해야 함"""
    result = await get_weather(city)
    assert result["city"] == city

@given(st.sampled_from(["celsius", "fahrenheit", "kelvin"]))
async def test_weather_returns_requested_units(units):
    """요청한 단위를 반환해야 함"""
    result = await get_weather("Seoul", units)
    assert result["units"] == units
```

---

## 고급 기능

### 1. Shrinking (반례 축소)

테스트가 실패하면 Hypothesis는 **최소 반례(minimal counterexample)**를 찾아줍니다.

```python
@given(st.lists(st.integers()))
def test_sum_is_positive(numbers):
    """(버그가 있는 가정) 합이 항상 양수?"""
    assert sum(numbers) > 0

# Hypothesis가 찾는 최소 반례: [-1] 또는 [0]
```

**실행 결과:**
```
Falsifying example: test_sum_is_positive(numbers=[-1])
```

### 2. Stateful Testing (상태 기반 테스트)

상태를 가진 객체의 동작을 테스트합니다.

```python
from hypothesis.stateful import RuleBasedStateMachine, rule

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def get_total(self):
        return len(self.items)

class CartStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.cart = ShoppingCart()
        self.model = []  # 모델 (예상 상태)

    @rule(item=st.text())
    def add_item(self, item):
        self.cart.add_item(item)
        self.model.append(item)
        assert self.cart.get_total() == len(self.model)

    @rule(item=st.text())
    def remove_item(self, item):
        self.cart.remove_item(item)
        if item in self.model:
            self.model.remove(item)
        assert self.cart.get_total() == len(self.model)

TestCart = CartStateMachine.TestCase
```

### 3. 가정 (Assumptions)

특정 조건을 만족하는 입력만 테스트합니다.

```python
from hypothesis import assume

@given(st.integers(), st.integers())
def test_division(a, b):
    assume(b != 0)  # b가 0이 아닌 경우만 테스트
    result = a / b
    assert result * b == pytest.approx(a)
```

---

## 실행 방법

### 1. pytest로 실행

```bash
cd 04-testing-deployment/01-ai-dlc-testing/examples/property-based
uv run pytest test_properties.py -v
```

**예상 출력:**
```
test_properties.py::test_reverse_string_twice_is_identity PASSED
test_properties.py::test_sorted_list_is_idempotent PASSED
test_properties.py::test_multiplication_is_commutative PASSED
...
===================== 100 passed in 2.34s =====================
```

### 2. 더 많은 케이스 테스트

```bash
# 기본 100개 대신 1000개 케이스 실행
uv run pytest test_properties.py --hypothesis-max-examples=1000
```

### 3. 프로파일 사용

```python
from hypothesis import settings, Verbosity

@settings(max_examples=1000, verbosity=Verbosity.verbose)
@given(st.integers())
def test_with_more_examples(n):
    assert n + 0 == n
```

---

## 모범 사례

### ✅ DO

1. **일반적인 속성부터**: 항등성, 역원, 교환법칙 등 보편적 속성 먼저 테스트
2. **제약 조건 명시**: `min_value`, `max_value` 등으로 유효한 입력 범위 제한
3. **실패 케이스 저장**: `@example` 데코레이터로 과거 실패 케이스 회귀 방지
4. **속성 문서화**: 각 테스트가 검증하는 속성을 docstring에 명시

```python
@given(st.integers(min_value=0))
@example(0)  # 경계값 명시
@example(1)
def test_factorial_properties(n):
    """속성: n! >= n (n >= 0)"""
    assert factorial(n) >= n
```

### ❌ DON'T

1. **과도한 `assume()`**: 입력 공간을 너무 좁히면 테스트 효율 저하
2. **부작용 무시**: 테스트 간 상태 공유 주의 (테스트 독립성 유지)
3. **속성 없이 구현 복제**: 속성 검증 대신 구현을 그대로 복사하지 말 것

---

## Metamorphic Testing과의 결합

Property-Based Testing과 Metamorphic Testing을 함께 사용하면 강력합니다!

```python
from hypothesis import given
from hypothesis import strategies as st
from metamorphic_relations import PermutationInvariance

relation = PermutationInvariance()

@given(st.lists(st.integers()))
def test_sort_permutation_invariance(items):
    """속성: 리스트를 섞어도 정렬 결과는 동일"""
    import random
    shuffled = items.copy()
    random.shuffle(shuffled)

    sorted_original = sorted(items)
    sorted_shuffled = sorted(shuffled)

    assert relation.verify_outputs(sorted_original, sorted_shuffled)
```

---

## 참고 자료

### 공식 문서
- [Hypothesis 공식 문서](https://hypothesis.readthedocs.io/)
- [Hypothesis Python 예제](https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python/examples)

### 추천 글
- [Property-Based Testing with Python](https://blog.logrocket.com/property-based-testing-python-hypothesis/)
- [Introduction to Property Based Testing](https://fsharpforfunandprofit.com/posts/property-based-testing/)

### 유사 라이브러리
- **Scala**: ScalaCheck
- **Haskell**: QuickCheck (원조!)
- **JavaScript**: fast-check
- **Rust**: proptest

---

## 다음 단계

Property-Based Testing을 마스터했다면:

1. **Metamorphic + Property-Based 결합**: 두 기법을 혼합하여 강력한 테스트 작성
2. **Stateful Testing**: 복잡한 상태 전환 검증
3. **MCP 서버 전체 테스트 스위트 구축**: Part 3 서버들을 PBT로 검증

📁 **[MCP 서버 테스트 예제 →](../mcp-testing/)**
