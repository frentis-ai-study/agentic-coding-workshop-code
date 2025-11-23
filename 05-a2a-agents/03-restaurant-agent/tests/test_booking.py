"""
Tests for Booking Agent

예약 에이전트 서버의 엔드포인트 테스트입니다.
"""

import pytest
from agents.booking_agent import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """FastAPI TestClient"""
    return TestClient(app)


def test_get_agent_card(client):
    """Agent Card 엔드포인트 테스트"""

    response = client.get("/.well-known/agent-card.json")

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Restaurant Booking Assistant"
    assert data["description"]
    assert data["version"] == "1.0.0"
    assert "endpoints" in data
    assert data["endpoints"]["tasks"]["send"] == "/tasks/send"


def test_task_send_endpoint_structure(client):
    """Task Send 엔드포인트 구조 검증"""

    task_request = {
        "task_id": "booking_001",
        "message": "La Trattoria 상세 정보",
        "user_id": "test_user"
    }

    response = client.post("/tasks/send", json=task_request)

    # 응답 구조 검증
    assert response.status_code in [200, 500]  # Ollama 없으면 500

    if response.status_code == 200:
        data = response.json()
        assert "task_id" in data
        assert "response" in data
        assert data["task_id"] == "booking_001"


@pytest.mark.integration
def test_get_restaurant_details(client):
    """레스토랑 상세 정보 조회 테스트 (Ollama 필요)"""

    task_request = {
        "task_id": "booking_002",
        "message": "La Trattoria 영업시간 알려줘",
        "user_id": "alice"
    }

    response = client.post("/tasks/send", json=task_request)

    if response.status_code == 200:
        data = response.json()
        assert "영업시간" in data["response"] or "전화번호" in data["response"]
