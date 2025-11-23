"""
CLI Client for Restaurant Agent System

추천 에이전트 서버(포트 8000)와 통신하는 CLI 클라이언트입니다.
추천 에이전트는 내부적으로 예약 에이전트(포트 8001)를 A2A 호출합니다.

Usage:
    python main.py --user-id alice --message "이탈리안 좋아해"
    python main.py --user-id alice --message "배고파"
"""

import argparse
import asyncio

import httpx
from config import settings


async def send_task(user_id: str, message: str, verbose: bool = False):
    """
    추천 에이전트에게 작업 전송

    Args:
        user_id: 사용자 ID
        message: 사용자 메시지
        verbose: 상세 로그 출력 여부
    """

    task_request = {
        "task_id": f"task_{user_id}_{hash(message) % 10000}",
        "message": message,
        "user_id": user_id
    }

    if verbose:
        print("\n=== 요청 ===")
        print(f"URL: {settings.RECOMMENDER_URL}/tasks/send")
        print(f"Payload: {task_request}\n")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.RECOMMENDER_URL}/tasks/send",
                json=task_request,
                timeout=30.0
            )

            if response.status_code == 200:
                data = response.json()

                if verbose:
                    print("=== 응답 ===")
                    print(f"Status: {response.status_code}")
                    print(f"Data: {data}\n")

                print(f"✅ {data['response']}")

            else:
                print(f"❌ 에러: HTTP {response.status_code}")
                print(f"   {response.text}")

        except httpx.ConnectError:
            print("❌ 추천 에이전트에 연결할 수 없습니다.")
            print(f"   포트 {settings.RECOMMENDER_PORT}에서 서버가 실행 중인지 확인하세요.")
            print("\n   서버 실행 명령:")
            print(f"   uvicorn agents.recommender_agent:app --port {settings.RECOMMENDER_PORT}")

        except httpx.TimeoutException:
            print("❌ 요청 시간 초과 (30초)")
            print("   Ollama가 실행 중인지 확인하세요.")


async def main():
    """CLI 엔트리 포인트"""

    parser = argparse.ArgumentParser(description="Restaurant Agent CLI Client")
    parser.add_argument(
        "--user-id",
        type=str,
        default="alice",
        help="사용자 ID (기본값: alice)"
    )
    parser.add_argument(
        "--message",
        type=str,
        help="사용자 메시지 (대화형 모드는 미지정)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="상세 로그 출력"
    )

    args = parser.parse_args()

    print("=== Restaurant Agent CLI ===\n")

    if args.message:
        # 단일 메시지 모드
        await send_task(args.user_id, args.message, args.verbose)
    else:
        # 대화형 모드
        print(f"사용자 ID: {args.user_id}")
        print("종료하려면 'exit' 또는 'quit'를 입력하세요.\n")

        while True:
            try:
                user_input = input(f"{args.user_id}> ")

                if not user_input.strip():
                    continue

                if user_input.lower() in ["exit", "quit"]:
                    print("종료합니다.")
                    break

                await send_task(args.user_id, user_input, args.verbose)
                print()

            except KeyboardInterrupt:
                print("\n종료합니다.")
                break


if __name__ == "__main__":
    asyncio.run(main())
