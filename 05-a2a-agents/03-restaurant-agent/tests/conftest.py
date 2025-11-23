"""
pytest fixtures for testing

테스트에 사용되는 공통 픽스처를 정의합니다.
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from tools.restaurant_search import RestaurantSearchTool


@pytest.fixture
def test_data_path(tmp_path):
    """테스트용 restaurants.json 생성"""

    test_data = {
        "La Trattoria": {
            "name": "La Trattoria",
            "category": "이탈리안",
            "hours": "11:00-22:00",
            "phone": "02-1234-5678",
            "address": "서울 강남구 논현동 123"
        },
        "Pasta House": {
            "name": "Pasta House",
            "category": "이탈리안",
            "hours": "10:00-21:00",
            "phone": "02-2345-6789",
            "address": "서울 서초구 서초동 456"
        },
        "Seoul Grill": {
            "name": "Seoul Grill",
            "category": "한식",
            "hours": "09:00-20:00",
            "phone": "02-3456-7890",
            "address": "서울 종로구 인사동 789"
        }
    }

    data_path = tmp_path / "restaurants.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    return str(data_path)


@pytest.fixture
def search_tool(test_data_path):
    """RestaurantSearchTool 인스턴스"""
    return RestaurantSearchTool(data_path=test_data_path)


@pytest.fixture(autouse=True)
def mock_llm(request):
    """
    LLM 호출을 자동으로 mock합니다.
    integration 마커가 있는 테스트는 제외합니다.
    """
    # integration 테스트는 mock하지 않음
    if "integration" in request.keywords:
        yield
        return

    # Mock LLM 응답 생성
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "save_preference"

    # OpenAI 클라이언트 mock
    with patch("agents.recommender_agent.llm") as mock_recommender_llm, \
         patch("agents.booking_agent.llm") as mock_booking_llm:

        # chat.completions.create를 mock
        mock_recommender_llm.chat.completions.create.return_value = mock_response
        mock_booking_llm.chat.completions.create.return_value = mock_response

        yield


@pytest.fixture
def mock_mem0_client():
    """mem0 클라이언트 mock"""
    mock = MagicMock()
    mock.search_preferences.return_value = ["이탈리안 음식을 좋아함"]
    mock.save_preference.return_value = None
    return mock
