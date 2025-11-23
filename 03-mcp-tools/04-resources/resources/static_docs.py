"""정적 마크다운 문서 리소스 제공."""

# 정적 문서 데이터 저장소
STATIC_DOCS: dict[str, str] = {
    "intro": """# MCP 리소스 소개

MCP(Model Context Protocol) 리소스는 AI 모델에게 구조화된 정보를 제공하는 방법입니다.

## 주요 특징
- **정적 리소스**: 변하지 않는 고정된 데이터
- **동적 리소스**: 요청 시점에 생성되는 데이터
- **파일 리소스**: 파일 시스템의 실제 파일

## URI 스키마
리소스는 고유한 URI로 식별됩니다 (예: `doc://intro`, `data://users/1`).
""",
    "quickstart": """# MCP 빠른 시작 가이드

## 1. 서버 생성
```python
from fastmcp import FastMCP
mcp = FastMCP("MyServer")
```

## 2. 리소스 등록
```python
@mcp.resource("doc://guide")
def get_guide() -> str:
    return "가이드 내용"
```

## 3. 서버 실행
```python
mcp.run()
```
""",
    "examples": """# MCP 리소스 예제

## 예제 1: 정적 텍스트
```python
@mcp.resource("doc://welcome")
def welcome() -> str:
    return "환영합니다!"
```

## 예제 2: 동적 데이터
```python
@mcp.resource("data://user/{id}")
def get_user(id: str) -> str:
    return f"사용자 ID: {id}"
```

## 예제 3: 파일 리소스
```python
from pathlib import Path

@mcp.resource("file://{filename}")
def get_file(filename: str) -> str:
    return Path(filename).read_text()
```
""",
}


def get_static_doc(name: str) -> str:
    """정적 문서를 반환합니다.

    Args:
        name: 문서 이름 (intro, quickstart, examples 중 하나)

    Returns:
        마크다운 형식의 문서 내용

    Raises:
        KeyError: 존재하지 않는 문서 이름인 경우
    """
    if name not in STATIC_DOCS:
        available = ", ".join(STATIC_DOCS.keys())
        raise KeyError(f"문서 '{name}'을(를) 찾을 수 없습니다. 사용 가능한 문서: {available}")
    return STATIC_DOCS[name]


def list_static_docs() -> list[str]:
    """사용 가능한 모든 정적 문서 목록을 반환합니다.

    Returns:
        문서 이름 리스트
    """
    return list(STATIC_DOCS.keys())
