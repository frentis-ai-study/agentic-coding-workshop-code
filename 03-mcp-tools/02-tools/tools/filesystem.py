"""파일시스템 도구 - 파일 읽기/쓰기 기능을 제공합니다."""

import os
from pathlib import Path

from fastmcp.exceptions import ToolError

# 허용된 기본 디렉토리 (보안을 위해 제한)
ALLOWED_BASE_DIR = Path(__file__).parent.parent / "data"


def register_filesystem_tools(mcp):
    """파일시스템 도구들을 MCP 서버에 등록합니다.

    Args:
        mcp: FastMCP 서버 인스턴스
    """

    @mcp.tool
    def read_file(filename: str) -> str:
        """data/ 폴더 내의 파일 내용을 읽어옵니다."""
        try:
            file_path = _validate_and_resolve_path(filename)

            if not file_path.exists():
                raise ToolError(f"파일을 찾을 수 없습니다: {filename}")

            if not file_path.is_file():
                raise ToolError(f"파일이 아닙니다: {filename}")

            with open(file_path, encoding="utf-8") as f:
                return f.read()

        except OSError as e:
            raise ToolError(f"파일 읽기 실패: {str(e)}")

    @mcp.tool
    def write_file(filename: str, content: str) -> str:
        """data/ 폴더에 파일을 작성합니다."""
        try:
            file_path = _validate_and_resolve_path(filename)

            # data 디렉토리가 없으면 생성
            ALLOWED_BASE_DIR.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"파일이 성공적으로 작성되었습니다: {filename}"

        except OSError as e:
            raise ToolError(f"파일 쓰기 실패: {str(e)}")

    @mcp.tool
    def list_files() -> list[str]:
        """data/ 폴더의 모든 파일 목록을 반환합니다."""
        try:
            if not ALLOWED_BASE_DIR.exists():
                ALLOWED_BASE_DIR.mkdir(parents=True, exist_ok=True)
                return []

            files = [f.name for f in ALLOWED_BASE_DIR.iterdir() if f.is_file()]
            return sorted(files)

        except OSError as e:
            raise ToolError(f"파일 목록 조회 실패: {str(e)}")

    @mcp.tool
    def delete_file(filename: str) -> str:
        """data/ 폴더의 파일을 삭제합니다."""
        try:
            file_path = _validate_and_resolve_path(filename)

            if not file_path.exists():
                raise ToolError(f"파일을 찾을 수 없습니다: {filename}")

            if not file_path.is_file():
                raise ToolError(f"파일이 아닙니다: {filename}")

            file_path.unlink()
            return f"파일이 성공적으로 삭제되었습니다: {filename}"

        except OSError as e:
            raise ToolError(f"파일 삭제 실패: {str(e)}")


def _validate_and_resolve_path(filename: str) -> Path:
    """파일명 검증 및 경로 생성 (교육용 간소화 버전).

    경로 탐색 공격을 방지하고 허용된 디렉토리 내부만 접근 가능하도록 합니다.
    """
    if not filename:
        raise ToolError("파일명을 입력해주세요")

    # 경로 구분자 및 상대 경로 방지
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise ToolError("유효하지 않은 파일명입니다")

    # 경로 생성 및 보안 검증
    file_path = (ALLOWED_BASE_DIR / filename).resolve()

    # 허용된 디렉토리 내부인지 확인
    if not str(file_path).startswith(str(ALLOWED_BASE_DIR.resolve())):
        raise ToolError("허용되지 않는 경로입니다")

    return file_path
