"""
TDD 예제: 계산기 구현

Red-Green-Refactor 사이클을 경험합니다.
"""

import pytest
from calculator import Calculator


class TestCalculator:
    """계산기 테스트 (TDD 방식)"""

    def setup_method(self):
        """각 테스트 전에 Calculator 인스턴스 생성"""
        self.calc = Calculator()

    # RED: 실패하는 테스트부터 작성
    def test_add_two_positive_numbers(self):
        """두 양수를 더하면 올바른 결과를 반환해야 함"""
        result = self.calc.add(2, 3)
        assert result == 5

    def test_add_negative_numbers(self):
        """음수 덧셈도 지원해야 함"""
        result = self.calc.add(-2, -3)
        assert result == -5

    def test_subtract(self):
        """뺄셈 기능"""
        result = self.calc.subtract(10, 3)
        assert result == 7

    def test_multiply(self):
        """곱셈 기능"""
        result = self.calc.multiply(4, 5)
        assert result == 20

    def test_divide(self):
        """나눗셈 기능"""
        result = self.calc.divide(10, 2)
        assert result == 5.0

    def test_divide_by_zero_raises_error(self):
        """0으로 나누면 예외 발생"""
        with pytest.raises(ValueError, match="0으로 나눌 수 없습니다"):
            self.calc.divide(10, 0)

    def test_divide_returns_float(self):
        """나눗셈 결과는 항상 float여야 함"""
        result = self.calc.divide(7, 2)
        assert isinstance(result, float)
        assert result == 3.5

    # AI와 함께 추가 엣지 케이스 발견
    def test_add_with_float(self):
        """소수점 덧셈 지원"""
        result = self.calc.add(1.5, 2.3)
        assert abs(result - 3.8) < 0.0001  # 부동소수점 오차 고려

    def test_large_numbers(self):
        """큰 숫자 계산 지원"""
        result = self.calc.add(10**10, 10**10)
        assert result == 2 * (10**10)


# pytest 실행 예시:
# uv run pytest test_calculator.py -v
