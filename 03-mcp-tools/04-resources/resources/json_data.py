"""동적 JSON 데이터 리소스 제공."""

import json
from typing import Any

# 샘플 사용자 데이터베이스
USERS_DB: dict[str, dict[str, Any]] = {
    "1": {
        "id": "1",
        "name": "김철수",
        "email": "kim@example.com",
        "role": "개발자",
        "joined": "2024-01-15",
    },
    "2": {
        "id": "2",
        "name": "이영희",
        "email": "lee@example.com",
        "role": "디자이너",
        "joined": "2024-02-20",
    },
    "3": {
        "id": "3",
        "name": "박민수",
        "email": "park@example.com",
        "role": "매니저",
        "joined": "2024-03-10",
    },
}


def get_user_data(user_id: str) -> str:
    """사용자 ID로 사용자 정보를 JSON 형식으로 반환합니다.

    Args:
        user_id: 조회할 사용자 ID

    Returns:
        사용자 정보를 담은 JSON 문자열

    Raises:
        KeyError: 존재하지 않는 사용자 ID인 경우
    """
    if user_id not in USERS_DB:
        raise KeyError(
            f"사용자 ID '{user_id}'을(를) 찾을 수 없습니다. "
            f"사용 가능한 ID: {', '.join(USERS_DB.keys())}"
        )
    return json.dumps(USERS_DB[user_id], ensure_ascii=False, indent=2)


def list_all_users() -> str:
    """모든 사용자 목록을 JSON 형식으로 반환합니다.

    Returns:
        전체 사용자 목록을 담은 JSON 문자열
    """
    users_list = list(USERS_DB.values())
    return json.dumps(users_list, ensure_ascii=False, indent=2)


def get_user_ids() -> list[str]:
    """사용 가능한 모든 사용자 ID 목록을 반환합니다.

    Returns:
        사용자 ID 리스트
    """
    return list(USERS_DB.keys())
