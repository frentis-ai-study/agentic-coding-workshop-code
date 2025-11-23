"""
Tests for RestaurantSearchTool

레스토랑 검색 도구의 테스트입니다.
"""



def test_search_by_name_found(search_tool):
    """이름으로 레스토랑 검색 - 성공"""

    result = search_tool.search_by_name("La Trattoria")

    assert result is not None
    assert result["name"] == "La Trattoria"
    assert result["category"] == "이탈리안"
    assert result["hours"] == "11:00-22:00"
    assert result["phone"] == "02-1234-5678"
    assert result["address"] == "서울 강남구 논현동 123"


def test_search_by_name_not_found(search_tool):
    """이름으로 레스토랑 검색 - 실패 (없는 레스토랑)"""

    result = search_tool.search_by_name("Nonexistent Restaurant")

    assert result is None


def test_search_by_category_italian(search_tool):
    """카테고리로 필터링 - 이탈리안"""

    results = search_tool.search_by_category("이탈리안")

    assert len(results) == 2
    assert all(r["category"] == "이탈리안" for r in results)

    names = [r["name"] for r in results]
    assert "La Trattoria" in names
    assert "Pasta House" in names


def test_search_by_category_korean(search_tool):
    """카테고리로 필터링 - 한식"""

    results = search_tool.search_by_category("한식")

    assert len(results) == 1
    assert results[0]["name"] == "Seoul Grill"
    assert results[0]["category"] == "한식"


def test_search_by_category_not_found(search_tool):
    """카테고리로 필터링 - 없는 카테고리"""

    results = search_tool.search_by_category("멕시칸")

    assert len(results) == 0


def test_get_all(search_tool):
    """전체 레스토랑 조회"""

    results = search_tool.get_all()

    assert len(results) == 3

    names = [r["name"] for r in results]
    assert "La Trattoria" in names
    assert "Pasta House" in names
    assert "Seoul Grill" in names
