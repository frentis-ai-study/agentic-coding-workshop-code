"""Part 3 MCP Resources 서버 테스트.

04-resources 서버의 리소스들을 테스트합니다.
"""

import sys
from pathlib import Path

import pytest

# Part 3 경로 추가
base_path = Path(__file__).parent.parent.parent.parent.parent
part3_path = base_path / "03-mcp-tools" / "04-resources"
if str(part3_path) not in sys.path:
    sys.path.insert(0, str(part3_path))


class TestMCPResources:
    """MCP Resources 서버 테스트"""

    def test_resources_server_exists(self, resources_server_path: Path) -> None:
        """리소스 서버 파일이 존재하는지 확인"""
        assert resources_server_path.exists()
        assert resources_server_path.is_file()

    def test_resources_server_has_fastmcp(self, resources_server_path: Path) -> None:
        """FastMCP를 사용하는지 확인"""
        content = resources_server_path.read_text()
        assert "fastmcp" in content.lower() or "FastMCP" in content

    def test_resources_server_has_resource_decorator(
        self, resources_server_path: Path
    ) -> None:
        """@mcp.resource 데코레이터를 사용하는지 확인"""
        content = resources_server_path.read_text()
        assert "@mcp.resource" in content or "mcp.resource(" in content


# 실제 리소스 통합 테스트 (langchain-mcp-adapters 사용)


@pytest.mark.skip(reason="langchain-mcp-adapters 통합 후 구현 예정")
class TestMCPResourceIntegration:
    """MCP 리소스 통합 테스트"""

    @pytest.mark.asyncio
    async def test_list_resources(self) -> None:
        """서버의 리소스 목록 조회"""
        # from langchain_mcp_adapters.client import MultiServerMCPClient
        #
        # client = MultiServerMCPClient({
        #     "resources_server": {
        #         "command": "uv",
        #         "args": ["run", "python", "03-mcp-tools/04-resources/main.py"],
        #         "transport": "stdio",
        #     }
        # })
        #
        # # 리소스 목록 조회
        # resources = await client.list_resources()
        # assert len(resources) > 0
        pass

    @pytest.mark.asyncio
    async def test_read_resource(self) -> None:
        """리소스 읽기"""
        # resource_uri = "config://app.json"
        # content = await client.read_resource(resource_uri)
        # assert content is not None
        pass

    @pytest.mark.asyncio
    async def test_resource_metadata(self) -> None:
        """리소스 메타데이터 검증"""
        # resources = await client.list_resources()
        # for resource in resources:
        #     assert "uri" in resource
        #     assert "name" in resource
        #     assert validate_resource_metadata(resource)
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
