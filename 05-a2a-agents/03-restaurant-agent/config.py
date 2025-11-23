"""
Configuration Settings

에이전트 서버 설정을 관리합니다.
Ollama 또는 OpenAI API를 선택할 수 있습니다.
"""

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """에이전트 설정"""

    # LLM 제공자 선택 (ollama 또는 openai)
    LLM_PROVIDER: Literal["ollama", "openai"] = os.getenv("LLM_PROVIDER", "ollama")  # type: ignore

    # Ollama 설정
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3-vl:4b")

    # OpenAI 설정
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # 동적 모델 선택
    @property
    def model_name(self) -> str:
        """현재 LLM 제공자에 따라 모델 이름 반환"""
        if self.LLM_PROVIDER == "openai":
            return self.OPENAI_MODEL
        return self.OLLAMA_MODEL

    @property
    def base_url(self) -> str:
        """현재 LLM 제공자에 따라 Base URL 반환"""
        if self.LLM_PROVIDER == "openai":
            return self.OPENAI_BASE_URL
        return f"{self.OLLAMA_BASE_URL}/v1"

    @property
    def api_key(self) -> str:
        """현재 LLM 제공자에 따라 API Key 반환"""
        if self.LLM_PROVIDER == "openai":
            return self.OPENAI_API_KEY
        return "ollama"  # Ollama는 API 키 불필요

    # mem0 클라우드 설정
    MEM0_API_KEY: str = os.getenv("MEM0_API_KEY", "")

    # 에이전트 포트 설정
    RECOMMENDER_PORT: int = int(os.getenv("RECOMMENDER_PORT", "8100"))
    BOOKING_PORT: int = int(os.getenv("BOOKING_PORT", "8101"))
    REVIEW_PORT: int = int(os.getenv("REVIEW_PORT", "8102"))

    # 에이전트 URL
    RECOMMENDER_URL: str = f"http://localhost:{RECOMMENDER_PORT}"
    BOOKING_URL: str = f"http://localhost:{BOOKING_PORT}"
    REVIEW_URL: str = f"http://localhost:{REVIEW_PORT}"


settings = Settings()
