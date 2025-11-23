"""
Tests for Basic MCP Server

서버 초기화 및 메타데이터 검증 테스트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from main import mcp


def test_server_initialization():
    """서버가 올바르게 초기화되는지 확인합니다."""
    assert mcp is not None
    assert mcp.name == "BasicMCPServer"


def test_server_metadata():
    """서버 메타데이터가 올바르게 설정되었는지 확인합니다."""
    assert hasattr(mcp, "name")
    assert isinstance(mcp.name, str)
    assert len(mcp.name) > 0


def test_server_has_run_method():
    """서버가 run() 메서드를 가지고 있는지 확인합니다."""
    assert hasattr(mcp, "run")
    assert callable(mcp.run)
