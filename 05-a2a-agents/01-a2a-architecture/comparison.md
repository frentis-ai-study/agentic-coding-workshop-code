# A2A 구현 방법 비교

## 개요

A2A 멀티 에이전트 시스템을 구현하는 방법은 여러 가지가 있습니다. 이 문서에서는 주요 방법을 비교하고, 본 워크샵에서 python-a2a를 선택한 이유를 설명합니다.

## Google A2A 프로토콜 소개

Google이 2024년 발표한 **Agent-to-Agent (A2A) 프로토콜**은 AI 에이전트 간 통신을 위한 산업 표준입니다.

### 핵심 개념

#### 1. Agent Card (에이전트 명함)

각 에이전트는 `/.well-known/agent-card.json`에서 자신의 능력을 공개합니다.

```json
{
  "name": "Restaurant Recommender",
  "description": "Recommends restaurants based on user preferences",
  "version": "1.0.0",
  "endpoints": {
    "tasks": {
      "send": "/tasks/send"
    }
  }
}
```

#### 2. Task Send 엔드포인트

에이전트 간 작업 전달을 위한 표준 API (`POST /tasks/send`)입니다.

```python
# 요청
{
    "id": "task_123",
    "message": "배고파, 레스토랑 추천해줘",
    "user_id": "alice"
}

# 응답
{
    "task_id": "task_123",
    "response": "추천 레스토랑: La Trattoria, Pasta House"
}
```

### 최신 버전 (v0.3, 2025년)

- **gRPC 지원**: HTTP/2 기반 고성능 통신
- **스트리밍**: 실시간 응답 스트리밍
- **보안**: OAuth 2.0, mTLS 인증

## 구현 방법 비교

### 비교 표

| 방법 | 출시 시점 | A2A 버전 | 난이도 | A2A 순수성 | 주요 지원 기능 | 코드 길이 | 워크샵 적합성 | A2A 이해도 |
|------|----------|---------|--------|-----------|-------------|----------|-------------|-----------|
| **python-a2a + FastAPI** | 2025.04 | v0.3 | ⭐ 최쉬움 | ✅ 100% | Agent Card, Task Send, HTTP/REST | 짧음 (50줄) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| CrewAI Multi-Agent | 2023.11 | - | ⭐⭐ 쉬움 | ❌ 0% | Sequential/Hierarchical, 자동 태스크 분배 | 짧음 (50줄) | ⭐⭐⭐⭐ | ⭐ (A2A 아님) |
| CrewAI A2A Delegation | 2025.01 | v0.3 | ⭐⭐⭐ 어려움 | ✅ 100% | A2A 프로토콜, Crew 편의 기능, Agent Card | 중간 (100줄) | ⭐⭐ | ⭐⭐⭐ |
| LangGraph Swarm | 2023.01 | - | ⭐⭐ 중간 | ❌ 0% | State Graph, Conditional Edges, Checkpointing | 중간 (70줄) | ⭐⭐⭐ | ⭐ (Multi-Agent) |
| 직접 HTTP 구현 | - | 사용자 정의 | ⭐⭐ 쉬움 | ✅ 90% | FastAPI, httpx, 사용자 정의 | 중간 (80줄) | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### 1. python-a2a + FastAPI ⭐ 권장

**Google A2A 프로토콜을 준수하는 공식 Python 라이브러리**

#### 장점

- ✅ **진짜 A2A**: Google A2A 프로토콜 100% 준수
- ✅ **가장 쉬움**: HTTP POST만 이해하면 됨 (⭐ 난이도)
- ✅ **투명성**: 내부 동작 완전 이해 가능 (블랙박스 없음)
- ✅ **코드 간결성**: 약 50줄로 에이전트 서버 완성
- ✅ **실무 적용성**: 마이크로서비스 아키텍처와 동일
- ✅ **확장 용이**: 3번째 에이전트 = 새 FastAPI 서버 추가

#### 단점

- ❌ 2개 서버 실행 필요 (포트 관리)
- ❌ 프레임워크의 자동 편의 기능 없음

#### 예제 코드

```python
# recommender_agent.py (FastAPI 서버)
from fastapi import FastAPI

app = FastAPI()

@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    return {
        "name": "Restaurant Recommender",
        "description": "Recommends restaurants based on user preferences"
    }

@app.post("/tasks/send")
async def receive_task(task: dict):
    # mem0에서 선호도 검색 → 레스토랑 추천
    # A2A 호출: 예약 에이전트로 상세 정보 요청
    return {"response": "추천 결과"}
```

**워크샵에서 사용하는 방법입니다.**

---

### 2. CrewAI Multi-Agent

**프레임워크 기반 멀티 에이전트 (A2A 아님)**

#### 장점

- ✅ 쉬운 학습 곡선 (Agent/Task/Crew 개념)
- ✅ 자동 태스크 분배 및 실행

#### 단점

- ❌ **A2A 아님**: 에이전트가 직접 통신하지 않음 (Crew가 조율)
- ❌ 블랙박스: 내부 동작 숨겨짐
- ❌ HTTP 통신 학습 불가

#### 예제 코드

```python
from crewai import Agent, Task, Crew

recommender = Agent(role="추천", goal="레스토랑 추천")
booker = Agent(role="예약", goal="레스토랑 정보 제공")

task1 = Task(description="배고파", agent=recommender)
task2 = Task(description="상세 정보", agent=booker)

crew = Crew(agents=[recommender, booker], tasks=[task1, task2])
result = crew.kickoff()
```

**A2A를 학습하려면 적합하지 않습니다.**

---

### 3. CrewAI A2A Delegation

**CrewAI에서 Google A2A 프로토콜 지원 (v0.98+)**

#### 장점

- ✅ Google A2A 프로토콜 100% 준수
- ✅ CrewAI의 편의 기능 활용

#### 단점

- ❌ 복잡함: A2A 설정 + CrewAI 프레임워크 학습 필요
- ❌ 코드 길이: 약 100줄 (python-a2a의 2배)
- ❌ 초급자에게는 과도한 추상화

#### 예제 코드

```python
from crewai import Agent, Task, Crew
from crewai.a2a import A2AClient

# A2A 클라이언트 설정
a2a_client = A2AClient(url="http://localhost:8001")

recommender = Agent(
    role="추천",
    a2a_client=a2a_client  # A2A 위임 설정
)

# A2A 호출은 자동으로 처리
```

**중급자 이상에게 적합합니다.**

---

### 4. LangGraph Swarm

**LangGraph 기반 멀티 에이전트 (A2A 아님)**

#### 장점

- ✅ 세밀한 제어 (State Graph)
- ✅ Part 4에서 LangGraph 학습 경험 활용

#### 단점

- ❌ **A2A 아님**: 에이전트가 독립 서버로 실행되지 않음
- ❌ State Graph 개념 추가 학습 필요
- ❌ HTTP 통신 학습 불가

#### 예제 코드

```python
from langgraph.graph import StateGraph

def recommender_node(state):
    # 추천 로직
    return state

def booker_node(state):
    # 예약 로직
    return state

graph = StateGraph()
graph.add_node("recommender", recommender_node)
graph.add_node("booker", booker_node)
graph.add_edge("recommender", "booker")
```

**멀티 에이전트 학습에는 좋지만, A2A 학습에는 부적합합니다.**

---

### 5. 직접 HTTP 구현 (순수 Python)

**python-a2a 없이 FastAPI + httpx로 직접 구현**

#### 장점

- ✅ 의존성 최소화
- ✅ A2A 본질 완전 이해

#### 단점

- ❌ Google A2A 프로토콜 일부 미준수 (약 90%)
- ❌ 보일러플레이트 코드 증가

#### 예제 코드

```python
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.post("/tasks/send")
async def receive_task(task: dict):
    # 직접 HTTP 호출
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/tasks/send",
            json=task
        )
    return response.json()
```

**python-a2a가 이미 이 작업을 해주므로, 직접 구현할 필요 없습니다.**

---

## python-a2a가 CrewAI보다 쉬운 이유

### 1. 개념 단순성

| python-a2a | CrewAI |
|-----------|--------|
| HTTP POST만 알면 됨 | Agent/Task/Crew/Process 개념 학습 |
| FastAPI 기초만 필요 | CrewAI 프레임워크 전체 학습 |

### 2. 디버깅 용이성

| python-a2a | CrewAI |
|-----------|--------|
| 로그 출력으로 즉시 확인 | 내부 로직 숨겨짐 |
| 브라우저에서 Agent Card 확인 가능 | 프레임워크 코드 읽어야 함 |

### 3. 실무 적용성

| python-a2a | CrewAI |
|-----------|--------|
| 마이크로서비스 아키텍처 동일 | 프레임워크 종속적 |
| FastAPI 경험 직접 활용 | CrewAI만의 패턴 |

## 선택 가이드

### python-a2a를 선택하세요 (본 워크샵)

- ✅ A2A 개념을 처음 배우는 경우
- ✅ HTTP REST API 경험이 있는 경우
- ✅ 마이크로서비스 아키텍처를 이해하고 싶은 경우
- ✅ 블랙박스 없이 모든 동작을 이해하고 싶은 경우

### CrewAI를 선택하세요

- ✅ 빠른 프로토타입 개발
- ✅ 복잡한 멀티 에이전트 시스템 (5개 이상)
- ✅ 자동 태스크 분배 및 협업 패턴 활용

### LangGraph를 선택하세요

- ✅ 복잡한 상태 관리 필요
- ✅ 세밀한 흐름 제어 필요
- ✅ Part 4 LangGraph 경험 활용

## 다음 단계

개념을 이해했다면, [Part 5-2: mem0 메모리 시스템](../02-mem0-integration/)에서 에이전트 메모리 관리를 학습합니다.
