# Docker 문제 해결 가이드

Docker 및 Docker Compose 사용 중 발생할 수 있는 일반적인 문제와 해결 방법입니다.

## 1. 설치 및 환경 문제

### Docker Desktop이 시작되지 않음 (macOS/Windows)

**증상**
- Docker Desktop 아이콘이 회색으로 표시됨
- "Docker is not running" 오류

**해결 방법**
```bash
# 1. Docker Desktop 완전 종료
# macOS
killall Docker

# Windows (PowerShell 관리자 권한)
Stop-Service docker

# 2. Docker Desktop 재시작
# macOS: Applications에서 Docker 실행
# Windows: 시작 메뉴에서 Docker Desktop 실행

# 3. 여전히 안 되면 재설치
```

### WSL2 관련 오류 (Windows)

**증상**
- "WSL 2 installation is incomplete" 오류
- "The virtual machine could not be started"

**해결 방법**
```powershell
# PowerShell 관리자 권한으로 실행

# 1. WSL2 활성화
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 2. 재부팅
Restart-Computer

# 3. WSL2 커널 업데이트
# https://aka.ms/wsl2kernel 에서 다운로드 후 설치

# 4. WSL2를 기본값으로 설정
wsl --set-default-version 2
```

### Permission Denied (Linux)

**증상**
```
Got permission denied while trying to connect to the Docker daemon socket
```

**해결 방법**
```bash
# 1. 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 2. 로그아웃 후 재로그인 (또는 재부팅)

# 3. 확인
docker run hello-world
```

## 2. 이미지 및 빌드 문제

### 이미지 빌드 실패

**증상**
```
ERROR [internal] load metadata for docker.io/library/python:3.12
```

**해결 방법**
```bash
# 1. Docker Hub 연결 확인
docker pull hello-world

# 2. DNS 문제일 경우
# macOS/Linux: /etc/docker/daemon.json
# Windows: Docker Desktop Settings > Docker Engine
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}

# 3. Docker 재시작
# macOS/Windows: Docker Desktop 재시작
# Linux:
sudo systemctl restart docker
```

### 빌드 캐시 문제

**증상**
- 코드를 수정했는데 이전 버전으로 빌드됨
- 의존성 변경이 반영되지 않음

**해결 방법**
```bash
# 캐시 무시하고 빌드
docker-compose build --no-cache

# 또는 특정 서비스만
docker-compose build --no-cache mcp-server
```

### 디스크 공간 부족

**증상**
```
no space left on device
```

**해결 방법**
```bash
# 1. 디스크 사용량 확인
docker system df

# 2. 미사용 리소스 정리
docker system prune -a --volumes

# 3. 특정 리소스만 정리
docker image prune -a  # 이미지
docker container prune  # 컨테이너
docker volume prune  # 볼륨
docker network prune  # 네트워크
```

## 3. 컨테이너 실행 문제

### 컨테이너가 즉시 종료됨

**증상**
```bash
$ docker-compose ps
NAME     STATUS
app      Exited (1)
```

**해결 방법**
```bash
# 1. 로그 확인
docker-compose logs app

# 2. 실패한 컨테이너 유지하고 디버깅
docker-compose run --entrypoint /bin/bash app

# 3. 일반적인 원인
# - 환경변수 누락 (.env 파일 확인)
# - 의존성 문제 (requirements.txt 확인)
# - 포트 충돌 (다른 서비스가 같은 포트 사용)
```

### 포트 바인딩 실패

**증상**
```
Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use
```

**해결 방법**
```bash
# 1. 포트 사용 중인 프로세스 확인
# macOS/Linux
lsof -i :8000

# Windows (PowerShell)
netstat -ano | findstr :8000

# 2. 프로세스 종료 (PID 확인 후)
# macOS/Linux
kill -9 <PID>

# Windows
taskkill /PID <PID> /F

# 3. 또는 docker-compose.yml에서 다른 포트 사용
ports:
  - "8001:8000"
```

### 환경변수가 로드되지 않음

**증상**
- 컨테이너 내부에서 환경변수가 비어있음

**해결 방법**
```bash
# 1. .env 파일 위치 확인 (docker-compose.yml과 같은 디렉토리)
ls -la .env

# 2. .env 파일 형식 확인 (주석, 공백 주의)
# 올바른 형식:
API_KEY=secret123
# 잘못된 형식:
# API_KEY = secret123  (공백 있으면 안 됨)
# export API_KEY=secret123  (export 불필요)

# 3. 환경변수 확인
docker-compose config  # 변수가 치환된 설정 출력
docker-compose exec app env  # 컨테이너 내부 환경변수 확인
```

## 4. 네트워크 문제

### 서비스 간 통신 실패

**증상**
```
curl: (6) Could not resolve host: mcp-server
```

**해결 방법**
```bash
# 1. 같은 네트워크에 있는지 확인
docker-compose config

# 2. 네트워크 재생성
docker-compose down
docker-compose up -d

# 3. 컨테이너 이름으로 연결 확인
docker-compose exec chat-app ping mcp-server

# 4. DNS 확인
docker-compose exec chat-app nslookup mcp-server
```

### host.docker.internal 접근 실패 (Linux)

**증상**
```
curl: (6) Could not resolve host: host.docker.internal
```

**해결 방법**
```bash
# Linux에서는 host.docker.internal이 기본 지원되지 않음

# 해결법 1: docker-compose.yml에 추가
services:
  app:
    extra_hosts:
      - "host.docker.internal:host-gateway"

# 해결법 2: 호스트 IP 직접 사용
# 호스트 IP 확인
ip addr show docker0 | grep inet
# 예: 172.17.0.1

# .env에서 사용
OPENAI_API_BASE=http://172.17.0.1:11434/v1
```

## 5. 볼륨 및 데이터 문제

### 볼륨 데이터가 유지되지 않음

**증상**
- 컨테이너 재시작 후 데이터 손실

**해결 방법**
```bash
# 1. 볼륨 마운트 확인
docker-compose config

# 2. 네임드 볼륨 사용 (권장)
volumes:
  - chat-data:/app/data  # ✅ 올바름

# 익명 볼륨 (데이터 손실 위험)
volumes:
  - /app/data  # ❌ 피하기

# 3. 볼륨 목록 확인
docker volume ls

# 4. 볼륨 정보 확인
docker volume inspect <volume-name>
```

### Permission Denied (볼륨)

**증상**
```
PermissionError: [Errno 13] Permission denied: '/app/data/file.db'
```

**해결 방법**
```bash
# 1. Dockerfile에서 권한 설정
# Dockerfile
RUN mkdir -p /app/data && chmod 777 /app/data

# 2. 또는 USER 지시자 사용
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# 3. 호스트 디렉토리 권한 확인 (바인드 마운트 사용 시)
chmod -R 755 ./data
```

## 6. 성능 문제

### 컨테이너가 느림 (macOS/Windows)

**증상**
- 파일 I/O가 매우 느림
- 빌드 시간이 오래 걸림

**해결 방법**
```bash
# 1. 볼륨 마운트 대신 네임드 볼륨 사용
# 느림:
volumes:
  - ./src:/app/src

# 빠름:
volumes:
  - src-data:/app/src

# 2. Docker Desktop 리소스 증가
# Settings > Resources > Advanced
# - CPUs: 4개 이상
# - Memory: 4GB 이상

# 3. VirtioFS 사용 (macOS)
# Settings > Experimental Features > VirtioFS 활성화
```

### 메모리 부족

**증상**
```
Killed
```

**해결 방법**
```bash
# 1. Docker Desktop 메모리 증가
# Settings > Resources > Advanced > Memory

# 2. docker-compose.yml에서 제한 설정
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G

# 3. 메모리 사용량 모니터링
docker stats
```

## 7. Ollama 통합 문제

### Ollama 연결 실패

**증상**
```
ConnectionError: Failed to connect to http://host.docker.internal:11434
```

**해결 방법**
```bash
# 1. Ollama가 실행 중인지 확인
curl http://localhost:11434/api/version

# 2. Ollama가 모든 인터페이스에서 listen하는지 확인
# ~/.ollama/config.json
{
  "host": "0.0.0.0:11434"
}

# Ollama 재시작
ollama serve

# 3. 방화벽 확인
# macOS
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/ollama

# 4. Linux에서는 호스트 IP 직접 사용
# docker-compose.yml
extra_hosts:
  - "host.docker.internal:172.17.0.1"
```

### Ollama 모델이 없음

**증상**
```
model 'llama3.2' not found
```

**해결 방법**
```bash
# 1. 모델 다운로드
ollama pull llama3.2

# 2. 설치된 모델 확인
ollama list

# 3. .env에서 모델 이름 확인
OPENAI_MODEL_NAME=llama3.2  # ollama list 결과와 일치해야 함
```

## 8. 일반적인 디버깅 절차

### 단계별 디버깅 체크리스트

```bash
# 1. 기본 확인
docker --version
docker-compose --version
docker info

# 2. 서비스 상태
docker-compose ps

# 3. 로그 확인
docker-compose logs -f

# 4. 설정 검증
docker-compose config

# 5. 네트워크 확인
docker network ls
docker network inspect <network-name>

# 6. 볼륨 확인
docker volume ls
docker volume inspect <volume-name>

# 7. 컨테이너 내부 접근
docker-compose exec <service> /bin/bash

# 8. 리소스 사용량
docker stats

# 9. 전체 정리 후 재시작
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

## 9. 플랫폼별 특수 문제

### macOS Apple Silicon (M1/M2/M3)

**문제**: 일부 이미지가 ARM64 지원 안 함

**해결**:
```dockerfile
# Dockerfile에서 플랫폼 명시
FROM --platform=linux/amd64 python:3.12

# 또는 docker-compose.yml
services:
  app:
    platform: linux/amd64
```

### Windows 경로 문제

**문제**: 볼륨 마운트 경로 오류

**해결**:
```yaml
# Windows에서는 절대 경로 사용
volumes:
  - C:/Users/myuser/data:/app/data

# 또는 WSL2 경로
volumes:
  - /mnt/c/Users/myuser/data:/app/data
```

## 10. 추가 리소스

- [Docker 공식 문제 해결 가이드](https://docs.docker.com/config/daemon/)
- [Docker Community Forums](https://forums.docker.com/)
- [Stack Overflow - Docker 태그](https://stackoverflow.com/questions/tagged/docker)
