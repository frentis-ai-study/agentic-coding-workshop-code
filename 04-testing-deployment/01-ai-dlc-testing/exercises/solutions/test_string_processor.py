"""
StringProcessor 테스트 코드 (Exercise 1 해답)

TDD 방식으로 작성된 포괄적인 테스트 스위트입니다.
"""

import pytest
from string_processor import StringProcessor


class TestStringProcessor:
    """StringProcessor 클래스 테스트"""

    @pytest.fixture
    def processor(self):
        """각 테스트마다 새로운 StringProcessor 인스턴스 생성"""
        return StringProcessor()

    # === count_words 테스트 ===

    def test_count_words_basic(self, processor):
        """기본 단어 개수 테스트"""
        assert processor.count_words("hello world") == 2

    def test_count_words_with_extra_spaces(self, processor):
        """여러 공백이 포함된 경우"""
        assert processor.count_words("  hello   world  ") == 2

    def test_count_words_empty_string(self, processor):
        """빈 문자열 처리"""
        assert processor.count_words("") == 0

    def test_count_words_single_word(self, processor):
        """단일 단어"""
        assert processor.count_words("hello") == 1

    def test_count_words_many_words(self, processor):
        """여러 단어"""
        assert processor.count_words("the quick brown fox jumps") == 5

    # === is_palindrome 테스트 ===

    def test_is_palindrome_simple(self, processor):
        """간단한 회문"""
        assert processor.is_palindrome("racecar") is True

    def test_is_palindrome_with_spaces(self, processor):
        """공백이 포함된 회문"""
        assert processor.is_palindrome("A man a plan a canal Panama") is True

    def test_is_palindrome_not_palindrome(self, processor):
        """회문이 아닌 경우"""
        assert processor.is_palindrome("hello") is False

    def test_is_palindrome_case_insensitive(self, processor):
        """대소문자 무시"""
        assert processor.is_palindrome("RaceCar") is True

    def test_is_palindrome_empty_string(self, processor):
        """빈 문자열 (회문으로 간주)"""
        assert processor.is_palindrome("") is True

    def test_is_palindrome_single_char(self, processor):
        """단일 문자 (항상 회문)"""
        assert processor.is_palindrome("a") is True

    # === to_title_case 테스트 ===

    def test_to_title_case_basic(self, processor):
        """기본 제목 케이스 변환"""
        assert processor.to_title_case("hello world") == "Hello World"

    def test_to_title_case_multiple_words(self, processor):
        """여러 단어"""
        assert processor.to_title_case("the quick brown fox") == "The Quick Brown Fox"

    def test_to_title_case_already_titled(self, processor):
        """이미 제목 케이스인 경우"""
        assert processor.to_title_case("Hello World") == "Hello World"

    def test_to_title_case_all_caps(self, processor):
        """모두 대문자인 경우"""
        assert processor.to_title_case("HELLO WORLD") == "Hello World"

    def test_to_title_case_empty_string(self, processor):
        """빈 문자열"""
        assert processor.to_title_case("") == ""

    # === char_frequency 테스트 ===

    def test_char_frequency_basic(self, processor):
        """기본 문자 빈도"""
        result = processor.char_frequency("hello")
        assert result == {"h": 1, "e": 1, "l": 2, "o": 1}

    def test_char_frequency_case_sensitive(self, processor):
        """대소문자 구분"""
        result = processor.char_frequency("AAbb")
        assert result == {"A": 2, "b": 2}

    def test_char_frequency_with_spaces(self, processor):
        """공백 무시"""
        result = processor.char_frequency("h e l l o")
        assert result == {"h": 1, "e": 1, "l": 2, "o": 1}

    def test_char_frequency_empty_string(self, processor):
        """빈 문자열"""
        result = processor.char_frequency("")
        assert result == {}

    def test_char_frequency_single_char(self, processor):
        """단일 문자"""
        result = processor.char_frequency("a")
        assert result == {"a": 1}

    # === Parametrize 활용 (보너스) ===

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("", 0),
            ("hello", 1),
            ("hello world", 2),
            ("  multiple   spaces  ", 2),
            ("one two three four five", 5),
        ],
    )
    def test_count_words_parametrized(self, processor, text, expected):
        """파라미터화된 단어 개수 테스트"""
        assert processor.count_words(text) == expected

    @pytest.mark.parametrize(
        "text,is_palindrome",
        [
            ("racecar", True),
            ("hello", False),
            ("A man a plan a canal Panama", True),
            ("Was it a car or a cat I saw", True),
            ("Not a palindrome", False),
            ("", True),
        ],
    )
    def test_is_palindrome_parametrized(self, processor, text, is_palindrome):
        """파라미터화된 회문 테스트"""
        assert processor.is_palindrome(text) == is_palindrome
