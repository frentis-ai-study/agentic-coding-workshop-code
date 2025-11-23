# Agentic Coding Workshop - Source Code

Agentic AI와 AI-DLC(Development Lifecycle)를 활용한 소프트웨어 개발 워크샵 소스코드입니다.

## 요구사항

- Python 3.12 이상
- uv (Python 패키지 매니저)
- Ollama (로컬 LLM 실행)

## 설치

```bash
# 의존성 설치
uv sync
```

## 프로젝트 구조

```
.
├── 03-mcp-tools/              # MCP 서버 구현 예제
│   ├── 01-basic-server/       # 기본 MCP 서버
│   ├── 02-tools/              # 툴 구현 (계산기, 파일시스템, 날씨 등)
│   ├── 03-transport-methods/  # 전송 방식 (stdio, HTTP)
│   └── 04-resources/          # 리소스 제공
│
├── 04-testing-deployment/     # 테스팅 및 배포
│   ├── 01-ai-dlc-testing/    # AI-DLC 테스팅 전략
│   ├── 02-mcp-chat-client/   # MCP 채팅 클라이언트 (Streamlit)
│   └── 03-docker-deployment/ # Docker 배포
│
└── 05-a2a-agents/            # Agent-to-Agent 통신
    ├── 02-mem0-integration/  # Mem0 메모리 통합
    └── 03-restaurant-agent/  # 레스토랑 예약 에이전트

```

## 실행 예제

### MCP 서버 실행

```bash
# 기본 서버
cd 03-mcp-tools/01-basic-server
uv run python main.py

# 툴 서버
cd 03-mcp-tools/02-tools
uv run python main.py
```

### 테스트 실행

```bash
# 전체 테스트
uv run pytest

# 특정 모듈 테스트
uv run pytest 03-mcp-tools/02-tools/tests/
```

### 채팅 클라이언트 실행

```bash
cd 04-testing-deployment/02-mcp-chat-client
uv run streamlit run app.py
```

### 레스토랑 에이전트 실행

```bash
cd 05-a2a-agents/03-restaurant-agent

# 서버 시작
./run_servers.sh

# UI 실행 (다른 터미널에서)
uv run streamlit run chat_ui.py

# 서버 종료
./stop_servers.sh
```

## Docker 배포

```bash
cd 04-testing-deployment/03-docker-deployment

# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 종료
docker-compose down
```

## 환경 변수

각 프로젝트에 필요한 환경 변수는 `.env` 파일을 참고하세요.

### Ollama 표준 모델

- 모델: `qwen3-vl:4b`
- 다운로드: `ollama pull qwen3-vl:4b`

### Mem0 Cloud (선택사항)

레스토랑 에이전트에서 Mem0 Cloud를 사용하려면:

```bash
export MEM0_API_KEY="your-api-key"
```

## 라이선스

MIT
