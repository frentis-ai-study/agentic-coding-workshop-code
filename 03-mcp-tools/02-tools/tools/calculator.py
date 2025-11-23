"""계산기 도구 - 기본 산술 연산을 제공합니다."""

from fastmcp.exceptions import ToolError


def register_calculator_tools(mcp):
    """계산기 도구들을 MCP 서버에 등록합니다.

    Args:
        mcp: FastMCP 서버 인스턴스
    """

    @mcp.tool
    def add(a: float, b: float) -> float:
        """두 숫자를 더합니다.

        Args:
            a: 첫 번째 숫자
            b: 두 번째 숫자

        Returns:
            두 숫자의 합

        Examples:
            >>> add(5, 3)
            8.0
            >>> add(-2, 7)
            5.0
        """
        return a + b

    @mcp.tool
    def subtract(a: float, b: float) -> float:
        """두 숫자를 뺍니다.

        Args:
            a: 첫 번째 숫자 (피감수)
            b: 두 번째 숫자 (감수)

        Returns:
            a에서 b를 뺀 결과

        Examples:
            >>> subtract(10, 4)
            6.0
            >>> subtract(3, 8)
            -5.0
        """
        return a - b

    @mcp.tool
    def multiply(a: float, b: float) -> float:
        """두 숫자를 곱합니다.

        Args:
            a: 첫 번째 숫자
            b: 두 번째 숫자

        Returns:
            두 숫자의 곱

        Examples:
            >>> multiply(4, 5)
            20.0
            >>> multiply(-3, 2)
            -6.0
        """
        return a * b

    @mcp.tool
    def divide(a: float, b: float) -> float:
        """두 숫자를 나눕니다.

        Args:
            a: 첫 번째 숫자 (피제수)
            b: 두 번째 숫자 (제수)

        Returns:
            a를 b로 나눈 결과

        Raises:
            ToolError: b가 0인 경우

        Examples:
            >>> divide(10, 2)
            5.0
            >>> divide(7, 2)
            3.5
        """
        if b == 0:
            raise ToolError("0으로 나눌 수 없습니다")
        return a / b

    @mcp.tool
    def power(base: float, exponent: float) -> float:
        """거듭제곱을 계산합니다.

        Args:
            base: 밑
            exponent: 지수

        Returns:
            base의 exponent 거듭제곱

        Examples:
            >>> power(2, 3)
            8.0
            >>> power(5, 2)
            25.0
        """
        return base**exponent
