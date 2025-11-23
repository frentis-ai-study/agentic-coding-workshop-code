"""MCP 리소스 제공 예제.

이 예제는 3가지 유형의 리소스를 제공하는 MCP 서버를 구현합니다:
1. 정적 문서 리소스 (doc://{name})
2. 동적 JSON 데이터 리소스 (data://users/{id})
3. 파일 시스템 리소스 (file://{filename})
"""

from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError
from resources.file_resources import list_files, read_file
from resources.json_data import get_user_data, get_user_ids, list_all_users
from resources.static_docs import get_static_doc, list_static_docs

# FastMCP 서버 생성
mcp = FastMCP("ResourceServer", version="1.0.0")


@mcp.resource("doc://{name}")
def get_document(name: str) -> str:
    """정적 마크다운 문서를 제공합니다.

    사용 가능한 문서:
    - doc://intro - MCP 리소스 소개
    - doc://quickstart - MCP 빠른 시작 가이드
    - doc://examples - MCP 리소스 예제

    Args:
        name: 문서 이름

    Returns:
        마크다운 형식의 문서 내용
    """
    try:
        return get_static_doc(name)
    except KeyError as e:
        raise ResourceError(str(e))


@mcp.resource("data://users/{user_id}")
def get_user(user_id: str) -> str:
    """사용자 정보를 JSON 형식으로 제공합니다.

    사용 가능한 사용자 ID: 1, 2, 3

    Args:
        user_id: 조회할 사용자 ID

    Returns:
        사용자 정보를 담은 JSON 문자열
    """
    try:
        return get_user_data(user_id)
    except KeyError as e:
        raise ResourceError(str(e))


@mcp.resource("data://users")
def get_all_users() -> str:
    """전체 사용자 목록을 JSON 형식으로 제공합니다.

    Returns:
        전체 사용자 목록을 담은 JSON 문자열
    """
    return list_all_users()


@mcp.resource("file://{filename}/")
def get_file(filename: str) -> str:
    """data/ 폴더 내의 파일 내용을 제공합니다.

    보안 제한:
    - data/ 폴더 외부 접근 차단
    - 상대 경로 탐색(..) 차단
    - 절대 경로 차단

    Args:
        filename: 읽을 파일명 (data/ 폴더 기준 상대 경로)

    Returns:
        파일 내용
    """
    try:
        # 슬래시 제거
        filename = filename.rstrip("/")
        return read_file(filename)
    except (ValueError, FileNotFoundError) as e:
        raise ResourceError(str(e))


@mcp.resource("file://list/")
def list_available_files() -> str:
    """data/ 폴더 내의 사용 가능한 파일 목록을 제공합니다.

    Returns:
        파일 목록을 담은 JSON 문자열
    """
    import json

    files = list_files()
    return json.dumps({"files": files, "count": len(files)}, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print("🚀 MCP 리소스 서버 시작")
    print("\n사용 가능한 리소스:")
    print("\n📄 정적 문서:")
    for doc_name in list_static_docs():
        print(f"  - doc://{doc_name}")
    print("\n👤 사용자 데이터:")
    print("  - data://users (전체 목록)")
    for user_id in get_user_ids():
        print(f"  - data://users/{user_id}")
    print("\n📁 파일 리소스:")
    print("  - file://list (파일 목록)")
    print("  - file://{filename} (data/ 폴더 내 파일)")
    files = list_files()
    if files:
        print(f"\n  현재 사용 가능한 파일: {len(files)}개")
        for file in files[:5]:
            print(f"    - file://{file}")
        if len(files) > 5:
            print(f"    ... 외 {len(files) - 5}개")
    else:
        print("  (아직 파일이 없습니다. data/ 폴더에 파일을 추가하세요)")
    print("\n서버 실행 중...\n")

    mcp.run()
