"""FastMCP 도구 데모 클라이언트.

이 스크립트는 02-tools 서버의 모든 도구를 시연합니다.

실행 방법:
    uv run python 03-mcp-tools/02-tools/demo_client.py
"""

import asyncio

from fastmcp.client import Client
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


async def demo_calculator(client: Client) -> None:
    """계산기 도구 데모."""
    console.print("\n[bold cyan]📊 Calculator 도구 테스트[/bold cyan]")

    operations = [
        ("add", {"a": 10, "b": 5}, "10 + 5"),
        ("subtract", {"a": 20, "b": 8}, "20 - 8"),
        ("multiply", {"a": 6, "b": 7}, "6 × 7"),
        ("divide", {"a": 100, "b": 4}, "100 ÷ 4"),
        ("power", {"base": 2, "exponent": 10}, "2^10"),
    ]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("연산", style="cyan")
    table.add_column("결과", style="green")

    for tool_name, args, display in operations:
        result = await client.call_tool(tool_name, args)
        table.add_row(display, str(result.data))

    console.print(table)

    # 에러 케이스
    console.print("\n[yellow]에러 처리 테스트: 0으로 나누기[/yellow]")
    result = await client.call_tool("divide", {"a": 10, "b": 0}, raise_on_error=False)
    if result.is_error:
        console.print(f"[red]✗ 에러: {result.content[0].text}[/red]")


async def demo_weather(client: Client) -> None:
    """날씨 도구 데모."""
    console.print("\n[bold cyan]🌤️  Weather 도구 테스트[/bold cyan]")

    cities = ["Seoul", "Tokyo", "London"]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("도시", style="cyan")
    table.add_column("온도", style="yellow")
    table.add_column("날씨", style="green")
    table.add_column("습도", style="blue")

    for city in cities:
        result = await client.call_tool("get_weather", {"city": city})
        data = result.data
        table.add_row(
            data["city"], f"{data['temperature']}°C", data["condition"], f"{data['humidity']}%"
        )

    console.print(table)

    # 일기예보
    console.print("\n[yellow]일기예보 (Seoul, 3일)[/yellow]")
    forecast = await client.call_tool("get_forecast", {"city": "Seoul", "days": 3})

    for day_data in forecast.data["forecast"]:
        console.print(
            f"  {day_data['date']}: "
            f"{day_data['temperature_low']}°C ~ {day_data['temperature_high']}°C, "
            f"{day_data['condition']}"
        )


async def demo_filesystem(client: Client) -> None:
    """파일시스템 도구 데모."""
    console.print("\n[bold cyan]📁 FileSystem 도구 테스트[/bold cyan]")

    # 파일 목록
    console.print("\n[yellow]현재 파일 목록:[/yellow]")
    files = await client.call_tool("list_files", {})
    for file in files.data:
        console.print(f"  • {file}")

    # 파일 읽기
    console.print("\n[yellow]example.txt 읽기:[/yellow]")
    content = await client.call_tool("read_file", {"filename": "example.txt"})
    console.print(Panel(content.data[:200] + "...", title="파일 내용 (일부)", border_style="green"))

    # 파일 쓰기
    console.print("\n[yellow]새 파일 작성:[/yellow]")
    test_content = "이것은 FastMCP 데모 클라이언트에서 작성한 파일입니다.\n작성 시간: " + str(
        asyncio.get_event_loop().time()
    )
    write_result = await client.call_tool(
        "write_file", {"filename": "demo_test.txt", "content": test_content}
    )
    console.print(f"[green]✓ {write_result.data}[/green]")

    # 작성한 파일 읽기
    read_result = await client.call_tool("read_file", {"filename": "demo_test.txt"})
    console.print(f"[green]✓ 파일 읽기 성공:[/green]\n{read_result.data}")

    # 파일 삭제
    console.print("\n[yellow]파일 삭제:[/yellow]")
    delete_result = await client.call_tool("delete_file", {"filename": "demo_test.txt"})
    console.print(f"[green]✓ {delete_result.data}[/green]")

    # 보안 테스트
    console.print("\n[yellow]보안 테스트: 경로 탐색 공격 방지[/yellow]")
    result = await client.call_tool(
        "read_file", {"filename": "../secret.txt"}, raise_on_error=False
    )
    if result.is_error:
        console.print(f"[green]✓ 보안 차단 성공: {result.content[0].text}[/green]")


async def main() -> None:
    """메인 함수."""
    console.print(
        Panel.fit(
            "[bold green]FastMCP Tools Demo Client[/bold green]\n모든 도구를 시연합니다.",
            border_style="green",
        )
    )

    # main.py에서 mcp 인스턴스를 가져옴
    from main import mcp

    async with Client(transport=mcp) as client:
        # 도구 목록 확인
        tools = await client.list_tools()
        console.print(f"\n[bold]등록된 도구: {len(tools)}개[/bold]")

        # 각 도구 데모 실행
        await demo_calculator(client)
        await demo_weather(client)
        await demo_filesystem(client)

    console.print("\n[bold green]✓ 모든 데모 완료![/bold green]\n")


if __name__ == "__main__":
    asyncio.run(main())
