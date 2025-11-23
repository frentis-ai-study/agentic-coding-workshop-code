#!/bin/bash

# Restaurant Agent Servers 종료 스크립트

echo "=== Restaurant Agent Servers 종료 ==="
echo ""

# PID 파일에서 프로세스 ID 읽기
if [ -f /tmp/recommender.pid ]; then
    RECOMMENDER_PID=$(cat /tmp/recommender.pid)
    if ps -p $RECOMMENDER_PID > /dev/null 2>&1; then
        echo "추천 에이전트 종료 (PID: $RECOMMENDER_PID)..."
        kill $RECOMMENDER_PID
    else
        echo "추천 에이전트가 실행 중이지 않습니다."
    fi
    rm -f /tmp/recommender.pid
else
    echo "추천 에이전트 PID 파일을 찾을 수 없습니다."
fi

if [ -f /tmp/booking.pid ]; then
    BOOKING_PID=$(cat /tmp/booking.pid)
    if ps -p $BOOKING_PID > /dev/null 2>&1; then
        echo "예약 에이전트 종료 (PID: $BOOKING_PID)..."
        kill $BOOKING_PID
    else
        echo "예약 에이전트가 실행 중이지 않습니다."
    fi
    rm -f /tmp/booking.pid
else
    echo "예약 에이전트 PID 파일을 찾을 수 없습니다."
fi

# 포트로 찾아서 종료 (백업)
echo ""
echo "포트 8100, 8101을 사용하는 프로세스 확인..."
lsof -ti:8100 | xargs -r kill 2>/dev/null && echo "포트 8100 프로세스 종료" || true
lsof -ti:8101 | xargs -r kill 2>/dev/null && echo "포트 8101 프로세스 종료" || true

echo ""
echo "✅ 서버 종료 완료!"
