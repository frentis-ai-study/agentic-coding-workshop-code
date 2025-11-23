"""Configuration management for MCP Chat Client."""

import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # OpenAI 호환 API 설정
    openai_api_base: str = "http://localhost:11434/v1"  # Ollama 기본값
    openai_api_key: str = "ollama"  # Ollama는 API 키 불필요
    model_name: str = "qwen3-vl:4b"  # 기본 모델

    # SQLite 데이터베이스
    database_url: str = "sqlite:///./chat_history.db"

    # Streamlit 설정
    page_title: str = "MCP Chat Client"
    page_icon: str = "🤖"

    # MCP 서버 설정 파일
    mcp_servers_config_path: str = "./mcp_servers/server_config.json"

    # 로깅
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    @property
    def is_ollama(self) -> bool:
        """Ollama를 사용 중인지 확인"""
        return "localhost:11434" in self.openai_api_base or "ollama" in self.openai_api_key.lower()


# 전역 설정 인스턴스
settings = Settings()
