"""날짜/시간 도구 - 현재 날짜와 시간 정보를 제공합니다."""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo


def register_datetime_tools(mcp):
    """날짜/시간 도구들을 MCP 서버에 등록합니다.

    Args:
        mcp: FastMCP 서버 인스턴스
    """

    @mcp.tool
    def get_current_datetime(timezone: str = "Asia/Seoul") -> dict[str, Any]:
        """현재 날짜와 시간을 조회합니다.

        Args:
            timezone: 시간대 (기본값: "Asia/Seoul")
                     예: "UTC", "America/New_York", "Europe/London"

        Returns:
            현재 날짜/시간 정보를 담은 딕셔너리:
            - datetime: ISO 8601 형식 문자열 (예: "2025-11-23T00:30:15+09:00")
            - date: 날짜 (예: "2025-11-23")
            - time: 시간 (예: "00:30:15")
            - timezone: 시간대 이름
            - year: 연도
            - month: 월 (1-12)
            - day: 일 (1-31)
            - hour: 시 (0-23)
            - minute: 분 (0-59)
            - second: 초 (0-59)
            - weekday: 요일 (0=월요일, 6=일요일)
            - weekday_name: 요일 이름 (한국어)

        Examples:
            >>> get_current_datetime()
            {'datetime': '2025-11-23T00:30:15+09:00', 'date': '2025-11-23', ...}

            >>> get_current_datetime("UTC")
            {'datetime': '2025-11-22T15:30:15+00:00', 'timezone': 'UTC', ...}
        """
        try:
            tz = ZoneInfo(timezone)
        except Exception:
            # 잘못된 시간대인 경우 기본값 사용
            tz = ZoneInfo("Asia/Seoul")
            timezone = "Asia/Seoul"

        now = datetime.now(tz)

        weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

        return {
            "datetime": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "timezone": timezone,
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "weekday": now.weekday(),
            "weekday_name": weekday_names[now.weekday()],
        }

    @mcp.tool
    def get_timestamp() -> dict[str, Any]:
        """현재 Unix 타임스탬프를 조회합니다.

        Returns:
            타임스탬프 정보를 담은 딕셔너리:
            - timestamp: Unix 타임스탬프 (초 단위)
            - timestamp_ms: Unix 타임스탬프 (밀리초 단위)
            - iso_utc: UTC 기준 ISO 8601 형식 문자열

        Examples:
            >>> get_timestamp()
            {'timestamp': 1732291815, 'timestamp_ms': 1732291815123, ...}
        """
        now_utc = datetime.now(ZoneInfo("UTC"))
        timestamp = now_utc.timestamp()

        return {
            "timestamp": int(timestamp),
            "timestamp_ms": int(timestamp * 1000),
            "iso_utc": now_utc.isoformat(),
        }
