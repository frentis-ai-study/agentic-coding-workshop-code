"""Part 3 MCP Tools 서버 테스트.

02-tools 서버의 도구들 (Calculator, Weather, FileSystem)을 테스트합니다.
"""

import sys
from pathlib import Path
from typing import Any

import pytest

# Part 3 경로 추가 (conftest.py에서 자동 추가되지만 명시)
base_path = Path(__file__).parent.parent.parent.parent.parent
part3_path = base_path / "03-mcp-tools" / "02-tools"
if str(part3_path) not in sys.path:
    sys.path.insert(0, str(part3_path))


class TestCalculatorTools:
    """Calculator 도구 테스트"""

    @pytest.fixture
    def calculator_tools(self) -> Any:
        """Calculator 도구 import"""
        try:
            from tools.calculator import add, divide, multiply, power, subtract

            return {
                "add": add,
                "subtract": subtract,
                "multiply": multiply,
                "divide": divide,
                "power": power,
            }
        except ImportError:
            pytest.skip("Calculator 도구를 import할 수 없습니다")

    def test_add(self, calculator_tools: dict[str, Any]) -> None:
        """덧셈 테스트"""
        add = calculator_tools["add"]
        assert add(5, 3) == 8
        assert add(-5, 3) == -2
        assert add(0, 0) == 0
        assert add(100, -50) == 50

    def test_subtract(self, calculator_tools: dict[str, Any]) -> None:
        """뺄셈 테스트"""
        subtract = calculator_tools["subtract"]
        assert subtract(10, 3) == 7
        assert subtract(3, 10) == -7
        assert subtract(0, 0) == 0
        assert subtract(100, 100) == 0

    def test_multiply(self, calculator_tools: dict[str, Any]) -> None:
        """곱셈 테스트"""
        multiply = calculator_tools["multiply"]
        assert multiply(4, 5) == 20
        assert multiply(-4, 5) == -20
        assert multiply(0, 100) == 0
        assert multiply(7, 7) == 49

    def test_divide(self, calculator_tools: dict[str, Any]) -> None:
        """나눗셈 테스트"""
        divide = calculator_tools["divide"]
        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5
        assert divide(0, 5) == 0.0
        assert divide(15, 3) == 5.0

    def test_divide_by_zero(self, calculator_tools: dict[str, Any]) -> None:
        """0으로 나누기 예외 테스트"""
        divide = calculator_tools["divide"]
        with pytest.raises(ValueError, match="0으로 나눌 수 없습니다"):
            divide(10, 0)

    def test_power(self, calculator_tools: dict[str, Any]) -> None:
        """거듭제곱 테스트"""
        power = calculator_tools["power"]
        assert power(2, 3) == 8
        assert power(5, 2) == 25
        assert power(10, 0) == 1
        assert power(2, 10) == 1024

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (2, 3, 5),
            (-5, 10, 5),
            (0, 0, 0),
            (100, -100, 0),
        ],
    )
    def test_add_parametrized(
        self, calculator_tools: dict[str, Any], a: int, b: int, expected: int
    ) -> None:
        """파라미터화된 덧셈 테스트"""
        add = calculator_tools["add"]
        assert add(a, b) == expected


class TestWeatherTools:
    """Weather 도구 테스트"""

    @pytest.fixture
    def weather_tools(self) -> Any:
        """Weather 도구 import"""
        try:
            from tools.weather import get_forecast, get_weather

            return {
                "get_weather": get_weather,
                "get_forecast": get_forecast,
            }
        except ImportError:
            pytest.skip("Weather 도구를 import할 수 없습니다")

    @pytest.mark.asyncio
    async def test_get_weather(self, weather_tools: dict[str, Any]) -> None:
        """현재 날씨 조회 테스트"""
        get_weather = weather_tools["get_weather"]
        result = await get_weather("Seoul")

        # 반환 형식 검증
        assert isinstance(result, dict)
        assert "city" in result
        assert "temperature" in result
        assert "conditions" in result
        assert result["city"] == "Seoul"

    @pytest.mark.asyncio
    async def test_get_weather_multiple_cities(
        self, weather_tools: dict[str, Any], weather_cities: list[str]
    ) -> None:
        """여러 도시 날씨 조회 테스트"""
        get_weather = weather_tools["get_weather"]

        for city in weather_cities:
            result = await get_weather(city)
            assert result["city"] == city
            assert "temperature" in result

    @pytest.mark.asyncio
    async def test_get_forecast(self, weather_tools: dict[str, Any]) -> None:
        """날씨 예보 조회 테스트"""
        get_forecast = weather_tools["get_forecast"]
        result = await get_forecast("Seoul", days=3)

        # 반환 형식 검증
        assert isinstance(result, dict)
        assert "city" in result
        assert "forecast" in result
        assert result["city"] == "Seoul"
        assert isinstance(result["forecast"], list)
        assert len(result["forecast"]) == 3

    @pytest.mark.asyncio
    async def test_get_forecast_default_days(
        self, weather_tools: dict[str, Any]
    ) -> None:
        """기본 예보 일수 테스트"""
        get_forecast = weather_tools["get_forecast"]
        result = await get_forecast("Tokyo")

        # 기본값 5일
        assert len(result["forecast"]) == 5


class TestFileSystemTools:
    """FileSystem 도구 테스트"""

    @pytest.fixture
    def filesystem_tools(self) -> Any:
        """FileSystem 도구 import"""
        try:
            from tools.filesystem import (
                delete_file,
                list_files,
                read_file,
                write_file,
            )

            return {
                "read_file": read_file,
                "write_file": write_file,
                "list_files": list_files,
                "delete_file": delete_file,
            }
        except ImportError:
            pytest.skip("FileSystem 도구를 import할 수 없습니다")

    def test_write_and_read_file(
        self, filesystem_tools: dict[str, Any], tmp_path: Path
    ) -> None:
        """파일 쓰기 및 읽기 테스트"""
        write_file = filesystem_tools["write_file"]
        read_file = filesystem_tools["read_file"]

        test_file = tmp_path / "test.txt"
        test_content = "Hello, FastMCP!"

        # 파일 쓰기
        write_result = write_file(str(test_file), test_content)
        assert "성공" in write_result or "successfully" in write_result.lower()

        # 파일 읽기
        read_result = read_file(str(test_file))
        assert test_content in read_result

    def test_list_files(
        self, filesystem_tools: dict[str, Any], temp_test_dir: Path
    ) -> None:
        """파일 목록 조회 테스트"""
        list_files = filesystem_tools["list_files"]

        result = list_files(str(temp_test_dir))

        # 결과 검증
        assert "file1.txt" in result
        assert "file2.txt" in result
        assert "subdir" in result

    def test_delete_file(
        self, filesystem_tools: dict[str, Any], tmp_path: Path
    ) -> None:
        """파일 삭제 테스트"""
        write_file = filesystem_tools["write_file"]
        delete_file = filesystem_tools["delete_file"]

        test_file = tmp_path / "delete_me.txt"

        # 파일 생성
        write_file(str(test_file), "This will be deleted")
        assert test_file.exists()

        # 파일 삭제
        delete_result = delete_file(str(test_file))
        assert "성공" in delete_result or "successfully" in delete_result.lower()
        assert not test_file.exists()

    def test_read_nonexistent_file(self, filesystem_tools: dict[str, Any]) -> None:
        """존재하지 않는 파일 읽기 테스트"""
        read_file = filesystem_tools["read_file"]

        with pytest.raises(Exception):  # FileNotFoundError 또는 ValueError
            read_file("/nonexistent/file.txt")


# Integration Tests (실제 MCP 서버 연동)


@pytest.mark.skip(reason="langchain-mcp-adapters 통합 후 구현 예정")
class TestMCPServerIntegration:
    """MCP 서버 통합 테스트 (langchain-mcp-adapters 사용)"""

    @pytest.mark.asyncio
    async def test_load_tools_from_server(self) -> None:
        """서버에서 도구 목록 로드"""
        # from langchain_mcp_adapters.client import MultiServerMCPClient
        # from langchain_mcp_adapters.tools import load_mcp_tools
        #
        # client = MultiServerMCPClient({
        #     "tools_server": {
        #         "command": "uv",
        #         "args": ["run", "python", "03-mcp-tools/02-tools/main.py"],
        #         "transport": "stdio",
        #     }
        # })
        #
        # tools = await client.get_tools()
        # assert len(tools) > 0
        pass

    @pytest.mark.asyncio
    async def test_call_calculator_via_mcp(self) -> None:
        """MCP를 통한 계산기 도구 호출"""
        # tools = await load_mcp_tools(session)
        # calculator_tool = next(t for t in tools if t.name == "add")
        # result = await calculator_tool.ainvoke({"a": 5, "b": 3})
        # assert result == 8
        pass


# Property-Based Testing 예제


@pytest.mark.skip(reason="Hypothesis 통합 예제")
class TestCalculatorProperties:
    """Calculator 도구의 속성 기반 테스트"""

    def test_addition_commutative(self) -> None:
        """덧셈 교환법칙: a + b == b + a"""
        # from hypothesis import given
        # from hypothesis import strategies as st
        #
        # @given(st.integers(), st.integers())
        # def test(a, b):
        #     assert add(a, b) == add(b, a)
        pass

    def test_multiplication_associative(self) -> None:
        """곱셈 결합법칙: (a * b) * c == a * (b * c)"""
        pass


# ============================================================
# Mock을 사용한 빠른 통합 테스트
# ============================================================


class TestCalculatorToolsMock:
    """Mock을 사용한 Calculator 도구 빠른 테스트

    실제 MCP 서버 없이 로직만 검증합니다.
    conftest.py의 calculator_tools_mock fixture를 사용합니다.
    """

    def test_add_mock(self, calculator_tools_mock: dict[str, Any]) -> None:
        """덧셈 테스트 (Mock)"""
        add = calculator_tools_mock["add"]
        assert add(5, 3) == 8
        assert add(-5, 3) == -2
        assert add(0, 0) == 0
        # Mock 호출 확인
        assert add.called

    def test_subtract_mock(self, calculator_tools_mock: dict[str, Any]) -> None:
        """뺄셈 테스트 (Mock)"""
        subtract = calculator_tools_mock["subtract"]
        assert subtract(10, 3) == 7
        assert subtract(3, 10) == -7

    def test_multiply_mock(self, calculator_tools_mock: dict[str, Any]) -> None:
        """곱셈 테스트 (Mock)"""
        multiply = calculator_tools_mock["multiply"]
        assert multiply(4, 5) == 20
        assert multiply(-4, 5) == -20

    def test_divide_mock(self, calculator_tools_mock: dict[str, Any]) -> None:
        """나눗셈 테스트 (Mock)"""
        divide = calculator_tools_mock["divide"]
        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_mock(self, calculator_tools_mock: dict[str, Any]) -> None:
        """0으로 나누기 예외 테스트 (Mock)"""
        divide = calculator_tools_mock["divide"]
        with pytest.raises(ValueError, match="0으로 나눌 수 없습니다"):
            divide(10, 0)

    def test_power_mock(self, calculator_tools_mock: dict[str, Any]) -> None:
        """거듭제곱 테스트 (Mock)"""
        power = calculator_tools_mock["power"]
        assert power(2, 3) == 8
        assert power(5, 2) == 25
        assert power(10, 0) == 1

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (2, 3, 5),
            (-5, 10, 5),
            (0, 0, 0),
            (100, -100, 0),
        ],
    )
    def test_add_parametrized_mock(
        self, calculator_tools_mock: dict[str, Any], a: float, b: float, expected: float
    ) -> None:
        """파라미터화된 덧셈 테스트 (Mock)"""
        add = calculator_tools_mock["add"]
        assert add(a, b) == expected


if __name__ == "__main__":
    # 직접 실행 시
    pytest.main([__file__, "-v"])
