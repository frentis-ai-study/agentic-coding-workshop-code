"""날씨 도구 - 외부 API를 통해 날씨 정보를 조회합니다."""

import os
from typing import Any

import httpx
from fastmcp.exceptions import ToolError


def register_weather_tools(mcp):
    """날씨 도구들을 MCP 서버에 등록합니다.

    Args:
        mcp: FastMCP 서버 인스턴스
    """

    @mcp.tool
    async def get_weather(city: str) -> dict[str, Any]:
        """도시의 현재 날씨 정보를 조회합니다.

        외부 API 호출 실패 시 Mock 데이터를 반환합니다.
        """
        if not city or not city.strip():
            raise ToolError("도시 이름을 입력해주세요")

        api_key = os.getenv("WEATHER_API_KEY")

        # API 키가 없거나 실제 API 호출 실패 시 Mock 데이터 반환
        if not api_key:
            return _get_mock_weather(city)

        try:
            # OpenWeatherMap API 사용 예시
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": api_key, "units": "metric", "lang": "kr"}

            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                return {
                    "city": data["name"],
                    "temperature": round(data["main"]["temp"], 1),
                    "condition": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "is_mock": False,
                }

        except (httpx.HTTPError, KeyError, ValueError):
            # API 호출 실패 시 Mock 데이터로 폴백
            return _get_mock_weather(city)

    @mcp.tool
    async def get_forecast(city: str, days: int = 3) -> dict[str, Any]:
        """도시의 일기예보를 조회합니다 (Mock 데이터)."""
        if not city or not city.strip():
            raise ToolError("도시 이름을 입력해주세요")

        if not 1 <= days <= 7:
            raise ToolError("예보 일수는 1-7일 사이여야 합니다")

        # 현재는 Mock 데이터만 반환 (실습용)
        return {
            "city": city,
            "forecast": [
                {
                    "date": f"Day {i + 1}",
                    "temperature_high": 20 + i,
                    "temperature_low": 10 + i,
                    "condition": ["Sunny", "Cloudy", "Rainy"][i % 3],
                }
                for i in range(days)
            ],
            "is_mock": True,
        }


def _get_mock_weather(city: str) -> dict[str, Any]:
    """Mock 날씨 데이터 생성 (교육용)."""
    return {
        "city": city,
        "temperature": 20,
        "condition": "Sunny",
        "humidity": 55,
        "wind_speed": 3.5,
        "is_mock": True,
    }
