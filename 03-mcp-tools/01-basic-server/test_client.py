"""
MCP 클라이언트 테스트 스크립트

basic-server와 실제 MCP 프로토콜 통신을 테스트합니다.
"""

import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_basic_server() -> None:
    """BasicMCPServer와 통신하여 ping 도구를 테스트합니다."""
    server_script = Path(__file__).parent / "main.py"

    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", str(server_script)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 서버 초기화
            init_result = await session.initialize()

            print("✓ 서버 연결 성공")
            print(f"  서버 정보: {init_result.serverInfo.name} v{init_result.serverInfo.version}")

            # 사용 가능한 도구 목록 조회
            tools = await session.list_tools()
            print(f"\n✓ 사용 가능한 도구: {len(tools.tools)}개")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # ping 도구 호출
            print("\n✓ ping 도구 호출 중...")
            result = await session.call_tool("ping", arguments={})
            print(f"  응답: {result.content[0].text}")

            print("\n✅ 모든 테스트 통과!")


if __name__ == "__main__":
    asyncio.run(test_basic_server())
