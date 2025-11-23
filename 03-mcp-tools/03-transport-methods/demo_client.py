"""FastMCP 전송 방식 데모 클라이언트.

이 스크립트는 STDIO와 HTTP 전송 방식의 차이를 시연합니다.
실제 서버 프로세스를 띄우고 클라이언트로 연결하여 전송 방식을 비교합니다.

실행 방법:
    uv run python 03-mcp-tools/03-transport-methods/demo_client.py
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
HTTP_SERVER = str(SCRIPT_DIR / "http_server.py")


async def demo_stdio_transport() -> None:
    """STDIO 전송 방식 데모 - 실제 서버 프로세스 연결."""
    console.print("\n[bold cyan]📡 STDIO 전송 방식 (stdin/stdout)[/bold cyan]")
    console.print("[dim]용도: Claude Desktop, 로컬 클라이언트 연동[/dim]")
    console.print(f"[dim]서버 실행: python {STDIO_SERVER}[/dim]\n")

    # 실제 서버 프로세스를 subprocess로 실행하고 stdin/stdout으로 연결
    async with Client(STDIO_SERVER) as client:
        # 도구 목록 확인
        tools = await client.list_tools()
        console.print(f"[yellow]등록된 도구: {len(tools)}개[/yellow]")
        for tool in tools:
            console.print(f"  • {tool.name}: {tool.description}")

        # 테스트 케이스
        console.print("\n[bold]도구 실행 테스트:[/bold]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("도구", style="cyan", width=12)
        table.add_column("입력", style="yellow")
        table.add_column("결과", style="green")

        # echo 테스트
        result = await client.call_tool("echo", {"message": "Hello, FastMCP!"})
        table.add_row("echo", "Hello, FastMCP!", result.data)

        # uppercase 테스트
        result = await client.call_tool("uppercase", {"text": "fastmcp rocks"})
        table.add_row("uppercase", "fastmcp rocks", result.data)

        console.print(table)


async def demo_http_transport() -> None:
    """HTTP 전송 방식 데모 - 실제 HTTP 서버 연결."""
    console.print("\n[bold cyan]🌐 HTTP 전송 방식 (HTTP/SSE)[/bold cyan]")
    console.print("[dim]용도: 웹 클라이언트, 원격 접근, 다중 클라이언트[/dim]")
    console.print(f"[dim]서버 실행: python {HTTP_SERVER} --port 8001[/dim]\n")

    # HTTP 서버를 백그라운드에서 실행
    console.print("[yellow]HTTP 서버 시작 중...[/yellow]")
    server_process = await asyncio.create_subprocess_exec(
        "python",
        HTTP_SERVER,
        "--port",
        "8001",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # 서버가 시작될 때까지 대기
    await asyncio.sleep(3)

    try:
        # HTTP URL로 연결 (FastMCP HTTP 서버의 베이스 URL)
        console.print("[yellow]HTTP 서버에 연결 중...[/yellow]")
        async with Client("http://127.0.0.1:8001/mcp") as client:
            # 도구 목록 확인
            tools = await client.list_tools()
            console.print(f"[yellow]등록된 도구: {len(tools)}개[/yellow]")
            for tool in tools:
                console.print(f"  • {tool.name}: {tool.description}")

            # 테스트 케이스
            console.print("\n[bold]도구 실행 테스트:[/bold]")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("도구", style="cyan", width=12)
            table.add_column("입력", style="yellow")
            table.add_column("결과", style="green")

            # echo 테스트
            result = await client.call_tool("echo", {"message": "Hello, HTTP!"})
            table.add_row("echo", "Hello, HTTP!", result.data)

            # uppercase 테스트
            result = await client.call_tool("uppercase", {"text": "http transport"})
            table.add_row("uppercase", "http transport", result.data)

            # reverse 테스트 (HTTP 서버만 제공)
            result = await client.call_tool("reverse", {"text": "FastMCP"})
            table.add_row("reverse", "FastMCP", result.data)

            console.print(table)
    finally:
        # HTTP 서버 종료
        console.print("\n[yellow]HTTP 서버 종료 중...[/yellow]")
        try:
            server_process.terminate()
            await server_process.wait()
        except ProcessLookupError:
            # 이미 종료된 프로세스
            pass


async def demo_comparison() -> None:
    """전송 방식 비교 데모."""
    console.print("\n[bold cyan]⚖️  전송 방식 비교[/bold cyan]\n")

    comparison_table = Table(show_header=True, header_style="bold magenta")
    comparison_table.add_column("항목", style="cyan", width=18)
    comparison_table.add_column("STDIO", style="yellow", width=30)
    comparison_table.add_column("HTTP", style="green", width=30)

    comparison_table.add_row("통신 방식", "stdin/stdout", "HTTP + SSE")
    comparison_table.add_row("클라이언트 연결", "Client(STDIO_SERVER)", 'Client("http://...")')
    comparison_table.add_row("주요 용도", "로컬 클라이언트", "웹/원격 클라이언트")
    comparison_table.add_row("네트워크", "불필요 (프로세스 간 통신)", "포트 바인딩 필요")
    comparison_table.add_row("보안", "프로세스 격리", "인증/암호화 필요")
    comparison_table.add_row("디버깅", "로그 파일", "브라우저/curl 테스트")
    comparison_table.add_row("확장성", "단일 프로세스", "다중 클라이언트")

    console.print(comparison_table)


async def main() -> None:
    """메인 함수."""
    console.print(
        Panel.fit(
            "[bold green]FastMCP Transport Methods Demo[/bold green]\n"
            "STDIO vs HTTP 전송 방식을 실제 서버 연결로 비교합니다.",
            border_style="green",
        )
    )

    # STDIO 전송 방식 데모
    await demo_stdio_transport()

    # HTTP 전송 방식 데모
    await demo_http_transport()

    # 비교 테이블
    await demo_comparison()

    console.print(
        Panel.fit(
            "[bold green]✓ 모든 데모 완료![/bold green]\n\n"
            "[dim]핵심 포인트:[/dim]\n"
            "• STDIO: Client(server_script) - 서버 프로세스 자동 실행\n"
            '• HTTP: Client("http://url") - 실행 중인 서버에 연결\n'
            "• 동일한 FastMCP 코드로 다른 전송 방식 지원\n"
            "• 전송 방식은 구현 세부사항, 도구 로직은 동일",
            border_style="green",
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
