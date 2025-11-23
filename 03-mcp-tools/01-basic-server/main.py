"""01-basic-server: 최소한의 FastMCP 서버 예제

Simple MCP server demonstrating basic FastMCP setup and initialization.
"""

from fastmcp import FastMCP

# FastMCP 서버 인스턴스 생성
mcp = FastMCP(
    name="BasicMCPServer",
)


@mcp.tool()
def ping() -> str:
    """서버가 정상적으로 응답하는지 확인하는 간단한 도구입니다.

    Returns:
        str: "pong" 메시지
    """
    return "pong"


def main() -> None:
    """서버를 시작합니다.

    STDIO 전송 방식을 사용하여 MCP 프로토콜 메시지를 주고받습니다.
    Claude Desktop 같은 로컬 클라이언트와 통신할 수 있습니다.
    """
    mcp.run()  # STDIO 기본 전송 방식으로 서버 실행


if __name__ == "__main__":
    main()
