"""LangGraph ReAct Agent with MCP Tools.

langchain-mcp-adapters를 사용하여 MCP 서버와 통합된 에이전트를 구현합니다.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .config import settings

logger = logging.getLogger(__name__)


class MCPAgent:
    """MCP 도구를 사용하는 LangGraph ReAct 에이전트."""

    def __init__(self) -> None:
        """에이전트 초기화."""
        self.model_name = settings.model_name
        self.api_base = settings.openai_api_base
        self.api_key = settings.openai_api_key
        self.mcp_client: MultiServerMCPClient | None = None
        self.agent = None
        self._initialized = False

    async def initialize(self) -> None:
        """에이전트 및 MCP 클라이언트 초기화."""
        if self._initialized:
            return

        try:
            config_path = Path(settings.mcp_servers_config_path)
            if not config_path.exists():
                logger.warning("MCP 설정 파일 없음, LLM만 사용")
                await self._initialize_without_mcp()
                return

            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)

            # 활성화된 서버만 필터링
            enabled_servers = [
                server for server in config.get("servers", []) if server.get("enabled", False)
            ]

            if not enabled_servers:
                logger.warning("활성화된 MCP 서버 없음")
                await self._initialize_without_mcp()
                return

            # MCP 서버 설정 변환
            server_configs = {}
            for server_config in enabled_servers:
                server_name = server_config.get("name", "unknown")
                server_configs[server_name] = {
                    "command": server_config.get("command"),
                    "args": server_config.get("args", []),
                    "transport": server_config.get("transport", "stdio"),
                }

            # MCP 클라이언트 및 도구 로드
            self.mcp_client = MultiServerMCPClient(server_configs)
            tools = await self.mcp_client.get_tools()
            logger.info(f"MCP 도구 {len(tools)}개 로드 완료")

            # LLM 및 에이전트 생성
            llm = ChatOpenAI(
                model=self.model_name,
                openai_api_base=self.api_base,
                openai_api_key=self.api_key,
                temperature=0.7,
            )
            self.agent = create_react_agent(llm, tools)
            self._initialized = True

        except Exception as e:
            logger.error(f"MCP 에이전트 초기화 실패: {e}")
            await self._initialize_without_mcp()

    async def _initialize_without_mcp(self) -> None:
        """MCP 없이 LLM만 사용하도록 초기화."""
        llm = ChatOpenAI(
            model=self.model_name,
            openai_api_base=self.api_base,
            openai_api_key=self.api_key,
            temperature=0.7,
        )
        self.agent = create_react_agent(llm, [])
        self._initialized = True

    async def chat(self, user_message: str, history: list[dict[str, str]] | None = None) -> str:
        """사용자 메시지에 응답합니다."""
        if not self._initialized:
            await self.initialize()

        try:
            # 메시지 히스토리를 LangChain 형식으로 변환
            messages = []
            if history:
                for msg in history:
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        messages.append(AIMessage(content=msg["content"]))

            messages.append(HumanMessage(content=user_message))

            # 에이전트 실행
            response = await self.agent.ainvoke({"messages": messages})

            # 응답 추출
            if "messages" in response and response["messages"]:
                last_message = response["messages"][-1]
                if isinstance(last_message, AIMessage):
                    return last_message.content
                return str(last_message.content)

            return "죄송합니다. 응답을 생성할 수 없습니다."

        except Exception as e:
            logger.error(f"채팅 응답 생성 중 오류: {e}")
            return f"❌ 오류 발생: {str(e)}"

    async def close(self) -> None:
        """리소스 정리."""
        if self.mcp_client:
            try:
                await self.mcp_client.cleanup()
            except Exception as e:
                logger.error(f"MCP 클라이언트 종료 오류: {e}")


_agent_instance: MCPAgent | None = None


async def get_agent() -> MCPAgent:
    """전역 에이전트 인스턴스 가져오기."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = MCPAgent()
        await _agent_instance.initialize()
    return _agent_instance
