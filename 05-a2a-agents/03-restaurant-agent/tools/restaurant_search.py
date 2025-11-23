"""
Restaurant Search Tool

레스토랑 정보를 검색하는 도구입니다.
JSON 파일 기반으로 간단하게 구현되었으며, 확장 가능한 구조입니다.
"""

import json
from pathlib import Path


class RestaurantSearchTool:
    """레스토랑 정보 검색 도구 (JSON 기반, 확장 가능)"""

    def __init__(self, data_path: str | None = None):
        """
        Args:
            data_path: restaurants.json 파일 경로 (None이면 기본 경로 사용)
        """
        if data_path is None:
            # 기본 경로: tools/ 디렉토리 기준 ../data/restaurants.json
            current_dir = Path(__file__).parent
            data_path = current_dir.parent / "data" / "restaurants.json"

        with open(data_path, encoding="utf-8") as f:
            self.data: dict = json.load(f)

    def search_by_name(self, name: str) -> dict | None:
        """
        이름으로 레스토랑 검색

        Args:
            name: 레스토랑 이름

        Returns:
            레스토랑 정보 dict 또는 None (없는 경우)

        Example:
            >>> tool = RestaurantSearchTool()
            >>> info = tool.search_by_name("La Trattoria")
            >>> print(info["category"])
            이탈리안
        """
        return self.data.get(name)

    def search_by_category(self, category: str) -> list[dict]:
        """
        카테고리로 레스토랑 필터링

        Args:
            category: 카테고리 (이탈리안, 한식, 일식, 중식, 양식)

        Returns:
            해당 카테고리의 레스토랑 목록

        Example:
            >>> tool = RestaurantSearchTool()
            >>> italian = tool.search_by_category("이탈리안")
            >>> len(italian)
            2
        """
        return [
            restaurant
            for restaurant in self.data.values()
            if restaurant["category"] == category
        ]

    def get_all(self) -> list[dict]:
        """
        모든 레스토랑 조회

        Returns:
            전체 레스토랑 목록

        Example:
            >>> tool = RestaurantSearchTool()
            >>> all_restaurants = tool.get_all()
            >>> len(all_restaurants)
            10
        """
        return list(self.data.values())
