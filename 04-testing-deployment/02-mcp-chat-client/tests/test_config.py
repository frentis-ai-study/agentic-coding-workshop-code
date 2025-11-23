"""Configuration tests for MCP Chat Client."""

import os
from pathlib import Path

import pytest

from backend.config import Settings


class TestSettings:
    """Settings 클래스 테스트."""

    def test_default_settings(self):
        """기본 설정 테스트."""
        settings = Settings()

        assert settings.openai_api_base == "http://localhost:11434/v1"
        assert settings.openai_api_key == "ollama"
        assert settings.model_name == "qwen3-vl:4b"
        assert settings.page_title == "MCP Chat Client"
        assert settings.page_icon == "🤖"

    def test_is_ollama_property(self):
        """Ollama 모드 감지 테스트."""
        # Ollama 설정
        settings = Settings(
            openai_api_base="http://localhost:11434/v1",
            openai_api_key="ollama",
        )
        assert settings.is_ollama is True

        # OpenAI 설정
        settings = Settings(
            openai_api_base="https://api.openai.com/v1",
            openai_api_key="sk-xxx",
        )
        assert settings.is_ollama is False

    def test_custom_settings(self):
        """커스텀 설정 테스트."""
        settings = Settings(
            model_name="gpt-4",
            page_title="Custom Chat",
            database_url="sqlite:///custom.db",
        )

        assert settings.model_name == "gpt-4"
        assert settings.page_title == "Custom Chat"
        assert settings.database_url == "sqlite:///custom.db"

    def test_env_file_loading(self, tmp_path):
        """환경변수 파일 로딩 테스트."""
        # 임시 .env 파일 생성
        env_file = tmp_path / ".env"
        env_file.write_text(
            """
OPENAI_API_BASE=https://custom-api.com/v1
OPENAI_API_KEY=test-key
MODEL_NAME=custom-model
PAGE_TITLE=Test Chat
        """.strip()
        )

        # 설정 로드
        settings = Settings(_env_file=str(env_file))

        assert settings.openai_api_base == "https://custom-api.com/v1"
        assert settings.openai_api_key == "test-key"
        assert settings.model_name == "custom-model"
        assert settings.page_title == "Test Chat"

    def test_log_level_validation(self):
        """로그 레벨 유효성 검사."""
        # 유효한 레벨
        for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            settings = Settings(log_level=level)
            assert settings.log_level == level

    def test_database_url_formats(self):
        """다양한 데이터베이스 URL 형식 테스트."""
        # SQLite 파일
        settings = Settings(database_url="sqlite:///./test.db")
        assert settings.database_url == "sqlite:///./test.db"

        # 메모리 DB
        settings = Settings(database_url="sqlite:///:memory:")
        assert settings.database_url == "sqlite:///:memory:"
