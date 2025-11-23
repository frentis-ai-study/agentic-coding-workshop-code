"""Recommender Agent Server

사용자 선호도 기반 레스토랑 추천 에이전트 서버
"""

import json
import logging
from datetime import datetime

import httpx
from config import settings
from fastapi import FastAPI
from memory.mem0_client import Mem0Client
from openai import OpenAI
from pydantic import BaseModel
from tools.restaurant_search import RestaurantSearchTool

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/recommender_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Restaurant Recommender Agent")

# 도구 및 메모리 초기화
mem0_client = Mem0Client()
search_tool = RestaurantSearchTool()

# LLM 클라이언트
llm = OpenAI(base_url=settings.base_url, api_key=settings.api_key)

# Function Calling Tools 정의
tools = [
    {
        "type": "function",
        "function": {
            "name": "save_preference",
            "description": "사용자의 음식 선호도를 저장합니다",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "선호도 내용 (예: 이탈리안 좋아함, 매운 음식 싫어함)"
                    }
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_preference",
            "description": "저장된 사용자 선호도를 조회합니다",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_restaurant",
            "description": "사용자 선호도를 기반으로 레스토랑을 추천합니다",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_booking_info",
            "description": "레스토랑 예약 정보 및 상세 정보를 조회합니다",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "예약 관련 질문 (예: La Trattoria 영업시간, 예약하고 싶어)"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


class TaskRequest(BaseModel):
    """작업 요청 모델"""
    task_id: str
    message: str
    user_id: str


class A2ACall(BaseModel):
    """A2A 호출 정보"""
    target_agent: str
    target_url: str
    request: dict
    response: dict
    timestamp: str


class TaskResponse(BaseModel):
    """작업 응답 모델"""
    task_id: str
    response: str
    a2a_calls: list[A2ACall] = []


@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    """Agent Card 반환 (Google A2A 프로토콜)"""
    return {
        "name": "Restaurant Recommender",
        "description": "Recommends restaurants based on user preferences using mem0 memory",
        "version": "1.0.0",
        "endpoints": {
            "tasks": {
                "send": "/tasks/send"
            }
        }
    }


@app.get("/memories/{user_id}")
async def get_user_memories(user_id: str):
    """사용자의 모든 메모리 조회 (디버그/UI용)"""
    try:
        memories = mem0_client.get_all_preferences(user_id)
        return {
            "user_id": user_id,
            "count": len(memories),
            "memories": memories
        }
    except Exception as e:
        logger.error(f"메모리 조회 실패: {e}")
        return {
            "user_id": user_id,
            "count": 0,
            "memories": [],
            "error": str(e)
        }


@app.get("/memories/{user_id}/details")
async def get_user_memories_with_ids(user_id: str):
    """사용자의 모든 메모리를 ID와 함께 조회 (관리/삭제용)"""
    try:
        memories = mem0_client.get_all_memories_with_ids(user_id)
        return {
            "user_id": user_id,
            "count": len(memories),
            "memories": memories
        }
    except Exception as e:
        logger.error(f"메모리 상세 조회 실패: {e}")
        return {
            "user_id": user_id,
            "count": 0,
            "memories": [],
            "error": str(e)
        }


@app.delete("/memories/{user_id}")
async def delete_all_user_memories(user_id: str):
    """사용자의 모든 메모리 삭제 (초기화)"""
    try:
        result = mem0_client.delete_all_preferences(user_id)
        logger.info(f"메모리 전체 삭제 완료 - user_id: {user_id}")
        return {
            "user_id": user_id,
            "success": True,
            "message": "모든 메모리가 삭제되었습니다.",
            "result": result
        }
    except Exception as e:
        logger.error(f"메모리 전체 삭제 실패: {e}")
        return {
            "user_id": user_id,
            "success": False,
            "error": str(e)
        }


@app.delete("/memories/{user_id}/{memory_id}")
async def delete_specific_memory(user_id: str, memory_id: str):
    """특정 메모리 삭제"""
    try:
        result = mem0_client.delete_memory(memory_id)
        logger.info(f"메모리 삭제 완료 - user_id: {user_id}, memory_id: {memory_id}")
        return {
            "user_id": user_id,
            "memory_id": memory_id,
            "success": True,
            "message": "메모리가 삭제되었습니다.",
            "result": result
        }
    except Exception as e:
        logger.error(f"메모리 삭제 실패: {e}")
        return {
            "user_id": user_id,
            "memory_id": memory_id,
            "success": False,
            "error": str(e)
        }


@app.post("/tasks/send", response_model=TaskResponse)
async def receive_task(task: TaskRequest):
    """작업 수신 및 처리 (Function Calling 방식)

    LLM이 자동으로 적절한 함수를 선택하여 실행합니다.
    """
    a2a_calls = []

    # LLM Function Calling
    response_llm = llm.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": task.message}],
        tools=tools,
        temperature=0
    )

    # tool_calls 파싱
    tool_calls = response_llm.choices[0].message.tool_calls

    if not tool_calls:
        # tool이 선택되지 않은 경우
        return TaskResponse(
            task_id=task.task_id,
            response="죄송합니다. 요청을 이해하지 못했습니다.",
            a2a_calls=[]
        )

    # 첫 번째 tool call 처리
    tool_call = tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    logger.info(f"Function called: {function_name} with args: {arguments}")

    # 함수 라우팅
    if function_name == "save_preference":
        logger.info(f"선호도 저장 시작 - user_id: {task.user_id}, content: {arguments['content']}")
        result = mem0_client.save_preference(task.user_id, arguments["content"])
        logger.info(f"저장 결과: {result}")

        # 저장 직후 확인
        check = mem0_client.get_all_preferences(task.user_id)
        logger.info(f"저장 직후 조회: {len(check)}개 - {check}")

        response = "선호도가 저장되었습니다."

    elif function_name == "query_preference":
        response = handle_query_preference(task.user_id)

    elif function_name == "recommend_restaurant":
        response, calls = await handle_recommendation(task.user_id, task.message)
        a2a_calls.extend(calls)

    elif function_name == "get_booking_info":
        response, calls = await handle_booking(arguments["query"])
        a2a_calls.extend(calls)

    else:
        response = "지원하지 않는 기능입니다."

    return TaskResponse(task_id=task.task_id, response=response, a2a_calls=a2a_calls)


def handle_query_preference(user_id: str) -> str:
    """선호도 조회 핸들러 (신규 기능 - Mem0 기반 intelligent 응답)"""
    try:
        preferences = mem0_client.get_all_preferences(user_id)

        if not preferences:
            return "아직 저장된 선호도가 없습니다. 좋아하는 음식을 알려주세요."

        # LLM이 메모리를 활용해 자연스러운 답변 생성
        memory_context = "\n".join(f"- {pref}" for pref in preferences)

        prompt = f"""사용자의 저장된 선호도를 바탕으로 자연스럽게 대답해주세요.

저장된 선호도:
{memory_context}

**중요: 반드시 한국어로 답변하세요.**
자연스럽고 친근하게 답변하되, 모든 선호도를 언급해주세요."""

        response = llm.chat.completions.create(
            model=settings.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"선호도 조회 실패: {e}")
        return "선호도를 조회하는 중 오류가 발생했습니다."


async def handle_recommendation(user_id: str, _message: str) -> tuple[str, list[A2ACall]]:
    """레스토랑 추천 처리."""
    a2a_calls = []

    # 1. mem0에서 선호도 검색
    preferences = mem0_client.search_preferences(user_id, "음식 선호도")

    if not preferences:
        return "선호도가 저장되지 않았습니다. 먼저 좋아하는 음식을 알려주세요.", a2a_calls

    # 2. 선호도에서 카테고리 추출
    category = await extract_category(preferences)

    # 3. 카테고리별 레스토랑 검색
    restaurants = search_tool.search_by_category(category)

    if not restaurants:
        return f"죄송합니다. {category} 레스토랑을 찾을 수 없습니다.", a2a_calls

    # 상위 3개만 추천
    top_3 = restaurants[:3]

    # 4. A2A 호출: 첫 번째 레스토랑 상세 정보
    first_restaurant = top_3[0]["name"]
    details, call_info = await get_restaurant_details(first_restaurant)
    if call_info:
        a2a_calls.append(call_info)

    # 5. 최종 응답 조합
    recommendation = f"선호도({category})를 기반으로 추천합니다:\n"
    for i, r in enumerate(top_3, 1):
        recommendation += f"{i}. {r['name']}\n"

    recommendation += f"\n{first_restaurant} 상세 정보:\n{details}"

    return recommendation, a2a_calls


async def extract_category(preferences: list[str]) -> str:
    """선호도에서 음식 카테고리를 추출합니다.

    LLM이 선호도 텍스트에서 적절한 카테고리를 찾아냅니다.
    """
    prefs_text = ", ".join(preferences)

    prompt = f"""다음 선호도에서 음식 카테고리를 찾으세요.

선호도: {prefs_text}

카테고리: 이탈리안, 한식, 일식, 중식, 양식

위 중 가장 적합한 하나만 응답하세요."""

    response = llm.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


async def get_restaurant_details(restaurant_name: str) -> tuple[str, A2ACall | None]:
    """A2A 호출: 예약 에이전트에게 레스토랑 상세 정보 요청."""
    request_data = {
        "task_id": "booking_task_001",
        "message": f"{restaurant_name} 상세 정보",
        "user_id": "system"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.BOOKING_URL}/tasks/send",
                json=request_data,
                timeout=10.0
            )

            if response.status_code == 200:
                response_json = response.json()
                call_info = A2ACall(
                    target_agent="Booking Agent",
                    target_url=f"{settings.BOOKING_URL}/tasks/send",
                    request=request_data,
                    response=response_json,
                    timestamp=datetime.now().isoformat()
                )
                return response_json["response"], call_info
            else:
                return "상세 정보를 가져올 수 없습니다.", None

        except httpx.RequestError as e:
            return f"예약 에이전트에 연결할 수 없습니다: {str(e)}", None


async def handle_booking(message: str) -> tuple[str, list[A2ACall]]:
    """A2A 호출: 예약 에이전트로 직접 전달."""
    a2a_calls = []
    request_data = {
        "task_id": "booking_task_002",
        "message": message,
        "user_id": "system"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.BOOKING_URL}/tasks/send",
                json=request_data,
                timeout=10.0
            )

            if response.status_code == 200:
                response_json = response.json()
                call_info = A2ACall(
                    target_agent="Booking Agent",
                    target_url=f"{settings.BOOKING_URL}/tasks/send",
                    request=request_data,
                    response=response_json,
                    timestamp=datetime.now().isoformat()
                )
                a2a_calls.append(call_info)
                return response_json["response"], a2a_calls
            else:
                return "예약 정보를 가져올 수 없습니다.", a2a_calls

        except httpx.RequestError as e:
            return f"예약 에이전트에 연결할 수 없습니다: {str(e)}", a2a_calls


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.RECOMMENDER_PORT)
