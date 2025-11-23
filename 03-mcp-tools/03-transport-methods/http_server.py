"""HTTP 전송 방식 MCP 서버 예제.

HTTP/SSE를 통해 통신하는 MCP 서버입니다.
웹 클라이언트 및 원격 접근이 필요한 경우 사용됩니다.
"""

import argparse

from fastmcp import FastMCP

# HTTP 전송 방식 서버 생성
mcp = FastMCP(name="http-transport-server")


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


@mcp.tool
def reverse(text: str) -> str:
    """텍스트를 역순으로 변환하는 도구.

    Args:
        text: 변환할 텍스트

    Returns:
        역순으로 변환된 텍스트
    """
    return text[::-1]


if __name__ == "__main__":
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(description="HTTP 전송 방식 MCP 서버")
    parser.add_argument("--host", default="127.0.0.1", help="서버 호스트 (기본: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="서버 포트 (기본: 8000)")
    args = parser.parse_args()

    # HTTP 모드로 서버 실행
    print(f"HTTP 서버 시작: http://{args.host}:{args.port}")
    mcp.run(transport="http", host=args.host, port=args.port)
