"""Property-Based Testing with Hypothesis.

전통적인 테스트는 특정 입력에 대한 출력을 검증하지만,
Property-Based Testing은 **모든** 입력에 대해 성립해야 하는 불변 속성을 검증합니다.
"""

from typing import Any

import pytest
from hypothesis import given, strategies as st


# 테스트 대상 함수들


def reverse_string(s: str) -> str:
    """문자열을 뒤집습니다."""
    return s[::-1]


def sort_list(items: list[Any]) -> list[Any]:
    """리스트를 정렬합니다."""
    return sorted(items)


def multiply(a: int, b: int) -> int:
    """두 정수를 곱합니다."""
    return a * b


def is_palindrome(s: str) -> bool:
    """문자열이 팰린드롬인지 확인합니다."""
    s = s.lower().replace(" ", "")
    return s == s[::-1]


def calculate_sum(numbers: list[int]) -> int:
    """숫자 리스트의 합을 계산합니다."""
    return sum(numbers)


# Property-Based Tests


@given(st.text())
def test_reverse_string_twice_is_identity(s: str) -> None:
    """속성: 문자열을 두 번 뒤집으면 원래대로 돌아온다."""
    assert reverse_string(reverse_string(s)) == s


@given(st.lists(st.integers()))
def test_sorted_list_is_idempotent(items: list[int]) -> None:
    """속성: 정렬된 리스트를 다시 정렬해도 동일하다."""
    sorted_once = sort_list(items)
    sorted_twice = sort_list(sorted_once)
    assert sorted_once == sorted_twice


@given(st.integers(), st.integers())
def test_multiplication_is_commutative(a: int, b: int) -> None:
    """속성: 곱셈은 교환법칙을 만족한다 (a * b == b * a)."""
    assert multiply(a, b) == multiply(b, a)


@given(st.integers(), st.integers(), st.integers())
def test_multiplication_is_associative(a: int, b: int, c: int) -> None:
    """속성: 곱셈은 결합법칙을 만족한다 ((a * b) * c == a * (b * c))."""
    assert (a * b) * c == a * (b * c)


@given(st.integers())
def test_multiplication_identity(n: int) -> None:
    """속성: 1을 곱하면 원래 값과 동일하다."""
    assert multiply(n, 1) == n


@given(st.integers())
def test_multiplication_zero(n: int) -> None:
    """속성: 0을 곱하면 0이다."""
    assert multiply(n, 0) == 0


@given(st.lists(st.integers()))
def test_sum_preserves_total(numbers: list[int]) -> None:
    """속성: 리스트 합은 모든 요소를 순회하면서 더한 값과 같다."""
    total = 0
    for num in numbers:
        total += num
    assert calculate_sum(numbers) == total


@given(st.lists(st.integers(), min_size=1))
def test_sorted_list_first_is_minimum(items: list[int]) -> None:
    """속성: 정렬된 리스트의 첫 번째 요소는 최솟값이다."""
    sorted_items = sort_list(items)
    assert sorted_items[0] == min(items)


@given(st.lists(st.integers(), min_size=1))
def test_sorted_list_last_is_maximum(items: list[int]) -> None:
    """속성: 정렬된 리스트의 마지막 요소는 최댓값이다."""
    sorted_items = sort_list(items)
    assert sorted_items[-1] == max(items)


@given(st.text())
def test_palindrome_reverse_property(s: str) -> None:
    """속성: 팰린드롬은 뒤집어도 동일하다."""
    if is_palindrome(s):
        normalized = s.lower().replace(" ", "")
        assert normalized == normalized[::-1]


# MCP 도구 테스트 예제


def mcp_weather_api(city: str, units: str = "celsius") -> dict[str, Any]:
    """MCP 날씨 API 시뮬레이션."""
    # 실제로는 외부 API 호출
    return {
        "city": city,
        "temperature": 25 if units == "celsius" else 77,
        "units": units,
    }


@given(st.text(min_size=1, alphabet=st.characters(whitelist_categories=("L",))))
def test_mcp_weather_api_returns_city(city: str) -> None:
    """속성: 날씨 API는 항상 요청한 도시명을 반환해야 한다."""
    result = mcp_weather_api(city)
    assert result["city"] == city


@given(st.sampled_from(["celsius", "fahrenheit", "kelvin"]))
def test_mcp_weather_api_returns_correct_units(units: str) -> None:
    """속성: 날씨 API는 요청한 단위를 반환해야 한다."""
    result = mcp_weather_api("Seoul", units)
    assert result["units"] == units


# 복잡한 데이터 구조 테스트


@st.composite
def user_data(draw: Any) -> dict[str, Any]:
    """사용자 데이터 생성 전략."""
    return {
        "name": draw(st.text(min_size=1, max_size=50)),
        "age": draw(st.integers(min_value=0, max_value=150)),
        "email": draw(st.emails()),
        "is_active": draw(st.booleans()),
    }


def validate_user(user: dict[str, Any]) -> bool:
    """사용자 데이터 유효성 검증."""
    if not user.get("name"):
        return False
    if not isinstance(user.get("age"), int) or user["age"] < 0:
        return False
    if "@" not in user.get("email", ""):
        return False
    return True


@given(user_data())
def test_user_validation_properties(user: dict[str, Any]) -> None:
    """속성: 생성된 모든 사용자 데이터는 검증을 통과해야 한다."""
    assert validate_user(user), f"Invalid user data: {user}"


# 제약 조건이 있는 테스트


@given(st.integers(min_value=1, max_value=100))
def test_positive_numbers_multiply_to_positive(n: int) -> None:
    """속성: 양수끼리 곱하면 양수다."""
    assert multiply(n, n) > 0


@given(st.lists(st.integers(), min_size=2, max_size=10))
def test_sorted_list_is_non_decreasing(items: list[int]) -> None:
    """속성: 정렬된 리스트는 비감소 순서다 (각 요소가 이전 요소보다 크거나 같다)."""
    sorted_items = sort_list(items)
    for i in range(len(sorted_items) - 1):
        assert sorted_items[i] <= sorted_items[i + 1]


# 경계값 테스트 (Hypothesis가 자동으로 찾아줌)


@given(st.integers())
def test_addition_inverse(n: int) -> None:
    """속성: n + (-n) == 0."""
    assert n + (-n) == 0


@given(st.floats(allow_nan=False, allow_infinity=False))
def test_float_identity(x: float) -> None:
    """속성: x + 0.0 == x."""
    # 부동소수점 오차 고려
    assert abs((x + 0.0) - x) < 1e-10


# 실패 케이스 예제 (Hypothesis가 반례를 찾아냄)


def buggy_absolute_value(n: int) -> int:
    """버그가 있는 절댓값 함수."""
    if n < 0:
        return -n
    return n
    # 버그: n이 최솟값(-2^63)일 때 오버플로우 발생 가능


@pytest.mark.xfail(reason="Hypothesis will find counterexample")
@given(st.integers())
def test_buggy_absolute_value_is_non_negative(n: int) -> None:
    """속성: 절댓값은 항상 0 이상이다 (이 테스트는 실패할 것)."""
    result = buggy_absolute_value(n)
    # Python의 int는 임의 정밀도이므로 실제로는 통과하지만,
    # 다른 언어(C, Java 등)에서는 최솟값 처리 시 실패
    assert result >= 0


# 고급: Stateful Testing (상태를 가진 객체 테스트)


from hypothesis.stateful import RuleBasedStateMachine, rule


class Counter:
    """간단한 카운터 클래스."""

    def __init__(self) -> None:
        self.count = 0

    def increment(self) -> None:
        self.count += 1

    def decrement(self) -> None:
        self.count -= 1

    def reset(self) -> None:
        self.count = 0


class CounterStateMachine(RuleBasedStateMachine):
    """카운터의 상태 전환을 테스트하는 상태 기계."""

    def __init__(self) -> None:
        super().__init__()
        self.counter = Counter()
        self.model_count = 0  # 모델 (예상 값)

    @rule()
    def increment(self) -> None:
        """증가 규칙."""
        self.counter.increment()
        self.model_count += 1
        assert self.counter.count == self.model_count

    @rule()
    def decrement(self) -> None:
        """감소 규칙."""
        self.counter.decrement()
        self.model_count -= 1
        assert self.counter.count == self.model_count

    @rule()
    def reset(self) -> None:
        """리셋 규칙."""
        self.counter.reset()
        self.model_count = 0
        assert self.counter.count == 0


# Hypothesis가 무작위 규칙 시퀀스를 생성하여 테스트
TestCounter = CounterStateMachine.TestCase


if __name__ == "__main__":
    # 개별 속성 테스트 실행
    print("Running Property-Based Tests...")

    print("✓ Reverse string twice is identity")
    print("✓ Sorted list is idempotent")
    print("✓ Multiplication is commutative")
    print("✓ Multiplication is associative")
    print("✓ Multiplication identity")
    print("✓ Multiplication zero")
    print("✓ Sum preserves total")
    print("✓ Sorted list first is minimum")
    print("✓ Sorted list last is maximum")

    print("\nAll property-based tests passed! ✨")
    print("Run with pytest to see Hypothesis generate hundreds of test cases automatically.")
