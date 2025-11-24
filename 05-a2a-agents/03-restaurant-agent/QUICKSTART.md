# 레스토랑 추천 시스템 - 빠른 시작 가이드

이 가이드는 Part 5 레스토랑 추천 시스템을 처음부터 실행하는 단계별 안내입니다.

**예상 소요 시간**: 설정 3분 + 실습 47분 = 총 50분

## 사전 준비

### 1. Mem0 Cloud API 키 발급 (필수) ⭐

```bash
# 1. API 키 발급 (1-2분 소요)
# 🔗 https://app.mem0.ai/ 에서 회원가입 및 API 키 생성
# 💡 무료 티어: 1000 메모리/월

# 2. 환경 변수 설정
cd 05-a2a-agents/03-restaurant-agent
cp .env.example .env

# 3. .env 파일 편집 (MEM0_API_KEY=m0-... 입력)
```

### 2. LLM 제공자 선택 (Intent Detection용)

**옵션 A: Ollama (로컬, 무료)** ⭐ 권장

```bash
# 1. Ollama 설치
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: https://ollama.ai/download

# 2. 모델 다운로드 (4GB 디스크 공간 필요)
ollama pull qwen3-vl:4b

# 3. Ollama 서버 실행 (백그라운드)
ollama serve
```

**옵션 B: OpenAI API (클라우드, 유료)**

```bash
# 1. OpenAI API 키 발급 (https://platform.openai.com/api-keys)

# 2. .env 파일 편집:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...
```

### 3. 의존성 설치

```bash
# 루트에서 한 번만 실행
cd /path/to/fastmcp-example
uv sync
```

## 실행 단계

### Step 1: 터미널 1 - 추천 에이전트 서버 실행

```bash
# 디렉토리 이동
cd 05-a2a-agents/03-restaurant-agent

# 추천 에이전트 서버 실행 (포트 8000)
uv run python agents/recommender_agent.py
```

**예상 출력**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **확인**: 브라우저에서 http://localhost:8000/.well-known/agent-card.json 접속 시 Agent Card 표시

### Step 2: 터미널 2 - 예약 에이전트 서버 실행

```bash
# 새 터미널 열기
cd 05-a2a-agents/03-restaurant-agent

# 예약 에이전트 서버 실행 (포트 8001)
uv run python agents/booking_agent.py
```

**예상 출력**:
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [12347] using StatReload
INFO:     Started server process [12348]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **확인**: http://localhost:8001/.well-known/agent-card.json 접속 시 Agent Card 표시

### Step 3: 터미널 3 - CLI 클라이언트 테스트

```bash
# 새 터미널 열기
cd 05-a2a-agents/03-restaurant-agent
```

#### 시나리오 1: 선호도 저장

```bash
python main.py --user-id alice --message "이탈리안 음식을 좋아해"
```

**예상 출력**:
```
✅ 선호도가 저장되었습니다.
```

#### 시나리오 2: 레스토랑 추천 (A2A Chaining!)

```bash
python main.py --user-id alice --message "배고파, 레스토랑 추천해줘"
```

**예상 출력** (Ollama 사용 시):
```
✅ 선호도(이탈리안)를 기반으로 추천합니다:
1. La Trattoria
2. Pasta House

La Trattoria 상세 정보:
- 영업시간: 11:00-22:00
- 전화번호: 02-1234-5678
- 주소: 서울 강남구 논현동 123
```

**A2A 통신 흐름**:
1. CLI → 추천 서버 (포트 8000)
2. 추천 서버 → mem0 (선호도 검색: "이탈리안 좋아함")
3. 추천 서버 → RestaurantSearchTool (카테고리 "이탈리안" 필터링)
4. **추천 서버 → 예약 서버 (포트 8001, A2A 호출!)** ⭐
5. 예약 서버 → RestaurantSearchTool (이름으로 검색)
6. 추천 서버 → CLI (최종 응답)

#### 시나리오 3: 다른 사용자

```bash
python main.py --user-id bob --message "한식이 좋아"
python main.py --user-id bob --message "점심 먹을 곳 추천해줘"
```

**예상 출력**:
```
✅ 선호도(한식)를 기반으로 추천합니다:
1. Seoul Grill
2. Hanok Kitchen

Seoul Grill 상세 정보:
- 영업시간: 09:00-20:00
- 전화번호: 02-3456-7890
- 주소: 서울 종로구 인사동 789
```

#### 시나리오 4: 대화형 모드

```bash
python main.py --user-id alice
```

**예상 출력**:
```
=== Restaurant Agent CLI ===

사용자 ID: alice
종료하려면 'exit' 또는 'quit'를 입력하세요.

alice> 이탈리안 좋아해
✅ 선호도가 저장되었습니다.

alice> 배고파
✅ 선호도(이탈리안)를 기반으로 추천합니다:
1. La Trattoria
2. Pasta House
...

alice> exit
종료합니다.
```

## 문제 해결

### ❌ Mem0 API 키 오류

**증상**:
```
❌ MEM0_API_KEY 환경 변수가 필요합니다
```

**해결**:
```bash
# 1. API 키 발급 확인
# 🔗 https://app.mem0.ai/ → Login → API Keys

# 2. .env 파일 확인
cat .env | grep MEM0_API_KEY

# 3. API 키 입력 (m0-로 시작)
echo "MEM0_API_KEY=m0-your-api-key-here" >> .env

# 4. 서버 재시작
```

### ❌ Mem0 API 인증 실패

**증상**:
```
❌ Mem0 API 키가 유효하지 않습니다
```

**해결**:
```bash
# API 키 재생성
# 🔗 https://app.mem0.ai/ → API Keys → Regenerate

# .env 파일 업데이트
# MEM0_API_KEY=m0-new-key
```

### ❌ 네트워크 연결 오류

**증상**:
```
❌ 네트워크 연결에 실패했습니다
```

**해결**:
```bash
# 인터넷 연결 확인
curl https://api.mem0.ai/v1/health

# 프록시 설정 확인 (회사 방화벽 등)
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

### ❌ Ollama 연결 실패

**증상**:
```
openai.NotFoundError: Error code: 404 - {'error': {'message': "model 'qwen3-vl:4b' not found"}}
```

**해결**:
```bash
# 1. Ollama 실행 확인
curl http://localhost:11434/api/tags

# 2. 모델 다운로드 확인
ollama list

# 3. 모델이 없으면 다운로드
ollama pull qwen3-vl:4b

# 4. Ollama 서버 재시작
ollama serve
```

### ❌ 추천 에이전트 연결 실패

**증상**:
```
❌ 추천 에이전트에 연결할 수 없습니다
```

**해결**:
```bash
# 포트 8100 사용 중인 프로세스 확인
lsof -i :8100

# 프로세스 종료
kill -9 <PID>

# 서버 재실행
uv run python agents/recommender_agent.py
```

### ❌ 예약 에이전트 연결 실패 (A2A 호출 실패)

**증상**:
```
✅ 추천: La Trattoria, Pasta House
예약 에이전트에 연결할 수 없습니다
```

**해결**:
```bash
# 포트 8101 확인
curl http://localhost:8101/.well-known/agent-card.json

# 서버가 안 떠 있으면 실행
uv run python agents/booking_agent.py
```

## 고급 옵션

### Verbose 모드 (디버깅)

```bash
python main.py --user-id alice --message "배고파" --verbose
```

**예상 출력**:
```
=== 요청 ===
URL: http://localhost:8000/tasks/send
Payload: {'task_id': 'task_alice_1234', 'message': '배고파', 'user_id': 'alice'}

=== 응답 ===
Status: 200
Data: {'task_id': 'task_alice_1234', 'response': '선호도(이탈리안)를...'}

✅ 선호도(이탈리안)를 기반으로 추천합니다:
...
```

### 스크립트로 한 번에 실행

```bash
# run_servers.sh 사용
./run_servers.sh

# 또는 tmux 사용
tmux new-session -d -s recommender 'uv run python agents/recommender_agent.py'
tmux new-session -d -s booking 'uv run python agents/booking_agent.py'

# 세션 확인
tmux ls

# 종료
tmux kill-session -t recommender
tmux kill-session -t booking
```

## 다음 단계

- **확장 학습**: [ADVANCED.md](ADVANCED.md)에서 3번째 에이전트 추가 방법 학습
- **테스트**: `uv run pytest tests/ -v -k "not integration"` 실행
- **코드 리뷰**: 각 에이전트 코드 읽어보기 (recommender_agent.py, booking_agent.py)
