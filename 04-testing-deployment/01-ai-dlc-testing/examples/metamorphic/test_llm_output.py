"""Metamorphic Testing for LLM Outputs.

LLM 생성 코드의 출력 일관성을 검증하는 테스트입니다.
"""

import pytest

from metamorphic_relations import (
    AdditiveMonotonicity,
    EquivalenceRelation,
    NegationInversion,
    ParaphraseConsistency,
    PermutationInvariance,
)


# 간단한 LLM 시뮬레이터 (실제로는 OpenAI API 등 사용)
def simple_calculator(query: str) -> str:
    """간단한 계산기 함수 (LLM 대신 사용)."""
    query = query.lower().replace("계산해줘:", "").replace("계산하세요:", "").strip()

    # 덧셈
    if "+" in query:
        parts = query.split("+")
        try:
            result = sum(int(p.strip()) for p in parts)
            return str(result)
        except ValueError:
            return "계산 오류"

    # 곱셈
    if "*" in query or "x" in query:
        separator = "*" if "*" in query else "x"
        parts = query.split(separator)
        try:
            result = 1
            for p in parts:
                result *= int(p.strip())
            return str(result)
        except ValueError:
            return "계산 오류"

    return "이해할 수 없는 쿼리"


def is_even_checker(query: str) -> bool:
    """숫자가 짝수인지 확인하는 함수."""
    query = query.lower()
    # 숫자 추출
    import re

    numbers = re.findall(r"\d+", query)
    if numbers:
        num = int(numbers[0])
        if "짝수" in query:
            return num % 2 == 0
        elif "홀수" in query:
            return num % 2 != 0
    return False


def text_length_analyzer(query: str) -> str:
    """텍스트 길이를 분석하는 함수 (간단한 응답)."""
    base_response = "이것은 기본 응답입니다."

    if "자세히" in query or "상세히" in query or "더" in query:
        return f"{base_response} 추가적인 상세 설명을 포함합니다. 더 많은 정보를 제공합니다."

    return base_response


# Metamorphic Testing 예제들


def test_permutation_invariance_addition() -> None:
    """순열 불변성 테스트: 덧셈은 순서에 관계없이 동일한 결과."""
    relation = PermutationInvariance()

    # 원본 입력
    original_input = "1 + 2 + 3"
    # 변환된 입력 (순서를 바꾸지만 덧셈이므로 결과는 동일해야 함)
    # 실제로는 "3 + 2 + 1"이지만 계산기는 순서 상관없이 6을 반환
    original_output = simple_calculator(original_input)
    transformed_output = simple_calculator("3 + 2 + 1")

    # 출력이 동일해야 함
    assert relation.verify_outputs(
        original_output, transformed_output
    ), f"Expected same output, got {original_output} vs {transformed_output}"


def test_paraphrase_consistency() -> None:
    """패러프레이즈 일관성 테스트: 유사한 의미의 입력은 유사한 출력."""
    relation = ParaphraseConsistency()

    # 원본 입력
    original_input = "계산해줘: 5 + 5"
    transformed_input = relation.transform_input(original_input)

    original_output = simple_calculator(original_input)
    transformed_output = simple_calculator(transformed_input)

    # 출력이 유사해야 함 (실제로는 같은 "10")
    assert relation.verify_outputs(
        original_output, transformed_output
    ), f"Paraphrase outputs differ: {original_output} vs {transformed_output}"


def test_additive_monotonicity() -> None:
    """가산 단조성 테스트: 추가 정보 요청 시 출력이 더 상세해짐."""
    relation = AdditiveMonotonicity(additional_context="더 자세히 설명해줘")

    original_input = "파이썬이란?"
    transformed_input = relation.transform_input(original_input)

    original_output = text_length_analyzer(original_input)
    transformed_output = text_length_analyzer(transformed_input)

    # 변환된 출력이 더 길어야 함
    assert relation.verify_outputs(
        original_output, transformed_output
    ), f"Expected longer output, got {len(original_output)} vs {len(transformed_output)}"


def test_negation_inversion_even_odd() -> None:
    """부정 반전 테스트: 짝수/홀수 질문의 답변이 반대."""
    relation = NegationInversion()

    # 5는 짝수인가? (False)
    original_input = "5는 짝수인가?"
    transformed_input = relation.transform_input(original_input)  # "5는 홀수인가?"

    original_output = is_even_checker(original_input)
    transformed_output = is_even_checker(transformed_input)

    # 출력이 반대여야 함
    assert relation.verify_outputs(
        original_output, transformed_output
    ), f"Expected inverted outputs, got {original_output} vs {transformed_output}"


def test_equivalence_relation_commutativity() -> None:
    """동등성 관계 테스트: 교환법칙이 성립하는 연산."""
    # "2 + 3"과 "3 + 2"는 동일한 결과
    original_input = "2 + 3"
    equivalent_input = "3 + 2"

    relation = EquivalenceRelation(equivalent_input)
    transformed_input = relation.transform_input(original_input)

    original_output = simple_calculator(original_input)
    transformed_output = simple_calculator(transformed_input)

    # 출력이 완전히 동일해야 함
    assert relation.verify_outputs(
        original_output, transformed_output
    ), f"Expected equal outputs, got {original_output} vs {transformed_output}"


def test_permutation_invariance_with_lists() -> None:
    """순열 불변성 테스트: 리스트 항목 순서 변경."""
    relation = PermutationInvariance()

    # 원본: "apple, banana, cherry"
    original_input = "apple, banana, cherry"
    transformed_input = relation.transform_input(original_input)  # 역순

    # 정렬된 결과를 반환하는 함수라고 가정
    def sorted_list(items: str) -> str:
        parts = [p.strip() for p in items.split(",")]
        return ", ".join(sorted(parts))

    original_output = sorted_list(original_input)
    transformed_output = sorted_list(transformed_input)

    # 정렬된 결과는 동일해야 함
    assert relation.verify_outputs(
        original_output, transformed_output
    ), f"Sorted lists should be equal: {original_output} vs {transformed_output}"


# 실패 케이스 예제 (의도적으로 실패하도록)
@pytest.mark.xfail(reason="This test is designed to fail to demonstrate metamorphic violation")
def test_failing_metamorphic_relation() -> None:
    """실패하는 Metamorphic Relation 테스트 예제."""
    relation = AdditiveMonotonicity()

    # 이 함수는 추가 정보를 무시하고 항상 같은 길이의 답변을 반환
    def stubborn_function(query: str) -> str:
        return "항상 같은 답변"

    original_input = "질문"
    transformed_input = relation.transform_input(original_input)

    original_output = stubborn_function(original_input)
    transformed_output = stubborn_function(transformed_input)

    # 이 테스트는 실패해야 함 (출력이 동일하므로 가산 단조성 위배)
    assert relation.verify_outputs(original_output, transformed_output)


# 실전 예제: MCP 도구 출력 검증


def test_mcp_tool_metamorphic_consistency() -> None:
    """MCP 도구의 출력 일관성을 Metamorphic Testing으로 검증."""
    # 예시: 계산기 MCP 도구
    def mcp_calculator_tool(expression: str) -> float:
        """MCP 계산기 도구 시뮬레이션."""
        # 실제로는 FastMCP 도구 호출
        return eval(expression)  # 간단한 예시 (실제 프로덕션에서는 사용 금지)

    # 교환법칙 테스트
    relation = EquivalenceRelation("5 * 3")

    original_output = mcp_calculator_tool("3 * 5")
    transformed_output = mcp_calculator_tool("5 * 3")

    assert relation.verify_outputs(
        original_output, transformed_output
    ), "MCP tool should respect commutativity"


if __name__ == "__main__":
    # 개별 테스트 실행
    print("Running Metamorphic Tests...")
    test_permutation_invariance_addition()
    print("✓ Permutation Invariance (Addition)")

    test_paraphrase_consistency()
    print("✓ Paraphrase Consistency")

    test_additive_monotonicity()
    print("✓ Additive Monotonicity")

    test_negation_inversion_even_odd()
    print("✓ Negation Inversion")

    test_equivalence_relation_commutativity()
    print("✓ Equivalence Relation")

    test_permutation_invariance_with_lists()
    print("✓ Permutation Invariance (Lists)")

    test_mcp_tool_metamorphic_consistency()
    print("✓ MCP Tool Consistency")

    print("\nAll metamorphic tests passed! ✨")
