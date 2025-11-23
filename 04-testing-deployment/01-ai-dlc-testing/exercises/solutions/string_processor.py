"""
StringProcessor 클래스 구현 (Exercise 1 해답)

TDD Red-Green-Refactor 사이클을 따라 완성된 구현입니다.
"""


class StringProcessor:
    """문자열 처리 유틸리티 클래스"""

    def count_words(self, text: str) -> int:
        """
        문자열의 단어 개수를 반환합니다.

        Args:
            text: 입력 문자열

        Returns:
            단어 개수 (공백으로 구분)

        Examples:
            >>> processor = StringProcessor()
            >>> processor.count_words("hello world")
            2
            >>> processor.count_words("  hello   world  ")
            2
            >>> processor.count_words("")
            0
        """
        if not text:
            return 0

        # 공백으로 분할하고 빈 문자열 제거
        words = text.split()
        return len(words)

    def is_palindrome(self, text: str) -> bool:
        """
        문자열이 회문(palindrome)인지 확인합니다.
        대소문자 및 공백을 무시합니다.

        Args:
            text: 입력 문자열

        Returns:
            회문이면 True, 아니면 False

        Examples:
            >>> processor = StringProcessor()
            >>> processor.is_palindrome("racecar")
            True
            >>> processor.is_palindrome("A man a plan a canal Panama")
            True
            >>> processor.is_palindrome("hello")
            False
        """
        # 공백 제거 및 소문자 변환
        cleaned = "".join(text.split()).lower()

        # 빈 문자열은 회문으로 간주
        if not cleaned:
            return True

        # 앞뒤 비교
        return cleaned == cleaned[::-1]

    def to_title_case(self, text: str) -> str:
        """
        각 단어의 첫 글자를 대문자로 변환합니다.

        Args:
            text: 입력 문자열

        Returns:
            제목 케이스로 변환된 문자열

        Examples:
            >>> processor = StringProcessor()
            >>> processor.to_title_case("hello world")
            'Hello World'
            >>> processor.to_title_case("the quick brown fox")
            'The Quick Brown Fox'
        """
        if not text:
            return ""

        # Python 내장 메서드 사용
        return text.title()

    def char_frequency(self, text: str) -> dict[str, int]:
        """
        각 문자의 출현 빈도를 계산합니다.
        대소문자를 구분하며, 공백은 무시합니다.

        Args:
            text: 입력 문자열

        Returns:
            문자별 출현 빈도 딕셔너리

        Examples:
            >>> processor = StringProcessor()
            >>> processor.char_frequency("hello")
            {'h': 1, 'e': 1, 'l': 2, 'o': 1}
            >>> processor.char_frequency("AAbb")
            {'A': 2, 'b': 2}
        """
        frequency: dict[str, int] = {}

        for char in text:
            # 공백 무시
            if char == " ":
                continue

            # 빈도 카운트
            frequency[char] = frequency.get(char, 0) + 1

        return frequency
