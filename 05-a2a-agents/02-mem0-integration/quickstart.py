"""
mem0 Cloud Quickstart: 기본 사용법

Mem0 Cloud Platform을 사용하여 메모리를 저장, 검색, 조회하는 기본 예제입니다.
API 키만 있으면 즉시 사용 가능합니다.
"""

import os

from mem0 import MemoryClient


def main():
    """mem0 클라우드 기본 사용법 데모"""

    # API 키 확인
    if not os.getenv("MEM0_API_KEY"):
        print("❌ MEM0_API_KEY 환경 변수가 필요합니다.")
        print("🔗 https://app.mem0.ai/ 에서 API 키를 발급받으세요.")
        print("💡 무료 티어: 1000 메모리/월\n")
        print("설정 방법:")
        print("  export MEM0_API_KEY=m0-...")
        return

    # 1. MemoryClient 초기화 (클라우드)
    print("=== mem0 Cloud 초기화 ===")
    memory = MemoryClient()
    print("✅ Mem0 Cloud 연결 완료\n")

    # 2. 메모리 저장 (사용자별로 분리)
    print("=== 메모리 저장 ===")

    # Alice의 선호도
    alice_memories = [
        "이탈리안 음식을 좋아해",
        "매운 음식을 싫어해",
        "저녁 7시 이후에 식사를 선호해"
    ]

    for content in alice_memories:
        result = memory.add(
            content,
            user_id="alice",
            metadata={"category": "food_preference"}
        )
        print(f"✅ Alice 메모리 저장: {content}")
        print(f"   Memory ID: {result['results'][0]['id']}\n")

    # Bob의 선호도
    bob_memories = [
        "한식을 좋아해",
        "채식주의자야"
    ]

    for content in bob_memories:
        result = memory.add(
            content,
            user_id="bob",
            metadata={"category": "food_preference"}
        )
        print(f"✅ Bob 메모리 저장: {content}")
        print(f"   Memory ID: {result['results'][0]['id']}\n")

    # 3. 메모리 검색 (사용자별, 쿼리 기반)
    print("=== 메모리 검색 ===")

    # Alice의 음식 선호도 검색
    alice_prefs = memory.search(
        query="음식 선호도가 뭐야?",
        user_id="alice"
    )

    print("Alice의 음식 선호도:")
    for mem in alice_prefs['results']:
        print(f"  - {mem['memory']}")
    print()

    # Bob의 음식 선호도 검색
    bob_prefs = memory.search(
        query="음식 선호도가 뭐야?",
        user_id="bob"
    )

    print("Bob의 음식 선호도:")
    for mem in bob_prefs['results']:
        print(f"  - {mem['memory']}")
    print()

    # 4. 모든 메모리 조회 (사용자별)
    print("=== 모든 메모리 조회 ===")

    alice_all = memory.get_all(user_id="alice")
    print(f"Alice의 전체 메모리 ({len(alice_all['results'])}개):")
    for mem in alice_all['results']:
        print(f"  - {mem['memory']}")
    print()

    bob_all = memory.get_all(user_id="bob")
    print(f"Bob의 전체 메모리 ({len(bob_all['results'])}개):")
    for mem in bob_all['results']:
        print(f"  - {mem['memory']}")
    print()

    # 5. 메모리 업데이트 (새로운 선호도 추가)
    print("=== 메모리 업데이트 ===")

    memory.add(
        "사실 요즘은 일식도 좋아해",
        user_id="alice",
        metadata={"category": "food_preference"}
    )
    print("✅ Alice 메모리 업데이트: 사실 요즘은 일식도 좋아해\n")

    # 업데이트 후 검색
    alice_updated = memory.search(
        query="음식 선호도가 뭐야?",
        user_id="alice"
    )

    print("업데이트 후 Alice의 음식 선호도:")
    for mem in alice_updated['results']:
        print(f"  - {mem['memory']}")
    print()

    print("=== 완료 ===")
    print("✅ mem0 Cloud 기본 사용법을 모두 학습했습니다!")
    print("\n다음 단계: agent_memory.py에서 에이전트 메모리 통합 학습")


if __name__ == "__main__":
    main()
