"""정적 문서 리소스 테스트."""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from resources.static_docs import get_static_doc, list_static_docs


def test_get_existing_doc():
    """존재하는 문서를 정상적으로 조회할 수 있어야 합니다."""
    doc = get_static_doc("intro")
    assert "MCP 리소스 소개" in doc
    assert isinstance(doc, str)
    assert len(doc) > 0


def test_get_all_available_docs():
    """모든 사용 가능한 문서를 조회할 수 있어야 합니다."""
    for doc_name in ["intro", "quickstart", "examples"]:
        doc = get_static_doc(doc_name)
        assert isinstance(doc, str)
        assert len(doc) > 0


def test_get_nonexistent_doc():
    """존재하지 않는 문서 조회 시 KeyError가 발생해야 합니다."""
    with pytest.raises(KeyError) as exc_info:
        get_static_doc("nonexistent")

    assert "찾을 수 없습니다" in str(exc_info.value)
    assert "nonexistent" in str(exc_info.value)


def test_list_static_docs():
    """문서 목록을 정상적으로 조회할 수 있어야 합니다."""
    docs = list_static_docs()
    assert isinstance(docs, list)
    assert len(docs) > 0
    assert "intro" in docs
    assert "quickstart" in docs
    assert "examples" in docs


def test_doc_content_format():
    """문서 내용이 마크다운 형식이어야 합니다."""
    doc = get_static_doc("intro")
    # 마크다운 헤더 확인
    assert "#" in doc


def test_quickstart_has_code_examples():
    """빠른 시작 가이드에 코드 예제가 포함되어야 합니다."""
    doc = get_static_doc("quickstart")
    assert "```python" in doc
    assert "FastMCP" in doc
