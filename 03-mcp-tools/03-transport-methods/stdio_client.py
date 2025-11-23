"""STDIO 전송 방식 클라이언트 예제.

서버를 별도로 실행한 후 이 클라이언트로 연결합니다.

사용 방법:
    1. 터미널 1에서 서버 실행:
       uv run python 03-mcp-tools/03-transport-methods/stdio_server.py

    2. 터미널 2에서 클라이언트 실행:
       uv run python 03-mcp-tools/03-transport-methods/stdio_client.py
"""

import asyncio
from pathlib import Path

from fastmcp.client import Client
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# 서버 파일 경로
SCRIPT_DIR = Path(__file__).parent
STDIO_SERVER = str(SCRIPT_DIR / "stdio_server.py")


async def main() -> None:
    """메인 함수."""
    console.print(
        Panel.fit(
            "[bold cyan]STDIO Transport Client[/bold cyan]\n"
            "STDIO 서버에 연결하여 도구를 실행합니다.",
            border_style="cyan",
        )
    )

    console.print(f"\n[yellow]서버 파일: {STDIO_SERVER}[/yellow]")
    console.print(
        "[dim]STDIO 전송 방식: Client가 서버 프로세스를 직접 실행하고 stdin/stdout으로 통신[/dim]\n"
    )

    # STDIO 서버 프로세스를 자동 실행하고 연결
    async with Client(STDIO_SERVER) as client:
        console.print("[green]✓ STDIO 서버 연결 성공[/green]\n")

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
        result = await client.call_tool("echo", {"message": "Hello, STDIO!"})
        table.add_row("echo", "Hello, STDIO!", result.data)
        console.print("[green]✓ 성공[/green]")

        # uppercase 테스트
        console.print("[dim]→ uppercase 도구 호출 중...[/dim]")
        result = await client.call_tool("uppercase", {"text": "fastmcp"})
        table.add_row("uppercase", "fastmcp", result.data)
        console.print("[green]✓ 성공[/green]")

        console.print("\n")
        console.print(table)

    console.print(
        Panel.fit(
            "[bold green]✓ 모든 작업 완료![/bold green]\n\n"
            "[dim]STDIO 전송 방식 특징:[/dim]\n"
            "• Client가 서버 스크립트를 subprocess로 자동 실행\n"
            "• stdin/stdout을 통한 JSON-RPC 통신\n"
            "• 네트워크 불필요 (프로세스 간 통신)\n"
            "• Claude Desktop과 같은 로컬 클라이언트에 적합",
            border_style="green",
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
