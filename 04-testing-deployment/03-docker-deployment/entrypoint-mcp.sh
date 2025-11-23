#!/bin/bash
# MCP 서버 엔트리포인트 스크립트

set -e

echo "🚀 Starting MCP Server..."
echo "📦 Server Type: ${MCP_SERVER_TYPE:-tools}"

# MCP 서버 타입에 따라 실행
case "${MCP_SERVER_TYPE}" in
  basic)
    echo "▶️ Running Basic MCP Server..."
    cd 03-mcp-tools/01-basic-server
    exec uv run python server.py
    ;;
  tools)
    echo "▶️ Running Tools MCP Server..."
    cd 03-mcp-tools/02-tools
    exec uv run python server.py
    ;;
  resources)
    echo "▶️ Running Resources MCP Server..."
    cd 03-mcp-tools/04-resources
    exec uv run python server.py
    ;;
  *)
    echo "❌ Unknown MCP_SERVER_TYPE: ${MCP_SERVER_TYPE}"
    echo "Valid types: basic, tools, resources"
    exit 1
    ;;
esac
