"""
계산기 구현 (TDD Green 단계)

AI가 생성하거나, 개발자가 직접 작성합니다.
"""


class Calculator:
    """간단한 계산기 클래스"""

    def add(self, a: float, b: float) -> float:
        """두 수를 더합니다.

        Args:
            a: 첫 번째 숫자
            b: 두 번째 숫자

        Returns:
            두 수의 합
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """두 수를 뺍니다.

        Args:
            a: 피감수
            b: 감수

        Returns:
            a - b의 결과
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """두 수를 곱합니다.

        Args:
            a: 첫 번째 숫자
            b: 두 번째 숫자

        Returns:
            두 수의 곱
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """두 수를 나눕니다.

        Args:
            a: 피제수
            b: 제수

        Returns:
            a / b의 결과 (항상 float)

        Raises:
            ValueError: b가 0일 때
        """
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return float(a) / float(b)
