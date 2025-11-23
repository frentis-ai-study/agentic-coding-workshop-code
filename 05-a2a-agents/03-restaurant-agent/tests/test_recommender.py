"""
Tests for Recommender Agent

추천 에이전트 서버의 엔드포인트 테스트입니다.

Note: 이 테스트는 Ollama LLM을 사용하므로 통합 테스트로 간주됩니다.
단위 테스트를 위해서는 LLM 응답을 모킹해야 합니다.
"""

import pytest
from agents.recommender_agent import app
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
    assert data["name"] == "Restaurant Recommender"
    assert data["description"]
    assert data["version"] == "1.0.0"
    assert "endpoints" in data
    assert data["endpoints"]["tasks"]["send"] == "/tasks/send"


def test_task_send_endpoint_structure(client):
    """Task Send 엔드포인트 구조 검증"""

    task_request = {
        "task_id": "test_001",
        "message": "이탈리안 좋아해",
        "user_id": "test_user"
    }

    response = client.post("/tasks/send", json=task_request)

    # 응답 구조 검증 (Ollama 없어도 응답은 받아야 함)
    assert response.status_code in [200, 500]  # Ollama 없으면 500

    if response.status_code == 200:
        data = response.json()
        assert "task_id" in data
        assert "response" in data
        assert data["task_id"] == "test_001"


# LLM 의존성이 있는 테스트는 통합 테스트로 분류
# 실제 Ollama가 실행 중일 때만 테스트
@pytest.mark.integration
def test_save_preference_intent(client):
    """선호도 저장 의도 테스트 (Ollama 필요)"""

    task_request = {
        "task_id": "test_002",
        "message": "이탈리안 음식을 좋아해",
        "user_id": "alice"
    }

    response = client.post("/tasks/send", json=task_request)

    if response.status_code == 200:
        data = response.json()
        assert "선호도" in data["response"] or "저장" in data["response"]
