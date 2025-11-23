"""
Part 3 MCP 서버 테스트 예제

01-basic-server를 테스트합니다.
"""

import pytest
import subprocess
import time
import json
from pathlib import Path


@pytest.fixture(scope="module")
def mcp_server_path():
    """Part 3 MCP 서버 경로 반환"""
    # 04-testing-deployment에서 03-mcp-tools로 상대 경로
    base_path = Path(__file__).parent.parent.parent.parent.parent
    server_path = base_path / "03-mcp-tools" / "01-basic-server" / "main.py"

    if not server_path.exists():
        pytest.skip(f"MCP 서버를 찾을 수 없습니다: {server_path}")

    return server_path


@pytest.fixture(scope="module")
def mcp_server_process(mcp_server_path):
    """MCP 서버 프로세스 시작 (STDIO)"""
    # 실제 구현에서는 MCP 클라이언트 라이브러리 사용
    # 여기서는 서버 존재 여부만 확인
    yield mcp_server_path
    # Cleanup (필요시)


class TestBasicMCPServer:
    """MCP 기본 서버 테스트"""

    def test_server_file_exists(self, mcp_server_path):
        """서버 파일이 존재하는지 확인"""
        assert mcp_server_path.exists()
        assert mcp_server_path.is_file()

    def test_server_is_executable_python(self, mcp_server_path):
        """Python 파일로 실행 가능한지 확인"""
        assert mcp_server_path.suffix == ".py"

    def test_server_has_fastmcp_import(self, mcp_server_path):
        """FastMCP를 import하는지 확인"""
        content = mcp_server_path.read_text()
        assert "fastmcp" in content.lower() or "FastMCP" in content

    # 실제 MCP 연결 테스트 (langchain-mcp-adapters 사용 예정)
    @pytest.mark.skip(reason="langchain-mcp-adapters 통합 후 구현 예정")
    def test_server_initialize(self):
        """서버 초기화 테스트"""
        # from langchain_mcp_adapters import load_mcp_tools
        # tools = await load_mcp_tools(...)
        # assert len(tools) > 0
        pass

    @pytest.mark.skip(reason="langchain-mcp-adapters 통합 후 구현 예정")
    def test_list_tools(self):
        """서버의 도구 목록 조회"""
        # 서버가 제공하는 도구 목록 확인
        pass


# pytest 실행:
# uv run pytest test_basic_server.py -v
