"""Metamorphic Relations for LLM Testing.

Metamorphic Testing은 입력 변환 시 출력 간 관계를 검증하여
LLM 생성 코드의 일관성을 확인하는 테스트 기법입니다.
"""

from abc import ABC, abstractmethod
from typing import Any


class MetamorphicRelation(ABC):
    """Metamorphic Relation 추상 클래스."""

    @abstractmethod
    def transform_input(self, original_input: str) -> str:
        """입력을 변환합니다."""
        pass

    @abstractmethod
    def verify_outputs(self, original_output: Any, transformed_output: Any) -> bool:
        """원본 출력과 변환된 출력 간 관계를 검증합니다."""
        pass


class PermutationInvariance(MetamorphicRelation):
    """순열 불변성: 입력 순서를 바꿔도 결과가 동일해야 함.

    예시:
    - "사과, 바나나, 오렌지를 정렬하세요" → 동일한 정렬 결과
    - "1 + 2 + 3" → 6 (덧셈은 순서 무관)
    """

    def transform_input(self, original_input: str) -> str:
        """리스트 항목의 순서를 바꿉니다."""
        # 간단한 예시: 쉼표로 구분된 항목을 역순으로
        if "," in original_input:
            parts = [p.strip() for p in original_input.split(",")]
            return ", ".join(reversed(parts))
        return original_input

    def verify_outputs(self, original_output: Any, transformed_output: Any) -> bool:
        """출력이 동일한지 확인 (정렬된 리스트 등)."""
        # 문자열 비교 (공백 제거)
        if isinstance(original_output, str) and isinstance(transformed_output, str):
            return original_output.strip() == transformed_output.strip()
        return original_output == transformed_output


class ParaphraseConsistency(MetamorphicRelation):
    """패러프레이즈 일관성: 의미가 같은 입력은 유사한 출력을 생성해야 함.

    예시:
    - "날씨가 어때?" vs "오늘 날씨는?"
    - "계산해줘: 5 + 3" vs "5 더하기 3은?"
    """

    def transform_input(self, original_input: str) -> str:
        """간단한 패러프레이징 (실제로는 LLM 사용 가능)."""
        paraphrase_map = {
            "계산해줘": "계산하세요",
            "알려줘": "알려주세요",
            "뭐야": "무엇인가요",
            "어때": "어떤가요",
        }
        transformed = original_input
        for original, paraphrase in paraphrase_map.items():
            transformed = transformed.replace(original, paraphrase)
        return transformed

    def verify_outputs(self, original_output: Any, transformed_output: Any) -> bool:
        """출력의 의미가 유사한지 확인 (간단한 문자열 유사도)."""
        if isinstance(original_output, str) and isinstance(transformed_output, str):
            # 단순 예시: 출력 길이 차이가 20% 이내
            len_original = len(original_output)
            len_transformed = len(transformed_output)
            if len_original == 0 and len_transformed == 0:
                return True
            max_len = max(len_original, len_transformed)
            if max_len == 0:
                return True
            diff_ratio = abs(len_original - len_transformed) / max_len
            return diff_ratio < 0.2
        return False


class AdditiveMonotonicity(MetamorphicRelation):
    """가산 단조성: 추가 정보를 제공하면 출력이 더 상세해져야 함.

    예시:
    - "파이썬이란?" vs "파이썬이란? 역사도 포함해줘"
    - "날씨는?" vs "날씨는? 온도와 습도도 알려줘"
    """

    def __init__(self, additional_context: str = "더 자세히 설명해줘"):
        self.additional_context = additional_context

    def transform_input(self, original_input: str) -> str:
        """원본 입력에 추가 컨텍스트를 붙입니다."""
        return f"{original_input} {self.additional_context}"

    def verify_outputs(self, original_output: Any, transformed_output: Any) -> bool:
        """변환된 출력이 원본보다 더 상세한지 확인 (길이 기준)."""
        if isinstance(original_output, str) and isinstance(transformed_output, str):
            # 변환된 출력이 원본보다 최소 10% 이상 길어야 함
            return len(transformed_output) >= len(original_output) * 1.1
        return False


class NegationInversion(MetamorphicRelation):
    """부정 반전: 질문을 부정형으로 바꾸면 답변도 반대가 되어야 함.

    예시:
    - "5는 짝수인가?" (False) vs "5는 홀수인가?" (True)
    - "파이썬은 컴파일 언어인가?" (False) vs "파이썬은 인터프리터 언어인가?" (True)
    """

    def transform_input(self, original_input: str) -> str:
        """부정형으로 변환 (간단한 예시)."""
        negation_map = {
            "짝수": "홀수",
            "홀수": "짝수",
            "크다": "작다",
            "작다": "크다",
            "있다": "없다",
            "없다": "있다",
        }
        transformed = original_input
        for original, negation in negation_map.items():
            if original in transformed:
                transformed = transformed.replace(original, negation)
                break
        return transformed

    def verify_outputs(self, original_output: Any, transformed_output: Any) -> bool:
        """출력이 반대인지 확인 (불린 값 또는 긍정/부정 답변)."""
        # 불린 타입
        if isinstance(original_output, bool) and isinstance(transformed_output, bool):
            return original_output != transformed_output

        # 문자열 답변 (Yes/No, True/False 등)
        if isinstance(original_output, str) and isinstance(transformed_output, str):
            positive_keywords = ["yes", "true", "참", "맞", "그렇"]
            negative_keywords = ["no", "false", "거짓", "아니", "틀"]

            original_lower = original_output.lower()
            transformed_lower = transformed_output.lower()

            original_positive = any(kw in original_lower for kw in positive_keywords)
            transformed_positive = any(kw in transformed_lower for kw in positive_keywords)

            original_negative = any(kw in original_lower for kw in negative_keywords)
            transformed_negative = any(kw in transformed_lower for kw in negative_keywords)

            # 하나는 긍정, 하나는 부정이어야 함
            return (original_positive and transformed_negative) or (
                original_negative and transformed_positive
            )

        return False


class EquivalenceRelation(MetamorphicRelation):
    """동등성 관계: 동일한 의미의 입력은 동일한 출력을 생성해야 함.

    예시:
    - "2 + 3" vs "3 + 2" (교환법칙)
    - "10 / 2" vs "10 나누기 2"
    """

    def __init__(self, equivalent_input: str):
        self.equivalent_input = equivalent_input

    def transform_input(self, original_input: str) -> str:
        """미리 정의된 동등한 입력을 반환합니다."""
        return self.equivalent_input

    def verify_outputs(self, original_output: Any, transformed_output: Any) -> bool:
        """출력이 완전히 동일한지 확인."""
        return original_output == transformed_output
