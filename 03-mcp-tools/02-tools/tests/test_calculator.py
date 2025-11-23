"""Calculator 도구 테스트."""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastmcp import FastMCP
from fastmcp.client import Client
from tools.calculator import register_calculator_tools


@pytest.fixture
async def mcp_client():
    """테스트용 MCP 클라이언트를 생성합니다."""
    mcp = FastMCP(name="TestCalculatorServer")
    register_calculator_tools(mcp)

    async with Client(transport=mcp) as client:
        yield client


async def test_add(mcp_client):
    """덧셈 도구 테스트."""
    result = await mcp_client.call_tool("add", {"a": 5, "b": 3})
    assert result.data == 8.0

    result = await mcp_client.call_tool("add", {"a": -2, "b": 7})
    assert result.data == 5.0

    result = await mcp_client.call_tool("add", {"a": 0, "b": 0})
    assert result.data == 0.0


async def test_subtract(mcp_client):
    """뺄셈 도구 테스트."""
    result = await mcp_client.call_tool("subtract", {"a": 10, "b": 4})
    assert result.data == 6.0

    result = await mcp_client.call_tool("subtract", {"a": 3, "b": 8})
    assert result.data == -5.0

    result = await mcp_client.call_tool("subtract", {"a": 5, "b": 5})
    assert result.data == 0.0


async def test_multiply(mcp_client):
    """곱셈 도구 테스트."""
    result = await mcp_client.call_tool("multiply", {"a": 4, "b": 5})
    assert result.data == 20.0

    result = await mcp_client.call_tool("multiply", {"a": -3, "b": 2})
    assert result.data == -6.0

    result = await mcp_client.call_tool("multiply", {"a": 0, "b": 100})
    assert result.data == 0.0


async def test_divide_success(mcp_client):
    """나눗셈 도구 성공 케이스 테스트."""
    result = await mcp_client.call_tool("divide", {"a": 10, "b": 2})
    assert result.data == 5.0

    result = await mcp_client.call_tool("divide", {"a": 7, "b": 2})
    assert result.data == 3.5

    result = await mcp_client.call_tool("divide", {"a": -10, "b": 5})
    assert result.data == -2.0


async def test_divide_by_zero(mcp_client):
    """0으로 나누기 에러 테스트."""
    result = await mcp_client.call_tool("divide", {"a": 10, "b": 0}, raise_on_error=False)

    assert result.is_error is True
    assert "0으로 나눌 수 없습니다" in str(result.content)


async def test_power(mcp_client):
    """거듭제곱 도구 테스트."""
    result = await mcp_client.call_tool("power", {"base": 2, "exponent": 3})
    assert result.data == 8.0

    result = await mcp_client.call_tool("power", {"base": 5, "exponent": 2})
    assert result.data == 25.0

    result = await mcp_client.call_tool("power", {"base": 10, "exponent": 0})
    assert result.data == 1.0

    result = await mcp_client.call_tool("power", {"base": 2, "exponent": -1})
    assert result.data == 0.5
