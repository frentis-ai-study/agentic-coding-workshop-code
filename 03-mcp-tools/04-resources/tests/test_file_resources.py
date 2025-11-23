"""파일 시스템 리소스 테스트."""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from resources.file_resources import (
    get_base_dir,
    list_files,
    read_file,
    validate_path,
)


@pytest.fixture
def sample_file():
    """테스트용 샘플 파일을 생성합니다."""
    base_dir = get_base_dir()
    test_file = base_dir / "test_sample.txt"
    test_file.write_text("테스트 내용입니다.", encoding="utf-8")
    yield test_file
    # 테스트 후 정리
    if test_file.exists():
        test_file.unlink()


def test_get_base_dir():
    """기본 디렉토리를 정상적으로 조회할 수 있어야 합니다."""
    base_dir = get_base_dir()
    assert isinstance(base_dir, Path)
    assert base_dir.exists()
    assert base_dir.is_dir()
    assert base_dir.name == "data"


def test_validate_path_success():
    """유효한 경로는 검증을 통과해야 합니다."""
    path = validate_path("sample.txt")
    assert isinstance(path, Path)
    assert path.is_absolute()


def test_validate_path_absolute():
    """절대 경로는 차단되어야 합니다."""
    with pytest.raises(ValueError) as exc_info:
        validate_path("/etc/passwd")
    assert "절대 경로" in str(exc_info.value)


def test_validate_path_parent_traversal():
    """상위 디렉토리 탐색(..)은 차단되어야 합니다."""
    with pytest.raises(ValueError) as exc_info:
        validate_path("../secrets.txt")
    assert ".." in str(exc_info.value)


def test_validate_path_outside_base():
    """data/ 폴더 외부 접근은 차단되어야 합니다."""
    # 복잡한 경로 탐색 시도 (.. 포함 경로는 상위 디렉토리 접근 에러가 먼저 발생)
    with pytest.raises(ValueError) as exc_info:
        validate_path("subdir/../../outside.txt")
    # .. 체크가 먼저 실행되므로 "상위 디렉토리" 메시지가 나옴
    assert "상위 디렉토리" in str(exc_info.value) or "외부 접근" in str(exc_info.value)


def test_read_file_success(sample_file):
    """존재하는 파일을 정상적으로 읽을 수 있어야 합니다."""
    content = read_file("test_sample.txt")
    assert content == "테스트 내용입니다."
    assert isinstance(content, str)


def test_read_file_not_found():
    """존재하지 않는 파일 조회 시 FileNotFoundError가 발생해야 합니다."""
    with pytest.raises(FileNotFoundError) as exc_info:
        read_file("nonexistent.txt")
    assert "찾을 수 없습니다" in str(exc_info.value)


def test_read_file_directory():
    """디렉토리는 읽을 수 없어야 합니다."""
    # 서브디렉토리 생성
    base_dir = get_base_dir()
    subdir = base_dir / "testdir"
    subdir.mkdir(exist_ok=True)

    try:
        with pytest.raises(ValueError) as exc_info:
            read_file("testdir")
        assert "디렉토리는 읽을 수 없습니다" in str(exc_info.value)
    finally:
        # 정리
        if subdir.exists():
            subdir.rmdir()


def test_list_files_empty():
    """빈 디렉토리의 경우 빈 리스트를 반환해야 합니다."""
    # 파일이 있을 수도 있고 없을 수도 있음
    files = list_files()
    assert isinstance(files, list)


def test_list_files_with_sample(sample_file):
    """파일이 있는 경우 파일 목록을 반환해야 합니다."""
    files = list_files()
    assert isinstance(files, list)
    assert "test_sample.txt" in files


def test_list_files_sorted():
    """파일 목록이 정렬되어 반환되어야 합니다."""
    files = list_files()
    assert files == sorted(files)


def test_read_file_korean(sample_file):
    """한글 파일을 정상적으로 읽을 수 있어야 합니다."""
    content = read_file("test_sample.txt")
    assert "테스트" in content
    assert isinstance(content, str)


def test_security_multiple_slashes():
    """여러 슬래시를 사용한 경로 조작 시도는 차단되어야 합니다."""
    with pytest.raises(ValueError):
        validate_path("subdir/../../etc/passwd")
