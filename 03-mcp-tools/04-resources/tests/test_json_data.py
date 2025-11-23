"""동적 JSON 데이터 리소스 테스트."""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json

import pytest
from resources.json_data import get_user_data, get_user_ids, list_all_users


def test_get_existing_user():
    """존재하는 사용자를 정상적으로 조회할 수 있어야 합니다."""
    user_json = get_user_data("1")
    user = json.loads(user_json)

    assert user["id"] == "1"
    assert "name" in user
    assert "email" in user
    assert "role" in user
    assert "joined" in user


def test_get_all_users():
    """모든 사용자를 조회할 수 있어야 합니다."""
    for user_id in ["1", "2", "3"]:
        user_json = get_user_data(user_id)
        user = json.loads(user_json)
        assert user["id"] == user_id
        assert isinstance(user, dict)


def test_get_nonexistent_user():
    """존재하지 않는 사용자 조회 시 KeyError가 발생해야 합니다."""
    with pytest.raises(KeyError) as exc_info:
        get_user_data("999")

    assert "찾을 수 없습니다" in str(exc_info.value)
    assert "999" in str(exc_info.value)


def test_list_all_users():
    """전체 사용자 목록을 조회할 수 있어야 합니다."""
    users_json = list_all_users()
    users = json.loads(users_json)

    assert isinstance(users, list)
    assert len(users) == 3
    assert all("id" in user for user in users)
    assert all("name" in user for user in users)


def test_get_user_ids():
    """사용자 ID 목록을 조회할 수 있어야 합니다."""
    ids = get_user_ids()
    assert isinstance(ids, list)
    assert len(ids) > 0
    assert "1" in ids
    assert "2" in ids
    assert "3" in ids


def test_json_format():
    """반환된 데이터가 유효한 JSON 형식이어야 합니다."""
    user_json = get_user_data("1")
    # JSON 파싱이 성공해야 함
    user = json.loads(user_json)
    assert isinstance(user, dict)


def test_korean_characters():
    """한글이 올바르게 인코딩되어야 합니다."""
    user_json = get_user_data("1")
    user = json.loads(user_json)
    # 한글 이름이 올바르게 저장되어 있어야 함
    assert "김철수" in user["name"] or "이영희" in user["name"] or "박민수" in user["name"]


def test_all_users_have_required_fields():
    """모든 사용자가 필수 필드를 가지고 있어야 합니다."""
    users_json = list_all_users()
    users = json.loads(users_json)

    required_fields = ["id", "name", "email", "role", "joined"]
    for user in users:
        for field in required_fields:
            assert field in user, f"사용자 {user.get('id')}에 {field} 필드가 없습니다"
