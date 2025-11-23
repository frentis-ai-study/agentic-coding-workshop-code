"""Booking Agent Server

레스토랑 상세 정보 제공 에이전트 서버
"""

from config import settings
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from tools.restaurant_search import RestaurantSearchTool

app = FastAPI(title="Restaurant Booking Agent")

# 도구 초기화
search_tool = RestaurantSearchTool()

# LLM 클라이언트
llm = OpenAI(base_url=settings.base_url, api_key=settings.api_key)


class TaskRequest(BaseModel):
    """작업 요청 모델"""
    task_id: str
    message: str
    user_id: str


class TaskResponse(BaseModel):
    """작업 응답 모델"""
    task_id: str
    response: str


@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    """Agent Card 반환 (Google A2A 프로토콜)"""
    return {
        "name": "Restaurant Booking Assistant",
        "description": "Provides restaurant booking information (hours, phone, address)",
        "version": "1.0.0",
        "endpoints": {
            "tasks": {
                "send": "/tasks/send"
            }
        }
    }


@app.post("/tasks/send", response_model=TaskResponse)
async def receive_task(task: TaskRequest):
    """작업 수신 및 처리

    메시지에서 레스토랑 이름을 추출하고 상세 정보를 반환합니다.
    """
    # 레스토랑 이름 추출
    restaurant_name = await extract_restaurant_name(task.message)

    if not restaurant_name:
        return TaskResponse(
            task_id=task.task_id,
            response="레스토랑 이름을 찾을 수 없습니다."
        )

    # 레스토랑 정보 검색
    info = search_tool.search_by_name(restaurant_name)

    if not info:
        return TaskResponse(
            task_id=task.task_id,
            response=f"'{restaurant_name}' 레스토랑을 찾을 수 없습니다."
        )

    # 상세 정보 포맷팅
    details = format_restaurant_details(info)

    return TaskResponse(task_id=task.task_id, response=details)


async def extract_restaurant_name(message: str) -> str:
    """메시지에서 레스토랑 이름 추출."""
    # 간단한 패턴 매칭 시도
    all_restaurants = search_tool.get_all()
    restaurant_names = [r["name"] for r in all_restaurants]

    for name in restaurant_names:
        if name in message:
            return name

    # 패턴 매칭 실패 시 LLM 사용
    prompt = f"""메시지에서 레스토랑 이름을 추출하세요.

메시지: {message}

가능한 레스토랑: {', '.join(restaurant_names)}

레스토랑 이름만 응답하세요. 목록에 없으면 "없음"이라고 응답하세요."""

    response = llm.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    extracted = response.choices[0].message.content.strip()

    if extracted == "없음" or extracted not in restaurant_names:
        return ""

    return extracted


def format_restaurant_details(info: dict) -> str:
    """레스토랑 정보 포맷팅."""
    return f"""- 영업시간: {info['hours']}
- 전화번호: {info['phone']}
- 주소: {info['address']}"""


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.BOOKING_PORT)
