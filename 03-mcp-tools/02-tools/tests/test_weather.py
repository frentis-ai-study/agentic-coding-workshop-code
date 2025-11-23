"""Weather 도구 테스트."""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastmcp import FastMCP
from fastmcp.client import Client
from tools.weather import register_weather_tools


@pytest.fixture
async def mcp_client():
    """테스트용 MCP 클라이언트를 생성합니다."""
    mcp = FastMCP(name="TestWeatherServer")
    register_weather_tools(mcp)

    async with Client(transport=mcp) as client:
        yield client


async def test_get_weather_mock_data(mcp_client):
    """Mock 날씨 데이터 조회 테스트."""
    # API 키가 없으면 Mock 데이터 반환
    result = await mcp_client.call_tool("get_weather", {"city": "Seoul"})

    assert result.data["city"] == "Seoul"
    assert "temperature" in result.data
    assert "condition" in result.data
    assert "humidity" in result.data
    assert result.data["is_mock"] is True


async def test_get_weather_known_cities(mcp_client):
    """알려진 도시들의 Mock 데이터 테스트."""
    cities = ["Seoul", "Tokyo", "New York", "London"]

    for city in cities:
        result = await mcp_client.call_tool("get_weather", {"city": city})
        assert result.data["city"] == city
        assert isinstance(result.data["temperature"], (int, float))
        assert isinstance(result.data["condition"], str)
        assert isinstance(result.data["humidity"], int)
        assert result.data["is_mock"] is True


async def test_get_weather_empty_city(mcp_client):
    """빈 도시 이름 에러 테스트."""
    result = await mcp_client.call_tool("get_weather", {"city": ""}, raise_on_error=False)

    assert result.is_error is True
    assert "도시 이름을 입력해주세요" in str(result.content)


async def test_get_forecast_success(mcp_client):
    """일기예보 조회 성공 테스트."""
    result = await mcp_client.call_tool("get_forecast", {"city": "Seoul", "days": 3})

    assert result.data["city"] == "Seoul"
    assert len(result.data["forecast"]) == 3
    assert result.data["is_mock"] is True

    # 첫 번째 예보 확인
    first_day = result.data["forecast"][0]
    assert "date" in first_day
    assert "temperature_high" in first_day
    assert "temperature_low" in first_day
    assert "condition" in first_day


async def test_get_forecast_different_days(mcp_client):
    """다양한 예보 일수 테스트."""
    for days in [1, 3, 5, 7]:
        result = await mcp_client.call_tool("get_forecast", {"city": "Tokyo", "days": days})
        assert len(result.data["forecast"]) == days


async def test_get_forecast_invalid_days(mcp_client):
    """잘못된 예보 일수 에러 테스트."""
    # 0일
    result = await mcp_client.call_tool(
        "get_forecast", {"city": "Seoul", "days": 0}, raise_on_error=False
    )
    assert result.is_error is True
    assert "1-7일 사이여야 합니다" in str(result.content)

    # 8일
    result = await mcp_client.call_tool(
        "get_forecast", {"city": "Seoul", "days": 8}, raise_on_error=False
    )
    assert result.is_error is True
    assert "1-7일 사이여야 합니다" in str(result.content)


async def test_get_forecast_empty_city(mcp_client):
    """빈 도시 이름 에러 테스트."""
    result = await mcp_client.call_tool(
        "get_forecast", {"city": "", "days": 3}, raise_on_error=False
    )

    assert result.is_error is True
    assert "도시 이름을 입력해주세요" in str(result.content)
