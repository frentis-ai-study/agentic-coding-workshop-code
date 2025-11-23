"""HTTP 서버 테스트."""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastmcp.client import Client


@pytest.fixture
async def mcp_client():
    """테스트용 MCP 클라이언트를 생성합니다."""
    import http_server

    async with Client(transport=http_server.mcp) as client:
        yield client


def test_http_server_import():
    """HTTP 서버를 임포트할 수 있는지 테스트."""
    try:
        import http_server

        assert http_server.mcp is not None
        assert http_server.mcp.name == "http-transport-server"
    except ImportError as e:
        pytest.fail(f"Failed to import http_server: {e}")


async def test_http_server_has_tools(mcp_client):
    """HTTP 서버가 도구를 가지고 있는지 테스트."""
    tools = await mcp_client.list_tools()
    tool_names = [tool.name for tool in tools]

    assert "echo" in tool_names
    assert "uppercase" in tool_names
    assert "reverse" in tool_names


async def test_echo_tool(mcp_client):
    """echo 도구 기능 테스트."""
    result = await mcp_client.call_tool("echo", {"message": "Hello, World!"})
    assert result.data == "Echo: Hello, World!"


async def test_uppercase_tool(mcp_client):
    """uppercase 도구 기능 테스트."""
    result = await mcp_client.call_tool("uppercase", {"text": "hello"})
    assert result.data == "HELLO"

    result = await mcp_client.call_tool("uppercase", {"text": "MiXeD CaSe"})
    assert result.data == "MIXED CASE"


async def test_reverse_tool(mcp_client):
    """reverse 도구 기능 테스트."""
    result = await mcp_client.call_tool("reverse", {"text": "Hello"})
    assert result.data == "olleH"

    result = await mcp_client.call_tool("reverse", {"text": "12345"})
    assert result.data == "54321"

    # 회문(palindrome) 테스트
    result = await mcp_client.call_tool("reverse", {"text": "racecar"})
    assert result.data == "racecar"
