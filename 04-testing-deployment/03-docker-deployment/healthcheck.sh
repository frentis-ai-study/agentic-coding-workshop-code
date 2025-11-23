#!/bin/bash
# Docker 컨테이너 헬스체크 스크립트
# 이 스크립트는 docker-compose.yml의 healthcheck에서 사용됩니다

set -e

# 컨테이너 타입 확인 (환경변수로 전달)
CONTAINER_TYPE=${CONTAINER_TYPE:-"unknown"}

case "$CONTAINER_TYPE" in
  "mcp-server")
    # MCP 서버 헬스체크: HTTP 엔드포인트 확인
    curl -f http://localhost:${MCP_SERVER_PORT:-8000}/health || exit 1
    ;;

  "chat-app")
    # Streamlit 앱 헬스체크: Streamlit 서버 응답 확인
    curl -f http://localhost:${STREAMLIT_SERVER_PORT:-8501}/_stcore/health || exit 1
    ;;

  *)
    echo "Unknown container type: $CONTAINER_TYPE"
    exit 1
    ;;
esac

echo "$CONTAINER_TYPE is healthy"
exit 0
