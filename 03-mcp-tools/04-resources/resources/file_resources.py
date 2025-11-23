"""파일 시스템 리소스 제공."""

from pathlib import Path


def get_base_dir() -> Path:
    """리소스 파일의 기본 디렉토리를 반환합니다.

    Returns:
        data/ 디렉토리의 절대 경로
    """
    current_file = Path(__file__).resolve()
    base_dir = current_file.parent.parent / "data"
    base_dir.mkdir(exist_ok=True)
    return base_dir


def validate_path(filename: str) -> Path:
    """파일 경로를 검증하고 안전한 경로를 반환합니다.

    보안 검증:
    - 절대 경로 차단
    - 상대 경로 탐색(..) 차단
    - data/ 폴더 외부 접근 차단

    Args:
        filename: 접근하려는 파일명

    Returns:
        검증된 파일의 절대 경로

    Raises:
        ValueError: 보안 위반이 감지된 경우
    """
    # 절대 경로 차단
    if Path(filename).is_absolute():
        raise ValueError(f"절대 경로는 허용되지 않습니다: {filename}\n상대 경로를 사용해주세요.")

    # .. 경로 탐색 차단
    if ".." in filename:
        raise ValueError(f"상위 디렉토리 접근(..)은 허용되지 않습니다: {filename}")

    # 안전한 경로 생성
    base_dir = get_base_dir()
    file_path = (base_dir / filename).resolve()

    # data/ 폴더 외부 접근 차단
    try:
        file_path.relative_to(base_dir)
    except ValueError:
        raise ValueError(
            f"data/ 폴더 외부 접근이 차단되었습니다: {filename}\n허용된 기본 경로: {base_dir}"
        )

    return file_path


def read_file(filename: str) -> str:
    """data/ 폴더 내의 파일을 읽어 반환합니다.

    Args:
        filename: 읽을 파일명 (data/ 폴더 기준 상대 경로)

    Returns:
        파일 내용

    Raises:
        ValueError: 보안 위반이 감지된 경우
        FileNotFoundError: 파일이 존재하지 않는 경우
    """
    file_path = validate_path(filename)

    if not file_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}\n전체 경로: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"디렉토리는 읽을 수 없습니다: {filename}")

    return file_path.read_text(encoding="utf-8")


def list_files() -> list[str]:
    """data/ 폴더 내의 모든 파일 목록을 반환합니다.

    Returns:
        파일명 리스트 (data/ 폴더 기준 상대 경로)
    """
    base_dir = get_base_dir()
    files = []

    for file_path in base_dir.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(base_dir)
            files.append(str(relative_path))

    return sorted(files)
