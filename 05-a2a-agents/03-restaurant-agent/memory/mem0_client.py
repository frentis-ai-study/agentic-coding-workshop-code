"""
mem0 Cloud Client

Mem0 Cloud Platform을 사용하는 클라이언트입니다.
로컬 설정 없이 API 키만으로 즉시 사용 가능합니다.
"""

import os

from mem0 import MemoryClient


class Mem0Client:
    """mem0 클라우드 메모리 클라이언트"""

    def __init__(self):
        """mem0 Cloud API 초기화"""
        # API 키 검증
        api_key = os.getenv("MEM0_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ MEM0_API_KEY 환경 변수가 필요합니다.\n"
                "🔗 https://app.mem0.ai/ 에서 API 키를 발급받으세요.\n"
                "💡 무료 티어: 1000 메모리/월\n\n"
                "설정 방법:\n"
                "1. .env 파일에 추가: MEM0_API_KEY=m0-...\n"
                "2. 또는 환경 변수 설정: export MEM0_API_KEY=m0-..."
            )

        # 클라우드 클라이언트 초기화 (환경 변수 자동 인식)
        try:
            self.memory = MemoryClient()
        except Exception as e:
            error_msg = str(e).lower()
            if "401" in str(e) or "unauthorized" in error_msg:
                raise ValueError(
                    "❌ Mem0 API 키가 유효하지 않습니다.\n"
                    "🔗 https://app.mem0.ai/ 에서 API 키를 확인하세요."
                ) from e
            elif "network" in error_msg or "connection" in error_msg:
                raise ValueError(
                    "❌ 네트워크 연결에 실패했습니다.\n"
                    "💡 인터넷 연결을 확인하세요."
                ) from e
            else:
                raise

    def save_preference(self, user_id: str, content: str) -> dict:
        """
        사용자 선호도 저장

        Args:
            user_id: 사용자 ID
            content: 선호도 내용 (예: "이탈리안 음식을 좋아함")

        Returns:
            저장 결과 dict

        Example:
            >>> client = Mem0Client()
            >>> result = client.save_preference("alice", "이탈리안 음식을 좋아함")
            >>> result["results"][0]["id"]
            'mem_001'
        """
        return self.memory.add(
            content,
            user_id=user_id,
            metadata={"category": "food_preference"}
        )

    def search_preferences(self, user_id: str, query: str) -> list[str]:
        """
        사용자 선호도 검색

        Args:
            user_id: 사용자 ID
            query: 검색 쿼리 (예: "음식 선호도")

        Returns:
            검색된 선호도 목록

        Example:
            >>> client = Mem0Client()
            >>> prefs = client.search_preferences("alice", "음식 선호도")
            >>> prefs
            ['이탈리안 음식을 좋아함', '매운 음식을 싫어함']
        """
        results = self.memory.search(query=query, user_id=user_id)

        memories = []
        for result in results.get("results", []):
            memories.append(result["memory"])

        return memories

    def get_all_preferences(self, user_id: str) -> list[str]:
        """
        사용자의 모든 선호도 조회

        Args:
            user_id: 사용자 ID

        Returns:
            전체 선호도 목록

        Example:
            >>> client = Mem0Client()
            >>> all_prefs = client.get_all_preferences("alice")
            >>> len(all_prefs)
            3
        """
        try:
            # Mem0 v1.0 V2 API: filters 파라미터 필수
            response = self.memory.get_all(
                filters={"AND": [{"user_id": user_id}]},
                version="v2"
            )
            memories = []
            for result in response.get("results", []):
                memories.append(result["memory"])
            return memories
        except Exception as e:
            # 메모리가 없거나 조회 실패 시 빈 리스트 반환
            print(f"get_all_preferences 오류: {e}")
            return []

    def delete_memory(self, memory_id: str) -> dict:
        """
        특정 메모리 삭제

        Args:
            memory_id: 메모리 ID

        Returns:
            삭제 결과 dict

        Example:
            >>> client = Mem0Client()
            >>> result = client.delete_memory("mem_001")
            >>> result["success"]
            True
        """
        return self.memory.delete(memory_id=memory_id)

    def delete_all_preferences(self, user_id: str) -> dict:
        """
        사용자의 모든 메모리 삭제 (초기화)

        Args:
            user_id: 사용자 ID

        Returns:
            삭제 결과 dict

        Example:
            >>> client = Mem0Client()
            >>> result = client.delete_all_preferences("alice")
            >>> result["success"]
            True
        """
        return self.memory.delete_all(user_id=user_id)

    def get_all_memories_with_ids(self, user_id: str) -> list[dict]:
        """
        사용자의 모든 메모리를 ID와 함께 조회

        Args:
            user_id: 사용자 ID

        Returns:
            메모리 목록 (각 항목은 {"id": str, "memory": str} 형식)

        Example:
            >>> client = Mem0Client()
            >>> memories = client.get_all_memories_with_ids("alice")
            >>> memories[0]
            {"id": "mem_001", "memory": "이탈리안 음식을 좋아함"}
        """
        try:
            # Mem0 v1.0 V2 API: filters 파라미터 필수
            response = self.memory.get_all(
                filters={"AND": [{"user_id": user_id}]},
                version="v2"
            )
            memories = []
            for result in response.get("results", []):
                memories.append({
                    "id": result["id"],
                    "memory": result["memory"]
                })
            return memories
        except Exception as e:
            # 메모리가 없거나 조회 실패 시 빈 리스트 반환
            print(f"get_all_memories_with_ids 오류: {e}")
            return []
