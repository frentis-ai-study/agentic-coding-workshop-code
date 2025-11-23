"""Pytest configuration and shared fixtures."""

import os
import sys
from pathlib import Path

import pytest

# 백엔드 모듈을 import할 수 있도록 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def test_env():
    """테스트용 환경변수 설정."""
    original_env = os.environ.copy()

    # 테스트 환경변수 설정
    os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
    os.environ["OPENAI_API_KEY"] = "test-key"
    os.environ["MODEL_NAME"] = "test-model"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    yield

    # 원래 환경변수 복원
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_chat_history():
    """샘플 채팅 기록."""
    return [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you!"},
    ]
