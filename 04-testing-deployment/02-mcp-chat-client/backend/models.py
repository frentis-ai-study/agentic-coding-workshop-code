"""Data models for MCP Chat Client."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """채팅 메시지 모델."""

    role: Literal["user", "assistant", "system"] = Field(..., description="메시지 역할")
    content: str = Field(..., description="메시지 내용")
    timestamp: datetime = Field(default_factory=datetime.now, description="생성 시간")
    session_id: str | None = Field(None, description="세션 ID")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Hello, MCP!",
                "timestamp": "2025-01-22T12:00:00",
                "session_id": "session_123",
            }
        }


class ChatSession(BaseModel):
    """채팅 세션 모델."""

    session_id: str = Field(..., description="세션 고유 ID")
    title: str = Field(default="New Conversation", description="세션 제목")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
    updated_at: datetime = Field(default_factory=datetime.now, description="마지막 업데이트")
    message_count: int = Field(default=0, description="메시지 개수")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "title": "Weather Query",
                "created_at": "2025-01-22T12:00:00",
                "updated_at": "2025-01-22T12:05:00",
                "message_count": 10,
            }
        }


class MCPServerConfig(BaseModel):
    """MCP 서버 설정 모델."""

    name: str = Field(..., description="서버 이름")
    command: str = Field(..., description="실행 명령")
    args: list[str] = Field(default_factory=list, description="명령 인자")
    transport: Literal["stdio", "streamable_http"] = Field(..., description="전송 방식")
    url: str | None = Field(None, description="HTTP URL (streamable_http 전용)")
    enabled: bool = Field(default=True, description="활성화 여부")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "calculator",
                "command": "uv",
                "args": ["run", "python", "../03-mcp-tools/02-tools/main.py"],
                "transport": "stdio",
                "enabled": True,
            }
        }


class AgentResponse(BaseModel):
    """LangGraph 에이전트 응답 모델."""

    content: str = Field(..., description="응답 내용")
    tool_calls: list[dict] = Field(default_factory=list, description="사용된 도구 호출")
    intermediate_steps: list[dict] = Field(default_factory=list, description="중간 단계")
    finish_reason: str = Field(default="stop", description="종료 이유")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "The calculation result is 8.",
                "tool_calls": [{"tool": "add", "args": {"a": 5, "b": 3}}],
                "intermediate_steps": [],
                "finish_reason": "stop",
            }
        }
