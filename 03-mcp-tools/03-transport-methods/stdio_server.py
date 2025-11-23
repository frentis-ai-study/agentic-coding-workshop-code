"""STDIO 전송 방식 MCP 서버 예제.

stdin/stdout을 통해 통신하는 MCP 서버입니다.
Claude Desktop 등 로컬 클라이언트와 연동할 때 사용됩니다.
"""

from fastmcp import FastMCP

# STDIO 전송 방식 서버 생성
mcp = FastMCP(name="stdio-transport-server")


@mcp.tool
def echo(message: str) -> str:
    """메시지를 그대로 반환하는 도구.

    Args:
        message: 반환할 메시지

    Returns:
        입력받은 메시지를 그대로 반환
    """
    return f"Echo: {message}"


@mcp.tool
def uppercase(text: str) -> str:
    """텍스트를 대문자로 변환하는 도구.

    Args:
        text: 변환할 텍스트

    Returns:
        대문자로 변환된 텍스트
    """
    return text.upper()


if __name__ == "__main__":
    # STDIO 모드로 서버 실행 (기본값)
    mcp.run()
