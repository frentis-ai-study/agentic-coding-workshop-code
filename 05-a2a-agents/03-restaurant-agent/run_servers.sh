#!/bin/bash

# Restaurant Agent Servers 실행 스크립트
#
# 2개의 FastAPI 서버를 실행합니다:
# - 추천 에이전트: 포트 8100
# - 예약 에이전트: 포트 8101

echo "=== Restaurant Agent Servers ==="
echo ""

# PYTHONPATH를 현재 디렉토리로 설정
export PYTHONPATH="$(pwd):$PYTHONPATH"

echo "추천 에이전트 서버 시작 (포트 8100)..."
uv run python agents/recommender_agent.py > /tmp/recommender.log 2>&1 &
RECOMMENDER_PID=$!
echo $RECOMMENDER_PID > /tmp/recommender.pid

echo "예약 에이전트 서버 시작 (포트 8101)..."
uv run python agents/booking_agent.py > /tmp/booking.log 2>&1 &
BOOKING_PID=$!
echo $BOOKING_PID > /tmp/booking.pid

sleep 2

echo ""
echo "✅ 서버 실행 완료!"
echo ""
echo "추천 에이전트: http://localhost:8100"
echo "예약 에이전트: http://localhost:8101"
echo ""
echo "Agent Cards 확인:"
echo "  curl http://localhost:8100/.well-known/agent-card.json"
echo "  curl http://localhost:8101/.well-known/agent-card.json"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

# 종료 시그널 처리
trap "echo '\n서버 종료 중...'; kill $RECOMMENDER_PID $BOOKING_PID; exit" INT TERM

# 대기
wait
