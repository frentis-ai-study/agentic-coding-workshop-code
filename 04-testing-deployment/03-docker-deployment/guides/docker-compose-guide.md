# Docker Compose 가이드

Docker Compose를 사용하여 멀티 컨테이너 애플리케이션을 관리하는 가이드입니다.

## 1. Docker Compose란?

Docker Compose는 여러 개의 Docker 컨테이너를 정의하고 실행하기 위한 도구입니다.
YAML 파일 하나로 전체 애플리케이션 스택을 관리할 수 있습니다.

### 주요 특징
- **멀티 컨테이너 관리**: 여러 서비스를 하나의 파일로 정의
- **네트워크 자동 생성**: 서비스 간 통신을 위한 네트워크 자동 구성
- **볼륨 관리**: 데이터 영속성을 위한 볼륨 관리
- **환경변수 관리**: .env 파일로 설정 관리

## 2. 기본 명령어

### 서비스 시작
```bash
# 백그라운드 실행
docker-compose up -d

# 포그라운드 실행 (로그 실시간 확인)
docker-compose up

# 특정 서비스만 시작
docker-compose up -d mcp-server

# 이미지 강제 재빌드 후 시작
docker-compose up -d --build

# 이전 컨테이너 제거 후 시작
docker-compose up -d --force-recreate
```

### 서비스 중지
```bash
# 서비스 중지 (컨테이너 유지)
docker-compose stop

# 서비스 중지 및 컨테이너 삭제
docker-compose down

# 볼륨도 함께 삭제
docker-compose down -v

# 이미지도 함께 삭제
docker-compose down --rmi all
```

### 서비스 상태 확인
```bash
# 실행 중인 서비스 확인
docker-compose ps

# 모든 서비스 확인 (중지된 것 포함)
docker-compose ps -a

# 서비스 상세 정보
docker-compose config
```

### 로그 확인
```bash
# 모든 서비스 로그
docker-compose logs

# 특정 서비스 로그
docker-compose logs mcp-server

# 실시간 로그 스트림
docker-compose logs -f

# 마지막 100줄만
docker-compose logs --tail=100

# 타임스탬프 포함
docker-compose logs -t
```

### 서비스 재시작
```bash
# 모든 서비스 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart mcp-server
```

### 이미지 빌드
```bash
# 모든 서비스 이미지 빌드
docker-compose build

# 특정 서비스만 빌드
docker-compose build mcp-server

# 캐시 없이 빌드
docker-compose build --no-cache
```

## 3. docker-compose.yml 구조

### 기본 구조
```yaml
version: '3.8'  # Docker Compose 파일 버전

services:  # 서비스 정의
  service1:
    # 서비스 설정
  service2:
    # 서비스 설정

networks:  # 네트워크 정의 (선택사항)
  my-network:

volumes:  # 볼륨 정의 (선택사항)
  my-volume:
```

### 서비스 설정 옵션

#### 이미지 사용
```yaml
services:
  app:
    image: python:3.12  # Docker Hub 이미지 사용
```

#### Dockerfile로 빌드
```yaml
services:
  app:
    build:
      context: .  # Dockerfile이 있는 디렉토리
      dockerfile: Dockerfile  # Dockerfile 이름
      args:  # 빌드 인자
        VERSION: 1.0
```

#### 포트 매핑
```yaml
services:
  app:
    ports:
      - "8000:8000"  # 호스트:컨테이너
      - "127.0.0.1:8001:8001"  # 특정 IP 바인딩
```

#### 환경변수
```yaml
services:
  app:
    environment:
      - API_KEY=secret
      - DEBUG=true
    # 또는 파일에서 로드
    env_file:
      - .env
      - config/app.env
```

#### 볼륨 마운트
```yaml
services:
  app:
    volumes:
      - ./data:/app/data  # 바인드 마운트
      - mydata:/app/mydata  # 네임드 볼륨
      - /app/cache  # 익명 볼륨
```

#### 네트워크
```yaml
services:
  app:
    networks:
      - frontend
      - backend

networks:
  frontend:
  backend:
```

#### 의존성
```yaml
services:
  app:
    depends_on:
      - db  # db 서비스가 먼저 시작됨
```

#### 재시작 정책
```yaml
services:
  app:
    restart: always  # 항상 재시작
    # restart: on-failure  # 실패 시만 재시작
    # restart: unless-stopped  # 수동 중지 전까지 재시작
```

#### 헬스체크
```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### 리소스 제한
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'  # CPU 50%
          memory: 512M  # 메모리 512MB
        reservations:
          cpus: '0.25'
          memory: 256M
```

## 4. 실전 예제

### 예제 1: Part 4 MCP 스택

```yaml
version: '3.8'

services:
  mcp-server:
    build:
      context: ../..
      dockerfile: 04-testing-deployment/03-docker-deployment/Dockerfile.mcp
    container_name: fastmcp-server
    ports:
      - "8000:8000"
    environment:
      - MCP_SERVER_TYPE=tools
    networks:
      - mcp-network
    restart: unless-stopped

  chat-app:
    build:
      context: ../..
      dockerfile: 04-testing-deployment/03-docker-deployment/Dockerfile.chat
    container_name: fastmcp-chat
    ports:
      - "8501:8501"
    environment:
      - MCP_SERVER_URL=http://mcp-server:8000
      - OPENAI_API_BASE=http://host.docker.internal:11434/v1
    volumes:
      - ./data:/app/data
    depends_on:
      - mcp-server
    networks:
      - mcp-network
    restart: unless-stopped

networks:
  mcp-network:
    driver: bridge

volumes:
  chat-data:
```

### 예제 2: 개발 환경 오버라이드

**docker-compose.yml** (프로덕션)
```yaml
version: '3.8'
services:
  app:
    image: my-app:latest
    restart: always
```

**docker-compose.override.yml** (자동 병합, 개발 전용)
```yaml
version: '3.8'
services:
  app:
    volumes:
      - ./src:/app/src  # 소스 코드 마운트
    environment:
      - DEBUG=true
    restart: "no"  # 개발 시 자동 재시작 비활성화
```

실행:
```bash
# override.yml이 자동으로 병합됨
docker-compose up -d

# 프로덕션 설정만 사용
docker-compose -f docker-compose.yml up -d
```

## 5. 환경변수 관리

### .env 파일
```bash
# .env
API_KEY=secret123
DATABASE_URL=postgresql://user:pass@db:5432/mydb
```

### docker-compose.yml에서 사용
```yaml
services:
  app:
    image: my-app:${APP_VERSION:-latest}
    environment:
      - API_KEY=${API_KEY}
      - DATABASE_URL=${DATABASE_URL}
```

### 변수 우선순위
1. docker-compose.yml의 environment
2. .env 파일
3. 셸 환경변수
4. Dockerfile의 ENV

## 6. 네트워크 패턴

### 패턴 1: 단일 네트워크 (간단)
```yaml
services:
  frontend:
    networks:
      - app-network
  backend:
    networks:
      - app-network
networks:
  app-network:
```

### 패턴 2: 멀티 네트워크 (보안 강화)
```yaml
services:
  frontend:
    networks:
      - public
      - backend
  backend:
    networks:
      - backend
      - database
  db:
    networks:
      - database  # 프론트엔드에서 직접 접근 불가

networks:
  public:
  backend:
  database:
```

### 패턴 3: 외부 네트워크 사용
```yaml
services:
  app:
    networks:
      - existing-network

networks:
  existing-network:
    external: true
```

## 7. 볼륨 패턴

### 패턴 1: 네임드 볼륨 (권장)
```yaml
services:
  app:
    volumes:
      - app-data:/app/data

volumes:
  app-data:  # Docker가 관리
```

### 패턴 2: 바인드 마운트 (개발)
```yaml
services:
  app:
    volumes:
      - ./src:/app/src  # 호스트 경로 직접 마운트
```

### 패턴 3: 읽기 전용 마운트
```yaml
services:
  app:
    volumes:
      - ./config:/app/config:ro  # 읽기 전용
```

## 8. 실전 워크플로우

### 초기 설정
```bash
# 1. .env 파일 생성
cp .env.example .env
nano .env  # 환경변수 수정

# 2. 빌드 및 시작
docker-compose up -d --build

# 3. 로그 확인
docker-compose logs -f
```

### 개발 중
```bash
# 코드 변경 후 특정 서비스만 재빌드
docker-compose up -d --build app

# 로그 실시간 확인
docker-compose logs -f app

# 컨테이너 내부 접근
docker-compose exec app /bin/bash
```

### 디버깅
```bash
# 서비스 상태 확인
docker-compose ps

# 특정 서비스 재시작
docker-compose restart app

# 설정 검증
docker-compose config

# 네트워크 확인
docker-compose exec app ping backend
```

### 정리
```bash
# 서비스 중지 및 삭제
docker-compose down

# 볼륨까지 삭제
docker-compose down -v

# 이미지까지 삭제
docker-compose down --rmi all
```

## 9. 문제 해결

### 문제 1: 서비스가 시작되지 않음
```bash
# 로그 확인
docker-compose logs service-name

# 설정 검증
docker-compose config

# 컨테이너 강제 재생성
docker-compose up -d --force-recreate
```

### 문제 2: 네트워크 연결 실패
```bash
# 네트워크 재생성
docker-compose down
docker-compose up -d

# 네트워크 확인
docker network ls
docker network inspect <network-name>
```

### 문제 3: 볼륨 데이터 손실
```bash
# 볼륨 목록 확인
docker volume ls

# 볼륨 정보 확인
docker volume inspect <volume-name>

# 백업 (컨테이너를 통해)
docker run --rm -v <volume-name>:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .
```

### 문제 4: 포트 충돌
```bash
# 포트 변경 (docker-compose.yml)
ports:
  - "8001:8000"  # 호스트 포트를 8001로 변경
```

## 10. 고급 기능

### 스케일링
```bash
# 서비스 인스턴스 3개로 확장
docker-compose up -d --scale app=3
```

### 프로파일 (v1.28+)
```yaml
services:
  app:
    profiles: ["production"]
  debug-tool:
    profiles: ["debug"]
```

```bash
# 특정 프로파일만 실행
docker-compose --profile production up -d
```

### 빌드 인자
```yaml
services:
  app:
    build:
      args:
        - PYTHON_VERSION=3.12
        - BUILD_DATE=${BUILD_DATE}
```

```bash
# 빌드 시 변수 전달
BUILD_DATE=$(date) docker-compose build
```

## 11. 참고 자료

- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [Compose 파일 레퍼런스](https://docs.docker.com/compose/compose-file/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
