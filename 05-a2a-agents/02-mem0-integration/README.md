# Part 5-2: mem0 메모리 시스템 통합

## 학습 목표

AI 에이전트를 위한 전문 메모리 시스템 mem0를 학습하고, 에이전트에 장기 메모리 기능을 추가합니다.

- **mem0 소개**: AI 에이전트 메모리 시스템의 필요성과 mem0의 특징
- **클라우드 API 설정**: Mem0 Cloud Platform API 키 발급 및 설정 방법
- **기본 사용법**: 메모리 저장, 검색, 조회 API
- **에이전트 메모리**: 대화 중 선호도 자동 저장 및 개인화된 응답

## mem0란?

**mem0**는 AI 에이전트를 위한 전문 메모리 시스템입니다.

### 주요 특징

- **GitHub 41K+ Stars**: 2025년 가장 인기 있는 AI 메모리 라이브러리
- **월 186M API 호출**: 실제 프로덕션에서 검증된 시스템
- **프레임워크 독립적**: OpenAI, LangChain, LangGraph, CrewAI 모두 지원
- **클라우드 플랫폼**: API 키 하나로 즉시 사용 가능 (설정 불필요)
- **간편성**: 3줄 코드로 메모리 저장/검색
- **무료 티어**: 1000 메모리/월 무료 제공

### mem0 vs LangChain Memory

| 측면 | mem0 | LangChain Memory |
|------|------|-----------------|
| **전문성** | AI 메모리 전용 | LangChain 일부 기능 |
| **백엔드** | SQLite, PostgreSQL, Qdrant | 제한적 |
| **검색 품질** | 벡터 유사도 검색 | 키워드 기반 |
| **프레임워크** | 독립적 | LangChain 종속 |
| **성숙도** | 2025년 최신 | 2023년 레거시 |

## 학습 시간

약 10분

## 실습 예제

1. [**Quickstart**](quickstart.py) - mem0 기본 사용법 (저장, 검색, 조회)
2. [**에이전트 메모리**](agent_memory.py) - 대화 중 선호도 자동 저장 및 개인화

## 설치 방법

```bash
# mem0 설치
uv add mem0ai

# 또는 pip
pip install mem0ai
```

## Mem0 Cloud API 설정

### 1. API 키 발급 (1-2분 소요)

```bash
# 1. 회원가입 및 API 키 발급
# 🔗 https://app.mem0.ai/

# 2. 환경 변수 설정
export MEM0_API_KEY="m0-your-api-key-here"
```

### 2. 코드에서 사용

```python
from mem0 import MemoryClient

# Mem0 Cloud 클라이언트 초기화 (환경 변수 자동 인식)
memory = MemoryClient()

# 메모리 저장 및 검색
memory.add("이탈리안 음식을 좋아해", user_id="alice")
results = memory.search("음식 선호도", user_id="alice")
```

## Mem0 Cloud 장점

- ⚡ **즉시 사용 가능**: API 키 하나로 3분 내 시작
- ⚡ **빠른 성능**: 벡터 검색 <0.3초 (클라우드 최적화)
- 🔧 **간단한 설정**: 환경 변수 1개만 필요
- 🌐 **멀티유저 지원**: 동시 사용자 무제한
- 💰 **무료 티어**: 1000 메모리/월 무료
- 📊 **대시보드**: [https://app.mem0.ai/](https://app.mem0.ai/)에서 메모리 관리

**워크샵에서는 Mem0 Cloud Platform을 사용합니다.**

## 다음 단계

mem0를 학습한 후, [Part 5-3: 레스토랑 추천 시스템](../03-restaurant-agent/)에서 A2A 에이전트와 mem0를 통합합니다.
