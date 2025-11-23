"""HTTP 전송 방식 클라이언트 예제.

서버를 별도로 실행한 후 이 클라이언트로 연결합니다.

사용 방법:
    1. 터미널 1에서 서버 실행:
       uv run python 03-mcp-tools/03-transport-methods/http_server.py

    2. 터미널 2에서 클라이언트 실행:
       uv run python 03-mcp-tools/03-transport-methods/http_client.py

    3. 포트 변경 시:
       서버: uv run python 03-mcp-tools/03-transport-methods/http_server.py --port 9000
       클라이언트: uv run python 03-mcp-tools/03-transport-methods/http_client.py --port 9000
"""

import argparse
import asyncio

from fastmcp.client import Client
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


async def main(port: int) -> None:
    """메인 함수."""
    server_url = f"http://127.0.0.1:{port}/mcp"

    console.print(
        Panel.fit(
            "[bold cyan]HTTP Transport Client[/bold cyan]\nHTTP 서버에 연결하여 도구를 실행합니다.",
            border_style="cyan",
        )
    )

    console.print(f"\n[yellow]서버 URL: {server_url}[/yellow]")
    console.print("[dim]HTTP 전송 방식: 실행 중인 서버에 HTTP/SSE로 연결[/dim]\n")

    console.print("[yellow]서버 연결 시도 중...[/yellow]")

    try:
        # HTTP 서버에 연결
        async with Client(server_url) as client:
            console.print("[green]✓ HTTP 서버 연결 성공[/green]\n")

            # 도구 목록 확인
            tools = await client.list_tools()
            console.print(f"[bold]등록된 도구: {len(tools)}개[/bold]")
            for tool in tools:
                console.print(f"  • [cyan]{tool.name}[/cyan]: {tool.description.split('.')[0]}")

            # 도구 실행 테스트
            console.print("\n[bold magenta]도구 실행 테스트:[/bold magenta]")

            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("도구", style="cyan", width=12)
            table.add_column("입력", style="yellow", width=25)
            table.add_column("결과", style="green", width=25)

            # echo 테스트
            console.print("\n[dim]→ echo 도구 호출 중...[/dim]")
            result = await client.call_tool("echo", {"message": "Hello, HTTP!"})
            table.add_row("echo", "Hello, HTTP!", result.data)
            console.print("[green]✓ 성공[/green]")

            # uppercase 테스트
            console.print("[dim]→ uppercase 도구 호출 중...[/dim]")
            result = await client.call_tool("uppercase", {"text": "http transport"})
            table.add_row("uppercase", "http transport", result.data)
            console.print("[green]✓ 성공[/green]")

            # reverse 테스트 (HTTP 서버만 제공)
            console.print("[dim]→ reverse 도구 호출 중...[/dim]")
            result = await client.call_tool("reverse", {"text": "FastMCP"})
            table.add_row("reverse", "FastMCP", result.data)
            console.print("[green]✓ 성공[/green]")

            console.print("\n")
            console.print(table)

        console.print(
            Panel.fit(
                "[bold green]✓ 모든 작업 완료![/bold green]\n\n"
                "[dim]HTTP 전송 방식 특징:[/dim]\n"
                "• 이미 실행 중인 서버에 HTTP URL로 연결\n"
                "• Server-Sent Events (SSE)를 통한 실시간 통신\n"
                "• 네트워크 기반 (포트 바인딩 필요)\n"
                "• 웹 클라이언트 및 원격 접근에 적합\n"
                "• 다중 클라이언트 동시 연결 가능",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(
            Panel.fit(
                f"[bold red]✗ 서버 연결 실패[/bold red]\n\n"
                f"에러: {e}\n\n"
                f"[yellow]해결 방법:[/yellow]\n"
                f"1. 서버가 실행 중인지 확인하세요:\n"
                f"   uv run python 03-mcp-tools/03-transport-methods/http_server.py --port {port}\n\n"
                f"2. 포트 번호가 일치하는지 확인하세요.\n\n"
                f"3. 방화벽이 포트 {port}를 차단하지 않는지 확인하세요.",
                border_style="red",
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP 전송 방식 MCP 클라이언트")
    parser.add_argument("--port", type=int, default=8000, help="서버 포트 (기본: 8000)")
    args = parser.parse_args()

    asyncio.run(main(args.port))
