#!/bin/bash
# 채팅 앱 엔트리포인트 스크립트

set -e

echo "🚀 Starting MCP Chat Client..."
echo "📍 Working Directory: $(pwd)"

# 환경변수 확인
echo "🔧 Configuration:"
echo "  - OPENAI_API_BASE: ${OPENAI_API_BASE}"
echo "  - MODEL_NAME: ${MODEL_NAME}"
echo "  - DATABASE_URL: ${DATABASE_URL}"

# 데이터베이스 디렉토리 생성 (SQLite 파일용)
mkdir -p /app/data

# Streamlit 앱 실행
cd 04-testing-deployment/02-mcp-chat-client
exec streamlit run app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true
