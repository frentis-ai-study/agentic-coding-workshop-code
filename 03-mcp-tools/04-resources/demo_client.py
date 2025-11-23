"""FastMCP 리소스 데모 클라이언트.

이 스크립트는 04-resources 서버의 모든 리소스를 시연합니다.

실행 방법:
    uv run python 03-mcp-tools/04-resources/demo_client.py
"""

import asyncio
import json

from fastmcp.client import Client
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


async def demo_static_docs(client: Client) -> None:
    """정적 문서 리소스 데모."""
    console.print("\n[bold cyan]📄 Static Documents 리소스 테스트[/bold cyan]")

    # 템플릿 리소스이므로 직접 URI 지정
    doc_names = ["intro", "quickstart", "examples"]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("URI", style="cyan")
    table.add_column("내용 미리보기", style="green")

    for name in doc_names:
        uri = f"doc://{name}"
        try:
            content = await client.read_resource(uri)
            preview = content[0].text[:80] + "..."
            table.add_row(uri, preview)
        except Exception as e:
            table.add_row(uri, f"[red]오류: {type(e).__name__}: {e}[/red]")

    console.print(table)

    # 특정 문서 전체 읽기
    console.print("\n[yellow]📖 'intro' 문서 전체 내용:[/yellow]")
    intro_content = await client.read_resource("doc://intro")
    console.print(
        Panel(
            intro_content[0].text,
            title="MCP 리소스 소개",
            border_style="cyan",
        )
    )


async def demo_json_data(client: Client) -> None:
    """JSON 데이터 리소스 데모."""
    console.print("\n[bold cyan]📊 JSON Data 리소스 테스트[/bold cyan]")

    # 템플릿 리소스이므로 직접 URI 지정
    user_ids = ["1", "2", "3"]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("사용자 ID", style="cyan")
    table.add_column("이름", style="white")
    table.add_column("이메일", style="green")
    table.add_column("역할", style="yellow")

    for user_id in user_ids:
        uri = f"data://users/{user_id}"
        try:
            content = await client.read_resource(uri)
            user_data = json.loads(content[0].text)
            table.add_row(
                user_data["id"],
                user_data["name"],
                user_data["email"],
                user_data["role"],
            )
        except Exception as e:
            console.print(f"[dim red]경고: {uri} 조회 실패 - {e}[/dim red]")

    console.print(table)

    # 에러 케이스
    console.print("\n[yellow]에러 처리 테스트: 존재하지 않는 사용자[/yellow]")
    try:
        await client.read_resource("data://users/9999")
    except Exception as e:
        console.print(f"[red]✗ 에러: {str(e)}[/red]")


async def demo_file_resources(client: Client) -> None:
    """파일 시스템 리소스 데모."""
    console.print("\n[bold cyan]📁 File Resources 테스트[/bold cyan]")

    # 먼저 파일 목록 가져오기
    try:
        list_content = await client.read_resource("file://list/")
        file_list_data = json.loads(list_content[0].text)
        file_names = file_list_data.get("files", [])
    except Exception:
        console.print("[yellow]⚠️  파일 목록을 가져올 수 없습니다.[/yellow]")
        return

    if not file_names:
        console.print("[yellow]⚠️  data/ 폴더에 파일이 없습니다.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("파일명", style="cyan")
    table.add_column("URI", style="white")
    table.add_column("내용 미리보기", style="green")

    for filename in file_names[:5]:  # 처음 5개만 표시
        uri = f"file://{filename}/"
        try:
            content = await client.read_resource(uri)
            preview = content[0].text[:60] + "..."
            table.add_row(filename, uri, preview)
        except Exception as e:
            table.add_row(filename, uri, f"[red]오류: {type(e).__name__}[/red]")

    console.print(table)

    # 특정 파일 전체 읽기 (sample.md가 있다면)
    if any("sample.md" in fn for fn in file_names):
        console.print("\n[yellow]📄 sample.md 전체 내용:[/yellow]")
        try:
            sample_content = await client.read_resource("file://sample.md/")
            console.print(
                Panel(
                    sample_content[0].text,
                    title="sample.md",
                    border_style="cyan",
                )
            )
        except Exception as e:
            console.print(f"[red]오류: {type(e).__name__}: {e}[/red]")


async def main() -> None:
    """메인 함수."""
    console.print(
        Panel.fit(
            "[bold green]FastMCP Resources Demo Client[/bold green]\n"
            "04-resources 서버의 모든 리소스를 테스트합니다.",
            border_style="green",
        )
    )

    # 서버 경로
    server_script = "03-mcp-tools/04-resources/main.py"

    console.print(f"\n[cyan]서버 연결 중...[/cyan] ({server_script})")

    try:
        async with Client(server_script) as client:
            # 서버 정보
            console.print("[green]✓ 서버 연결 성공![/green]")

            # 리소스 목록
            resources = await client.list_resources()
            console.print(f"[dim]등록된 고정 리소스: {len(resources)}개[/dim]")
            console.print("[dim]템플릿 리소스는 직접 URI로 접근합니다.[/dim]\n")

            # 각 리소스 타입별 데모
            await demo_static_docs(client)
            await demo_json_data(client)
            await demo_file_resources(client)

            console.print("\n[bold green]✓ 모든 리소스 테스트 완료![/bold green]\n")

    except Exception as e:
        console.print(f"\n[bold red]✗ 오류 발생:[/bold red] {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
