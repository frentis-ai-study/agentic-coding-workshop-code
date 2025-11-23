"""pytest fixtures for MCP server testing.

Part 3 MCP 서버들을 테스트하기 위한 공통 fixture들을 제공합니다.
"""

import sys
from pathlib import Path
from typing import Any

import pytest


# Part 3 경로를 Python path에 추가
@pytest.fixture(scope="session", autouse=True)
def add_part3_to_path() -> None:
    """Part 3 디렉토리를 Python path에 추가합니다."""
    # 04-testing-deployment에서 03-mcp-tools로 상대 경로
    base_path = Path(__file__).parent.parent.parent.parent.parent
    part3_path = base_path / "03-mcp-tools"

    if part3_path.exists() and str(part3_path) not in sys.path:
        sys.path.insert(0, str(part3_path))


@pytest.fixture(scope="session")
def mcp_servers_base_path() -> Path:
    """Part 3 MCP 서버들의 기본 경로를 반환합니다."""
    base_path = Path(__file__).parent.parent.parent.parent.parent
    return base_path / "03-mcp-tools"


@pytest.fixture
def basic_server_path(mcp_servers_base_path: Path) -> Path:
    """01-basic-server 경로"""
    server_path = mcp_servers_base_path / "01-basic-server" / "main.py"
    if not server_path.exists():
        pytest.skip(f"서버를 찾을 수 없습니다: {server_path}")
    return server_path


@pytest.fixture
def tools_server_path(mcp_servers_base_path: Path) -> Path:
    """02-tools 서버 경로"""
    server_path = mcp_servers_base_path / "02-tools" / "main.py"
    if not server_path.exists():
        pytest.skip(f"서버를 찾을 수 없습니다: {server_path}")
    return server_path


@pytest.fixture
def resources_server_path(mcp_servers_base_path: Path) -> Path:
    """04-resources 서버 경로"""
    server_path = mcp_servers_base_path / "04-resources" / "main.py"
    if not server_path.exists():
        pytest.skip(f"서버를 찾을 수 없습니다: {server_path}")
    return server_path


@pytest.fixture
def temp_test_file(tmp_path: Path) -> Path:
    """임시 테스트 파일 생성"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, MCP Testing!")
    return test_file


@pytest.fixture
def temp_test_dir(tmp_path: Path) -> Path:
    """임시 테스트 디렉토리 생성"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file1.txt").write_text("File 1")
    (test_dir / "file2.txt").write_text("File 2")
    (test_dir / "subdir").mkdir()
    return test_dir


# Calculator 도구 테스트용 fixture
@pytest.fixture
def calculator_test_cases() -> list[dict[str, Any]]:
    """계산기 도구 테스트 케이스"""
    return [
        {"operation": "add", "a": 5, "b": 3, "expected": 8},
        {"operation": "add", "a": -5, "b": 3, "expected": -2},
        {"operation": "add", "a": 0, "b": 0, "expected": 0},
        {"operation": "subtract", "a": 10, "b": 3, "expected": 7},
        {"operation": "subtract", "a": 3, "b": 10, "expected": -7},
        {"operation": "multiply", "a": 4, "b": 5, "expected": 20},
        {"operation": "multiply", "a": -4, "b": 5, "expected": -20},
        {"operation": "multiply", "a": 0, "b": 100, "expected": 0},
        {"operation": "divide", "a": 10, "b": 2, "expected": 5.0},
        {"operation": "divide", "a": 7, "b": 2, "expected": 3.5},
        {"operation": "power", "a": 2, "b": 3, "expected": 8},
        {"operation": "power", "a": 5, "b": 2, "expected": 25},
    ]


@pytest.fixture
def weather_cities() -> list[str]:
    """날씨 API 테스트용 도시 목록"""
    return [
        "Seoul",
        "New York",
        "Tokyo",
        "London",
        "Paris",
    ]


# 메타데이터 검증용 helper 함수
def validate_tool_metadata(tool_info: dict[str, Any]) -> bool:
    """도구 메타데이터가 올바른 형식인지 검증합니다."""
    required_fields = ["name", "description"]
    return all(field in tool_info for field in required_fields)


def validate_resource_metadata(resource_info: dict[str, Any]) -> bool:
    """리소스 메타데이터가 올바른 형식인지 검증합니다."""
    required_fields = ["uri", "name"]
    return all(field in resource_info for field in required_fields)


# ============================================================
# Mock 통합 테스트용 Fixture (빠른 테스트)
# ============================================================

from unittest.mock import Mock


@pytest.fixture
def calculator_tools_mock() -> dict[str, Any]:
    """Mock Calculator 도구 (실제 로직 구현)

    실제 MCP 서버 없이 빠르게 테스트할 수 있습니다.
    """

    def mock_divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return a / b

    return {
        "add": Mock(side_effect=lambda a, b: a + b),
        "subtract": Mock(side_effect=lambda a, b: a - b),
        "multiply": Mock(side_effect=lambda a, b: a * b),
        "divide": Mock(side_effect=mock_divide),
        "power": Mock(side_effect=lambda a, b: a**b),
    }
