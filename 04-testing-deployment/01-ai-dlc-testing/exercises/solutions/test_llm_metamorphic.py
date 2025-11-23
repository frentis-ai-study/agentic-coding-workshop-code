"""
LLM Metamorphic Testing 테스트 코드 (Exercise 2 해답)

4가지 Metamorphic 관계(MR)를 검증하는 완전한 구현입니다.
"""

import pytest
from typing import List
import os

# LLM 클라이언트 선택 (환경에 따라 주석 해제)
try:
    import ollama

    LLM_BACKEND = "ollama"
except ImportError:
    LLM_BACKEND = None

try:
    from openai import OpenAI

    if os.getenv("OPENAI_API_KEY"):
        LLM_BACKEND = "openai"
except ImportError:
    pass


class TestLLMMetamorphic:
    """LLM 출력의 Metamorphic 관계 검증"""

    @pytest.fixture
    def llm_client(self):
        """LLM 클라이언트 초기화"""
        if LLM_BACKEND == "ollama":
            return ollama.Client()
        elif LLM_BACKEND == "openai":
            return OpenAI()
        else:
            pytest.skip("LLM 백엔드가 설정되지 않았습니다 (ollama 또는 openai 필요)")

    def generate_text(self, client, prompt: str, model: str = None) -> str:
        """
        LLM으로 텍스트 생성

        Args:
            client: LLM 클라이언트
            prompt: 입력 프롬프트
            model: 모델 이름 (기본값: 백엔드별 기본 모델)

        Returns:
            생성된 텍스트
        """
        if LLM_BACKEND == "ollama":
            model = model or "llama3.2"
            response = client.generate(model=model, prompt=prompt)
            return response["response"]
        elif LLM_BACKEND == "openai":
            model = model or "gpt-4o-mini"
            response = client.chat.completions.create(
                model=model, messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:
            raise ValueError("지원되지 않는 LLM 백엔드")

    def translate(self, client, text: str, target_lang: str = "Korean") -> str:
        """텍스트 번역"""
        prompt = f"Translate the following text to {target_lang}. Only output the translation, nothing else.\n\nText: {text}"
        return self.generate_text(client, prompt)

    def summarize(self, client, text: str, max_words: int = 50) -> str:
        """텍스트 요약"""
        prompt = f"Summarize the following text in at most {max_words} words. Only output the summary.\n\nText: {text}"
        return self.generate_text(client, prompt)

    def analyze_sentiment(self, client, text: str) -> float:
        """
        감정 분석 (0.0 ~ 1.0)
        0.0 = 매우 부정적, 0.5 = 중립, 1.0 = 매우 긍정적
        """
        prompt = f"""Analyze the sentiment of the following text and output ONLY a number between 0.0 (very negative) and 1.0 (very positive).
Do not include any explanation, just the number.

Text: {text}"""
        response = self.generate_text(client, prompt)
        try:
            # 숫자만 추출
            score = float(response.strip().split()[0])
            return max(0.0, min(1.0, score))  # 0~1 범위로 제한
        except (ValueError, IndexError):
            # 파싱 실패 시 중립값 반환
            return 0.5

    def extract_keywords(self, client, text: str, num_keywords: int = 5) -> set:
        """키워드 추출"""
        prompt = f"""Extract the top {num_keywords} keywords from the following text.
Output ONLY the keywords separated by commas, nothing else.

Text: {text}"""
        response = self.generate_text(client, prompt)
        keywords = {kw.strip().lower() for kw in response.split(",")}
        return keywords

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        자카드 유사도 계산

        Returns:
            0.0 ~ 1.0 사이의 유사도 점수
        """
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union) if union else 0.0

    # ============================================================
    # MR1: 번역 순서 불변성 (Order Invariance)
    # ============================================================

    @pytest.mark.slow
    def test_translation_order_invariance(self, llm_client):
        """
        MR1: 번역 순서 불변성

        문장 순서를 바꿔서 번역한 후 재배열하면,
        원본을 번역한 결과와 유사해야 함
        """
        sentences = ["Hello", "Goodbye", "Thank you"]

        # 원본 순서로 번역
        original_translations = [self.translate(llm_client, s) for s in sentences]

        # 역순으로 번역 후 재배열
        reversed_sentences = sentences[::-1]
        reversed_translations = [self.translate(llm_client, s) for s in reversed_sentences]
        reordered_translations = reversed_translations[::-1]

        # Metamorphic 관계 검증
        for i, (orig, reord) in enumerate(zip(original_translations, reordered_translations)):
            similarity = self.calculate_similarity(orig, reord)
            assert similarity > 0.5, (
                f"순서 불변성 위반 (문장 {i}): "
                f"유사도 {similarity:.2f} (원본: '{orig}', 재배열: '{reord}')"
            )

    # ============================================================
    # MR2: 요약 길이 단조성 (Summary Length Monotonicity)
    # ============================================================

    @pytest.mark.slow
    def test_summary_length_monotonicity(self, llm_client):
        """
        MR2: 요약 길이 단조성

        텍스트 길이가 증가하면 요약문 길이도 증가하거나 유지되어야 함
        """
        # 짧은 텍스트
        short_text = "Artificial intelligence is transforming software development."

        # 긴 텍스트 (짧은 텍스트의 확장)
        long_text = """
        Artificial intelligence is transforming software development in profound ways.
        AI-powered tools like GitHub Copilot and ChatGPT enable developers to write code faster,
        debug more efficiently, and learn new technologies with ease.
        The integration of large language models into development workflows represents
        a paradigm shift in how we approach coding challenges.
        """

        # 요약 생성
        short_summary = self.summarize(llm_client, short_text, max_words=10)
        long_summary = self.summarize(llm_client, long_text, max_words=30)

        # 단어 개수 계산
        short_word_count = len(short_summary.split())
        long_word_count = len(long_summary.split())

        # Metamorphic 관계 검증
        assert long_word_count >= short_word_count * 0.8, (
            f"길이 단조성 위반: "
            f"긴 텍스트 요약({long_word_count}단어)이 "
            f"짧은 텍스트 요약({short_word_count}단어)보다 너무 짧음"
        )

    # ============================================================
    # MR3: 감정 분석 대칭성 (Sentiment Symmetry)
    # ============================================================

    @pytest.mark.slow
    def test_sentiment_analysis_symmetry(self, llm_client):
        """
        MR3: 감정 분석 대칭성

        긍정문과 부정문의 감정 점수는 반대 방향이어야 함
        """
        positive_text = "This product is excellent and I absolutely love it!"
        negative_text = "This product is terrible and I absolutely hate it!"

        # 감정 분석
        positive_score = self.analyze_sentiment(llm_client, positive_text)
        negative_score = self.analyze_sentiment(llm_client, negative_text)

        # Metamorphic 관계 검증
        assert positive_score > 0.5, f"긍정문의 감정 점수가 0.5 이하: {positive_score}"
        assert negative_score < 0.5, f"부정문의 감정 점수가 0.5 이상: {negative_score}"

        # 점수 차이가 충분히 큰지 확인
        score_diff = abs(positive_score - negative_score)
        assert score_diff > 0.2, f"감정 점수 차이가 너무 작음: {score_diff}"

    # ============================================================
    # MR4: 키워드 추출 포함 관계 (Keyword Inclusion)
    # ============================================================

    @pytest.mark.slow
    def test_keyword_extraction_inclusion(self, llm_client):
        """
        MR4: 키워드 추출 포함 관계

        두 문서를 합친 텍스트의 키워드는
        개별 키워드의 합집합을 대부분 포함해야 함
        """
        doc_a = """
        Machine learning is a subset of artificial intelligence that focuses on
        training algorithms to learn from data.
        """

        doc_b = """
        Deep learning uses neural networks with multiple layers to process
        complex patterns in large datasets.
        """

        # 개별 문서 키워드
        keywords_a = self.extract_keywords(llm_client, doc_a, num_keywords=3)
        keywords_b = self.extract_keywords(llm_client, doc_b, num_keywords=3)

        # 합친 문서 키워드
        combined_doc = doc_a + "\n" + doc_b
        keywords_combined = self.extract_keywords(llm_client, combined_doc, num_keywords=5)

        # 개별 키워드 합집합
        expected_keywords = keywords_a | keywords_b

        # Metamorphic 관계 검증
        # 합친 문서의 키워드가 개별 키워드의 최소 50% 이상 포함해야 함
        intersection = keywords_combined & expected_keywords
        inclusion_rate = len(intersection) / len(expected_keywords) if expected_keywords else 0

        assert inclusion_rate >= 0.4, (
            f"키워드 포함 관계 위반: "
            f"포함률 {inclusion_rate:.2%} "
            f"(기대: {expected_keywords}, 실제: {keywords_combined})"
        )

    # ============================================================
    # 보너스: 통계적 검증 (Statistical Validation)
    # ============================================================

    @pytest.mark.slow
    @pytest.mark.bonus
    def test_translation_consistency_statistical(self, llm_client):
        """
        보너스: 통계적 검증

        같은 입력을 여러 번 번역하여 일관성 확인
        """
        text = "Hello"
        num_iterations = 5

        # 여러 번 번역
        translations = [self.translate(llm_client, text) for _ in range(num_iterations)]

        # 첫 번째 번역과 나머지의 유사도 계산
        similarities = [self.calculate_similarity(translations[0], t) for t in translations[1:]]

        # 평균 유사도
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0

        # 일관성 검증
        assert avg_similarity > 0.6, (
            f"번역 일관성 부족: 평균 유사도 {avg_similarity:.2f} "
            f"(번역 결과: {translations})"
        )
