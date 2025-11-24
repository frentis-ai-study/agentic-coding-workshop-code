# 고급 가이드: A2A 에이전트 확장

이 가이드는 레스토랑 추천 시스템을 확장하고, 실제 프로덕션 환경에 적용하는 방법을 다룹니다.

## 목차

1. [3번째 에이전트 추가](#1-3번째-에이전트-추가)
2. [실제 API 연동](#2-실제-api-연동)
3. [CrewAI A2A Delegation 비교](#3-crewai-a2a-delegation-비교)
4. [프로덕션 배포](#4-프로덕션-배포)

---

## 1. 3번째 에이전트 추가

리뷰 분석 에이전트를 추가하여 3개 에이전트 시스템으로 확장합니다.

### 1.1 리뷰 에이전트 구현

**파일**: `agents/review_agent.py`

```python
"""
Review Agent Server

레스토랑 리뷰를 분석하는 에이전트 서버입니다.

포트: 8002
"""

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

from config import settings
from tools.restaurant_search import RestaurantSearchTool

app = FastAPI(title="Restaurant Review Analyzer")

search_tool = RestaurantSearchTool()

llm = OpenAI(
    base_url=f"{settings.OLLAMA_BASE_URL}/v1",
    api_key="ollama"
)


class TaskRequest(BaseModel):
    task_id: str
    message: str
    user_id: str


class TaskResponse(BaseModel):
    task_id: str
    response: str


@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    return {
        "name": "Restaurant Review Analyzer",
        "description": "Analyzes restaurant reviews and ratings",
        "version": "1.0.0",
        "endpoints": {
            "tasks": {
                "send": "/tasks/send"
            }
        }
    }


@app.post("/tasks/send", response_model=TaskResponse)
async def receive_task(task: TaskRequest):
    """리뷰 분석 작업 처리"""

    # 레스토랑 이름 추출
    restaurant_name = extract_restaurant_name(task.message)

    # 리뷰 분석 (실제로는 Google Places API 등에서 가져옴)
    # 여기서는 간단한 예시
    reviews = get_mock_reviews(restaurant_name)
    analysis = analyze_reviews(reviews)

    return TaskResponse(
        task_id=task.task_id,
        response=f"{restaurant_name} 리뷰 분석:\n{analysis}"
    )


def extract_restaurant_name(message: str) -> str:
    """메시지에서 레스토랑 이름 추출"""
    all_restaurants = search_tool.get_all()
    for r in all_restaurants:
        if r["name"] in message:
            return r["name"]
    return "La Trattoria"  # 기본값


def get_mock_reviews(restaurant_name: str) -> list[str]:
    """Mock 리뷰 데이터 (실제로는 API에서 가져옴)"""
    return [
        "음식이 정말 맛있었어요! 파스타가 일품입니다.",
        "분위기가 좋고 서비스도 친절했어요.",
        "가격은 조금 비싼 편이지만 만족스러웠습니다."
    ]


def analyze_reviews(reviews: list[str]) -> str:
    """리뷰 분석 (LLM 사용)"""
    reviews_text = "\n".join(f"- {r}" for r in reviews)

    prompt = f"""다음 레스토랑 리뷰를 분석하여 요약하세요:

{reviews_text}

긍정/부정 비율, 주요 키워드, 전반적인 평가를 포함하세요.
"""

    response = llm.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": "당신은 리뷰 분석 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
```

### 1.2 설정 업데이트

**파일**: `config.py`

```python
class Settings:
    # ... 기존 설정 ...

    # 리뷰 에이전트 포트 추가
    REVIEW_PORT: int = int(os.getenv("REVIEW_PORT", "8002"))
    REVIEW_URL: str = f"http://localhost:{REVIEW_PORT}"
```

### 1.3 추천 에이전트에서 리뷰 에이전트 호출

**파일**: `agents/recommender_agent.py` (수정)

```python
async def handle_recommendation(user_id: str, _message: str) -> str:
    # ... 기존 코드 ...

    # 4. A2A 호출: 첫 번째 레스토랑 상세 정보
    first_restaurant = top_3[0]["name"]
    details = await get_restaurant_details(first_restaurant)

    # 5. A2A 호출: 리뷰 분석 (새로 추가!)
    reviews = await get_restaurant_reviews(first_restaurant)

    # 6. 최종 응답 조합
    recommendation = f"선호도({category})를 기반으로 추천합니다:\n"
    for i, r in enumerate(top_3, 1):
        recommendation += f"{i}. {r['name']}\n"

    recommendation += f"\n{first_restaurant} 상세 정보:\n{details}"
    recommendation += f"\n\n{first_restaurant} 리뷰:\n{reviews}"

    return recommendation


async def get_restaurant_reviews(restaurant_name: str) -> str:
    """A2A 호출: 리뷰 에이전트에게 리뷰 분석 요청"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.REVIEW_URL}/tasks/send",
                json={
                    "task_id": "review_task_001",
                    "message": f"{restaurant_name} 리뷰 분석",
                    "user_id": "system"
                },
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                return data["response"]
            else:
                return "리뷰 분석을 가져올 수 없습니다."

        except httpx.RequestError:
            return "리뷰 에이전트에 연결할 수 없습니다. (포트 8002 확인)"
```

### 1.4 실행

```bash
# 터미널 1: 추천 서버
uv run python agents/recommender_agent.py

# 터미널 2: 예약 서버
uv run python agents/booking_agent.py

# 터미널 3: 리뷰 서버 (새로 추가!)
uv run python agents/review_agent.py

# 터미널 4: 테스트
python main.py --user-id alice --message "배고파"
```

---

## 2. 실제 API 연동

### 2.1 Google Places API 연동

**설치**:
```bash
pip install googlemaps
```

**구현**: `tools/google_places.py`

```python
import googlemaps
import os

class GooglePlacesTool:
    """Google Places API 도구"""

    def __init__(self):
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        self.gmaps = googlemaps.Client(key=api_key)

    def search_restaurants(self, location: str, category: str) -> list[dict]:
        """레스토랑 검색"""
        query = f"{category} restaurant in {location}"

        places = self.gmaps.places(query=query, language="ko")

        results = []
        for place in places.get("results", [])[:5]:
            results.append({
                "name": place["name"],
                "address": place.get("vicinity", ""),
                "rating": place.get("rating", 0),
                "place_id": place["place_id"]
            })

        return results

    def get_place_details(self, place_id: str) -> dict:
        """레스토랑 상세 정보"""
        details = self.gmaps.place(place_id=place_id, language="ko")

        result = details.get("result", {})

        return {
            "name": result.get("name", ""),
            "phone": result.get("formatted_phone_number", ""),
            "address": result.get("formatted_address", ""),
            "hours": result.get("opening_hours", {}).get("weekday_text", []),
            "rating": result.get("rating", 0),
            "reviews": [r["text"] for r in result.get("reviews", [])[:3]]
        }
```

**사용**:
```python
# agents/recommender_agent.py
from tools.google_places import GooglePlacesTool

google_places = GooglePlacesTool()

async def handle_recommendation(user_id: str, _message: str) -> str:
    # ... mem0에서 선호도 검색 ...

    # Google Places API로 실제 레스토랑 검색
    restaurants = google_places.search_restaurants(
        location="서울",
        category=category
    )

    # ...
```

### 2.2 Naver 지역 검색 API

**구현**: `tools/naver_search.py`

```python
import httpx
import os

class NaverSearchTool:
    """Naver 지역 검색 API 도구"""

    def __init__(self):
        self.client_id = os.getenv("NAVER_CLIENT_ID")
        self.client_secret = os.getenv("NAVER_CLIENT_SECRET")
        self.base_url = "https://openapi.naver.com/v1/search/local.json"

    async def search_restaurants(self, query: str) -> list[dict]:
        """레스토랑 검색"""
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

        params = {
            "query": query,
            "display": 5,
            "start": 1,
            "sort": "random"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url,
                headers=headers,
                params=params
            )

            data = response.json()

            results = []
            for item in data.get("items", []):
                results.append({
                    "name": item["title"].replace("<b>", "").replace("</b>", ""),
                    "category": item.get("category", ""),
                    "phone": item.get("telephone", ""),
                    "address": item["address"],
                    "link": item["link"]
                })

            return results
```

---

## 3. CrewAI A2A Delegation 비교

### 3.1 CrewAI A2A 구현

**설치**:
```bash
pip install crewai>=0.98.0
```

**구현**: `examples/crewai_a2a.py`

```python
from crewai import Agent, Task, Crew
from crewai.a2a import A2AClient

# A2A 클라이언트 설정 (예약 에이전트 URL)
booking_a2a = A2AClient(url="http://localhost:8001")

# 추천 에이전트 (CrewAI Agent)
recommender = Agent(
    role="레스토랑 추천",
    goal="사용자 선호도 기반 레스토랑 추천",
    backstory="mem0 메모리를 활용한 개인화 추천 전문가",
    a2a_client=booking_a2a  # A2A 위임 설정
)

# 예약 에이전트는 FastAPI 서버로 독립 실행
# CrewAI 에이전트가 A2A 프로토콜로 호출

# 태스크
task = Task(
    description="배고파, 레스토랑 추천해줘",
    agent=recommender,
    expected_output="추천 레스토랑 목록 및 상세 정보"
)

# Crew 실행
crew = Crew(agents=[recommender], tasks=[task])
result = crew.kickoff()
```

### 3.2 python-a2a vs CrewAI 비교

| 측면 | python-a2a + FastAPI | CrewAI A2A Delegation |
|------|---------------------|----------------------|
| **난이도** | ⭐ 최쉬움 (HTTP만) | ⭐⭐⭐ 어려움 (프레임워크 학습) |
| **코드 길이** | 짧음 (50줄) | 중간 (100줄) |
| **투명성** | ⭐⭐⭐⭐⭐ 완전 투명 | ⭐⭐ 일부 숨겨짐 |
| **A2A 순수성** | ✅ 100% | ✅ 100% |
| **프로덕션** | 직접 구현 필요 | 프레임워크 지원 |
| **학습 곡선** | 1시간 | 3시간+ |

**결론**: 초급 학습자는 python-a2a, 프로덕션 환경에서는 CrewAI 권장

---

## 4. 프로덕션 배포

### 4.1 Docker Compose

**파일**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  recommender:
    build: .
    command: uvicorn agents.recommender_agent:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - BOOKING_URL=http://booking:8001
      - MEM0_API_KEY=${MEM0_API_KEY}  # 클라우드 API 키
    depends_on:
      - ollama

  booking:
    build: .
    command: uvicorn agents.booking_agent:app --host 0.0.0.0 --port 8001
    ports:
      - "8001:8001"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama

  review:
    build: .
    command: uvicorn agents.review_agent:app --host 0.0.0.0 --port 8002
    ports:
      - "8002:8002"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  ollama_data:
```

**Dockerfile**:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install uv && uv sync

COPY . .

CMD ["uvicorn", "agents.recommender_agent:app", "--host", "0.0.0.0", "--port", "8000"]
```

**실행**:
```bash
docker-compose up -d
```

### 4.2 프로덕션 mem0 설정

프로덕션 환경에서는 **Mem0 Cloud Platform**을 사용하는 것을 권장합니다:

**장점**:
- ⚡ 자동 확장 및 로드 밸런싱
- 🔒 보안 및 백업 자동화
- 📊 사용량 모니터링 및 분석
- 💰 예측 가능한 비용 (사용량 기반)

**설정**:
```bash
# 환경 변수만 설정
export MEM0_API_KEY="m0-production-key"
```

**대시보드**: [https://app.mem0.ai/](https://app.mem0.ai/)에서 메모리 관리 및 모니터링

> **참고**: 특별한 요구사항이 있는 경우 Self-hosted mem0 (PostgreSQL + pgvector)를 사용할 수 있지만, 클라우드 플랫폼 사용을 권장합니다.

### 4.3 Kubernetes 배포

**파일**: `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recommender-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: recommender
  template:
    metadata:
      labels:
        app: recommender
    spec:
      containers:
      - name: recommender
        image: your-registry/recommender-agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: OLLAMA_BASE_URL
          value: "http://ollama-service:11434"
        - name: BOOKING_URL
          value: "http://booking-service:8001"
```

### 4.4 모니터링 및 로깅

**Prometheus 메트릭**:
```python
from prometheus_client import Counter, Histogram

# agents/recommender_agent.py
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Prometheus 메트릭 자동 수집
Instrumentator().instrument(app).expose(app)

# 커스텀 메트릭
a2a_calls = Counter('a2a_calls_total', 'Total A2A calls', ['target_agent'])
recommendation_latency = Histogram('recommendation_latency_seconds', 'Recommendation latency')

@app.post("/tasks/send")
async def receive_task(task: TaskRequest):
    with recommendation_latency.time():
        # ... 기존 코드 ...

        # A2A 호출 시
        a2a_calls.labels(target_agent='booking').inc()
```

### 4.5 보안

**API Key 인증**:
```python
# agents/recommender_agent.py
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.post("/tasks/send", dependencies=[Depends(verify_api_key)])
async def receive_task(task: TaskRequest):
    # ...
```

**HTTPS (Let's Encrypt)**:
```bash
# Nginx Reverse Proxy
sudo certbot --nginx -d your-domain.com
```

---

## 다음 단계

- **멀티 에이전트 오케스트레이션**: LangGraph Supervisor 패턴 학습
- **실시간 스트리밍**: Server-Sent Events (SSE) 적용
- **에이전트 메모리 공유**: Redis Pub/Sub 활용
- **비동기 작업 큐**: Celery + RabbitMQ 통합
