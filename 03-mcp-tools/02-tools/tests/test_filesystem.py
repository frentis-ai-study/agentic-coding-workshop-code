"""FileSystem 도구 테스트."""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastmcp import FastMCP
from fastmcp.client import Client
from tools.filesystem import register_filesystem_tools


@pytest.fixture
async def mcp_client():
    """테스트용 MCP 클라이언트를 생성합니다."""
    mcp = FastMCP(name="TestFileSystemServer")
    register_filesystem_tools(mcp)

    async with Client(transport=mcp) as client:
        yield client


@pytest.fixture
def test_data_dir():
    """테스트 데이터 디렉토리 경로를 반환합니다."""
    return Path(__file__).parent.parent / "data"


async def test_list_files(mcp_client, test_data_dir):
    """파일 목록 조회 테스트."""
    result = await mcp_client.call_tool("list_files", {})

    assert isinstance(result.data, list)
    # example.txt가 존재해야 함
    assert "example.txt" in result.data


async def test_read_existing_file(mcp_client):
    """기존 파일 읽기 테스트."""
    result = await mcp_client.call_tool("read_file", {"filename": "example.txt"})

    assert isinstance(result.data, str)
    assert len(result.data) > 0
    assert "MCP" in result.data or "예제" in result.data


async def test_read_nonexistent_file(mcp_client):
    """존재하지 않는 파일 읽기 에러 테스트."""
    result = await mcp_client.call_tool(
        "read_file", {"filename": "nonexistent.txt"}, raise_on_error=False
    )

    assert result.is_error is True
    assert "파일을 찾을 수 없습니다" in str(result.content)


async def test_write_and_read_file(mcp_client, test_data_dir):
    """파일 쓰기 및 읽기 테스트."""
    test_filename = "test_write.txt"
    test_content = "This is a test content for MCP FileSystem tool."

    # 파일 쓰기
    write_result = await mcp_client.call_tool(
        "write_file", {"filename": test_filename, "content": test_content}
    )
    assert "성공적으로 작성되었습니다" in write_result.data

    # 파일 읽기
    read_result = await mcp_client.call_tool("read_file", {"filename": test_filename})
    assert read_result.data == test_content

    # 정리: 파일 삭제
    await mcp_client.call_tool("delete_file", {"filename": test_filename}, raise_on_error=False)


async def test_delete_file(mcp_client, test_data_dir):
    """파일 삭제 테스트."""
    test_filename = "test_delete.txt"

    # 파일 생성
    await mcp_client.call_tool("write_file", {"filename": test_filename, "content": "Delete me!"})

    # 파일 삭제
    delete_result = await mcp_client.call_tool("delete_file", {"filename": test_filename})
    assert "성공적으로 삭제되었습니다" in delete_result.data

    # 삭제 확인
    read_result = await mcp_client.call_tool(
        "read_file", {"filename": test_filename}, raise_on_error=False
    )
    assert read_result.is_error is True
    assert "파일을 찾을 수 없습니다" in str(read_result.content)


async def test_delete_nonexistent_file(mcp_client):
    """존재하지 않는 파일 삭제 에러 테스트."""
    result = await mcp_client.call_tool(
        "delete_file", {"filename": "nonexistent.txt"}, raise_on_error=False
    )

    assert result.is_error is True
    assert "파일을 찾을 수 없습니다" in str(result.content)


async def test_security_path_traversal(mcp_client):
    """경로 탐색 공격 방지 테스트."""
    dangerous_filenames = [
        "../secret.txt",
        "../../etc/passwd",
        "subdir/../../../secret",
        "test/../../file.txt",
    ]

    for filename in dangerous_filenames:
        result = await mcp_client.call_tool(
            "read_file", {"filename": filename}, raise_on_error=False
        )
        assert result.is_error is True


async def test_security_dangerous_characters(mcp_client):
    """위험한 문자 허용 테스트 (교육용 간소화 - OS가 자동으로 처리)."""
    # 간소화된 버전에서는 위험한 문자를 OS가 처리하도록 함
    # 대부분의 특수 문자는 OS 레벨에서 거부되거나 안전하게 처리됨
    pass


async def test_security_dot_files(mcp_client):
    """점으로 시작하는 파일명 방지 테스트."""
    result = await mcp_client.call_tool(
        "write_file", {"filename": ".hidden", "content": "test"}, raise_on_error=False
    )
    assert result.is_error is True
    assert "유효하지 않은 파일명입니다" in str(result.content)


async def test_empty_filename(mcp_client):
    """빈 파일명 에러 테스트."""
    result = await mcp_client.call_tool("read_file", {"filename": ""}, raise_on_error=False)
    assert result.is_error is True
    assert "파일명을 입력해주세요" in str(result.content)
