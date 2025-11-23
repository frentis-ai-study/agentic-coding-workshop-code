"""
Agent Memory: 에이전트 메모리 통합

Mem0 Cloud를 사용하여 대화 중 사용자 선호도를 자동으로 저장하고,
다음 대화에서 개인화된 응답을 제공하는 예제입니다.

요구사항:
- MEM0_API_KEY 환경 변수 설정 (https://app.mem0.ai/)
- LLM: Ollama (기본) 또는 OpenAI
  - Ollama 사용 시: qwen3-vl:4b 모델 필요 (ollama pull qwen3-vl:4b)
"""

import os

from mem0 import MemoryClient
from openai import OpenAI


class ChatAgent:
    """mem0 클라우드 메모리를 사용하는 간단한 챗봇 에이전트"""

    def __init__(self, user_id: str):
        """
        Args:
            user_id: 사용자 ID (메모리 분리용)
        """
        self.user_id = user_id

        # Mem0 Cloud 초기화
        if not os.getenv("MEM0_API_KEY"):
            raise ValueError(
                "❌ MEM0_API_KEY 환경 변수가 필요합니다.\n"
                "🔗 https://app.mem0.ai/ 에서 API 키를 발급받으세요.\n"
                "💡 무료 티어: 1000 메모리/월"
            )

        self.memory = MemoryClient()

        # LLM 클라이언트 초기화 (Ollama 기본, OpenAI 사용 시 환경변수 설정)
        llm_provider = os.getenv("LLM_PROVIDER", "ollama")

        if llm_provider == "openai":
            self.llm = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            )
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        else:  # ollama
            self.llm = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama"  # Ollama는 API 키가 필요 없지만 형식상 필요
            )
            self.model = os.getenv("OLLAMA_MODEL", "qwen3-vl:4b")

    def chat(self, user_message: str) -> str:
        """
        사용자 메시지에 응답하고, 선호도를 메모리에 저장합니다.

        Args:
            user_message: 사용자 메시지

        Returns:
            에이전트 응답
        """

        # 1. 이전 메모리 검색 (클라우드에서)
        memories = self.memory.search(
            query=user_message,
            user_id=self.user_id
        )

        context = ""
        if memories['results']:
            context = "사용자에 대해 알고 있는 정보:\n"
            for mem in memories['results']:
                context += f"- {mem['memory']}\n"
            context += "\n"

        # 2. LLM에게 응답 생성 요청
        prompt = f"""{context}사용자: {user_message}

위 메시지에 친절하게 응답하세요. 이전 대화 내용을 기억하고 있다면 개인화된 응답을 제공하세요.
"""

        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        agent_response = response.choices[0].message.content

        # 3. 사용자 메시지를 클라우드 메모리에 저장 (선호도 자동 저장)
        self.memory.add(
            user_message,
            user_id=self.user_id,
            metadata={"type": "conversation"}
        )

        return agent_response

    def show_all_memories(self):
        """클라우드에 저장된 모든 메모리 출력"""
        all_memories = self.memory.get_all(user_id=self.user_id)

        if not all_memories['results']:
            print("저장된 메모리가 없습니다.")
            return

        print(f"\n=== {self.user_id}의 전체 메모리 (클라우드) ===")
        for mem in all_memories['results']:
            print(f"  - {mem['memory']}")
        print()


def main():
    """에이전트 메모리 데모"""

    print("=== mem0 Cloud + LLM 챗봇 에이전트 ===\n")

    # MEM0 API 키 확인
    if not os.getenv("MEM0_API_KEY"):
        print("❌ MEM0_API_KEY 환경 변수가 필요합니다.")
        print("🔗 https://app.mem0.ai/ 에서 API 키를 발급받으세요.")
        print("💡 무료 티어: 1000 메모리/월\n")
        print("설정 방법:")
        print("  export MEM0_API_KEY=m0-...")
        return

    print("✅ Mem0 Cloud 연결 준비\n")

    # LLM 제공자 확인 및 Ollama 체크
    llm_provider = os.getenv("LLM_PROVIDER", "ollama")
    if llm_provider == "ollama":
        ollama_running = os.system("curl -s http://localhost:11434/api/tags > /dev/null 2>&1") == 0
        if not ollama_running:
            print("❌ Ollama가 실행되지 않았습니다.")
            print("   다음 명령어로 Ollama를 실행하세요:")
            print("   $ ollama serve")
            return
        print("✅ Ollama 연결 확인\n")
    else:
        print(f"✅ LLM 제공자: {llm_provider}\n")

    # Alice 에이전트 생성
    alice_agent = ChatAgent(user_id="alice")

    # 첫 번째 대화: 선호도 저장
    print("=== 첫 번째 대화: 선호도 저장 ===")
    user_msg_1 = "안녕! 나는 이탈리안 음식을 정말 좋아해."
    print(f"사용자: {user_msg_1}")

    response_1 = alice_agent.chat(user_msg_1)
    print(f"에이전트: {response_1}\n")

    # 두 번째 대화: 추가 선호도 저장
    print("=== 두 번째 대화: 추가 선호도 ===")
    user_msg_2 = "그리고 매운 음식은 잘 못 먹어."
    print(f"사용자: {user_msg_2}")

    response_2 = alice_agent.chat(user_msg_2)
    print(f"에이전트: {response_2}\n")

    # 저장된 메모리 확인
    alice_agent.show_all_memories()

    # 세 번째 대화: 메모리 기반 개인화된 응답
    print("=== 세 번째 대화: 개인화된 추천 ===")
    user_msg_3 = "저녁 먹을 곳 추천해줘!"
    print(f"사용자: {user_msg_3}")

    response_3 = alice_agent.chat(user_msg_3)
    print(f"에이전트: {response_3}\n")

    print("=== 완료 ===")
    print("✅ 에이전트가 이전 대화(이탈리안 좋아함, 매운 음식 싫어함)를")
    print("   클라우드 메모리에서 불러와 개인화된 추천을 제공했습니다!")
    print("\n다음 단계: 03-restaurant-agent에서 A2A 에이전트와 mem0 통합")


if __name__ == "__main__":
    main()
