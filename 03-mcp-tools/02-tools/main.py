"""FastMCP Tools 예제 - 다양한 도구 구현.

이 예제는 FastMCP 서버에 여러 도구를 등록하고 사용하는 방법을 보여줍니다:
- Calculator: 기본 산술 연산 (동기)
- Weather: 외부 API 호출 (비동기)
- FileSystem: 파일 읽기/쓰기 (동기)

실행 방법:
    uv run python 03-mcp-tools/02-tools/main.py
"""

import logging

from fastmcp import FastMCP
from tools.calculator import register_calculator_tools
from tools.datetime_tools import register_datetime_tools
from tools.filesystem import register_filesystem_tools
from tools.weather import register_weather_tools

# 로깅 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    """MCP 서버를 생성하고 도구들을 등록합니다.

    Returns:
        설정된 FastMCP 서버 인스턴스
    """
    # FastMCP 서버 생성
    mcp = FastMCP(
        name="ToolsServer",
    )

    # 도구 등록
    logger.info("도구 등록 시작...")
    register_calculator_tools(mcp)
    logger.info("✓ Calculator 도구 등록 완료")

    register_datetime_tools(mcp)
    logger.info("✓ DateTime 도구 등록 완료")

    register_weather_tools(mcp)
    logger.info("✓ Weather 도구 등록 완료")

    register_filesystem_tools(mcp)
    logger.info("✓ FileSystem 도구 등록 완료")

    logger.info("모든 도구 등록 완료!")
    return mcp


# 서버 인스턴스 생성
mcp = create_server()


if __name__ == "__main__":
    logger.info("MCP 서버 시작...")
    logger.info("사용 가능한 도구:")
    logger.info("  - add, subtract, multiply, divide, power")
    logger.info("  - get_current_datetime, get_timestamp")
    logger.info("  - get_weather, get_forecast")
    logger.info("  - read_file, write_file, list_files, delete_file")
    logger.info("서버가 실행 중입니다. Ctrl+C로 종료할 수 있습니다.")

    # STDIO 전송 방식으로 서버 실행 (Claude Desktop 연동용)
    mcp.run()
