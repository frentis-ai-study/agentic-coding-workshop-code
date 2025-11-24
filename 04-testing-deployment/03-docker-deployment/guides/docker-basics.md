# Docker 기본 명령어 가이드

Docker를 처음 사용하거나 기본 명령어를 빠르게 참조할 때 사용하는 가이드입니다.

## 1. Docker 이미지 관리

### 이미지 목록 확인
```bash
docker images
# 또는
docker image ls
```

### 이미지 빌드
```bash
# 현재 디렉토리의 Dockerfile로 빌드
docker build -t my-image:latest .

# 특정 Dockerfile 사용
docker build -f Dockerfile.mcp -t mcp-server:latest .

# 빌드 캐시 무시
docker build --no-cache -t my-image:latest .
```

### 이미지 삭제
```bash
# 특정 이미지 삭제
docker rmi my-image:latest

# 사용하지 않는 모든 이미지 삭제
docker image prune -a
```

### 이미지 정보 확인
```bash
docker inspect my-image:latest

# 이미지 히스토리 확인
docker history my-image:latest
```

## 2. Docker 컨테이너 관리

### 컨테이너 실행
```bash
# 기본 실행
docker run my-image:latest

# 백그라운드 실행
docker run -d my-image:latest

# 포트 매핑
docker run -p 8000:8000 my-image:latest

# 이름 지정
docker run --name my-container my-image:latest

# 환경변수 전달
docker run -e API_KEY=secret my-image:latest

# 볼륨 마운트
docker run -v ./data:/app/data my-image:latest

# 컨테이너 종료 시 자동 삭제
docker run --rm my-image:latest
```

### 컨테이너 목록 확인
```bash
# 실행 중인 컨테이너
docker ps

# 모든 컨테이너 (중지된 것 포함)
docker ps -a

# 최근 컨테이너 1개
docker ps -l
```

### 컨테이너 제어
```bash
# 컨테이너 시작
docker start my-container

# 컨테이너 중지
docker stop my-container

# 컨테이너 재시작
docker restart my-container

# 컨테이너 강제 종료
docker kill my-container

# 컨테이너 일시 정지
docker pause my-container

# 컨테이너 재개
docker unpause my-container
```

### 컨테이너 삭제
```bash
# 특정 컨테이너 삭제 (중지된 상태여야 함)
docker rm my-container

# 강제 삭제 (실행 중이어도 삭제)
docker rm -f my-container

# 모든 중지된 컨테이너 삭제
docker container prune
```

## 3. 컨테이너 디버깅

### 로그 확인
```bash
# 전체 로그 출력
docker logs my-container

# 실시간 로그 스트림 (tail -f와 유사)
docker logs -f my-container

# 마지막 100줄만 출력
docker logs --tail 100 my-container

# 타임스탬프 포함
docker logs -t my-container
```

### 컨테이너 내부 접근
```bash
# 컨테이너 내부 셸 실행
docker exec -it my-container /bin/bash

# 또는 sh (경량 이미지의 경우)
docker exec -it my-container /bin/sh

# 특정 명령어 실행
docker exec my-container ls -la /app
```

### 컨테이너 상태 확인
```bash
# 상세 정보 확인
docker inspect my-container

# 리소스 사용량 확인
docker stats my-container

# 실행 중인 프로세스 확인
docker top my-container
```

### 파일 복사
```bash
# 호스트 → 컨테이너
docker cp ./local-file.txt my-container:/app/file.txt

# 컨테이너 → 호스트
docker cp my-container:/app/file.txt ./local-file.txt
```

## 4. Docker 네트워크

### 네트워크 목록 확인
```bash
docker network ls
```

### 네트워크 생성
```bash
docker network create my-network
```

### 네트워크에 컨테이너 연결
```bash
docker network connect my-network my-container
```

### 네트워크 정보 확인
```bash
docker network inspect my-network
```

### 네트워크 삭제
```bash
docker network rm my-network
```

## 5. Docker 볼륨

### 볼륨 목록 확인
```bash
docker volume ls
```

### 볼륨 생성
```bash
docker volume create my-volume
```

### 볼륨 정보 확인
```bash
docker volume inspect my-volume
```

### 볼륨 삭제
```bash
docker volume rm my-volume

# 사용하지 않는 모든 볼륨 삭제
docker volume prune
```

## 6. 시스템 관리

### 디스크 사용량 확인
```bash
docker system df
```

### 전체 정리 (미사용 리소스 삭제)
```bash
# 중지된 컨테이너, 미사용 네트워크, 댕글링 이미지, 빌드 캐시 삭제
docker system prune

# 모든 미사용 이미지도 삭제
docker system prune -a

# 볼륨도 삭제
docker system prune --volumes
```

### Docker 정보 확인
```bash
docker info
docker version
```

## 7. 유용한 조합 명령어

### 모든 컨테이너 중지
```bash
docker stop $(docker ps -q)
```

### 모든 컨테이너 삭제
```bash
docker rm $(docker ps -a -q)
```

### 특정 패턴의 이미지 삭제
```bash
docker rmi $(docker images | grep "my-pattern" | awk '{print $3}')
```

### 컨테이너 IP 주소 확인
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-container
```

## 8. 실습 예제

### 예제 1: Nginx 웹 서버 실행
```bash
# Nginx 이미지 다운로드 및 실행
docker run -d -p 8080:80 --name my-nginx nginx:latest

# 브라우저에서 http://localhost:8080 접속
# 로그 확인
docker logs -f my-nginx

# 중지 및 삭제
docker stop my-nginx
docker rm my-nginx
```

### 예제 2: Python 스크립트 실행
```bash
# Python 이미지로 스크립트 실행
docker run --rm -v $(pwd):/app -w /app python:3.12 python script.py
```

### 예제 3: 데이터 볼륨 사용
```bash
# 볼륨 생성
docker volume create mydata

# 볼륨을 사용하는 컨테이너 실행
docker run -d -v mydata:/data --name app1 my-image

# 같은 볼륨을 공유하는 다른 컨테이너
docker run -d -v mydata:/data --name app2 my-image
```

## 9. 문제 해결 팁

### 컨테이너가 즉시 종료되는 경우
```bash
# 로그 확인
docker logs my-container

# 실패한 컨테이너 유지하고 디버깅
docker run -it --entrypoint /bin/bash my-image
```

### 포트가 이미 사용 중인 경우
```bash
# 포트 사용 중인 프로세스 확인 (macOS/Linux)
lsof -i :8000

# 다른 포트로 매핑
docker run -p 8001:8000 my-image
```

### 디스크 공간 부족
```bash
# 미사용 리소스 정리
docker system prune -a --volumes
```

## 10. 참고 자료

- [Docker 공식 문서](https://docs.docker.com/)
- [Docker CLI 레퍼런스](https://docs.docker.com/engine/reference/commandline/cli/)
- [Docker Hub](https://hub.docker.com/)
