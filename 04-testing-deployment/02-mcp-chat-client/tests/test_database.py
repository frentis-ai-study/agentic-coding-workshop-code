"""Database tests for MCP Chat Client."""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from backend import ChatDatabase, ChatMessage, ChatSession


@pytest.fixture
def temp_db():
    """임시 데이터베이스를 생성합니다."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    # 임시 DB 경로로 초기화
    db = ChatDatabase(db_path=db_path)

    yield db

    # 정리
    db.close()
    Path(db_path).unlink(missing_ok=True)


class TestChatDatabase:
    """ChatDatabase 클래스 테스트."""

    def test_create_session(self, temp_db):
        """세션 생성 테스트."""
        session = temp_db.create_session(title="Test Session")

        assert session is not None
        assert session.session_id is not None
        assert session.title == "Test Session"
        assert session.message_count == 0
        assert isinstance(session.created_at, datetime)

    def test_get_session(self, temp_db):
        """세션 조회 테스트."""
        # 세션 생성
        created_session = temp_db.create_session(title="Test Session")

        # 조회
        retrieved_session = temp_db.get_session(created_session.session_id)

        assert retrieved_session is not None
        assert retrieved_session.session_id == created_session.session_id
        assert retrieved_session.title == created_session.title

    def test_get_nonexistent_session(self, temp_db):
        """존재하지 않는 세션 조회 테스트."""
        session = temp_db.get_session("nonexistent-id")
        assert session is None

    def test_list_sessions(self, temp_db):
        """세션 목록 조회 테스트."""
        # 여러 세션 생성
        temp_db.create_session(title="Session 1")
        temp_db.create_session(title="Session 2")
        temp_db.create_session(title="Session 3")

        # 목록 조회
        sessions = temp_db.list_sessions()

        assert len(sessions) == 3
        assert all(isinstance(s, ChatSession) for s in sessions)

    def test_add_message(self, temp_db):
        """메시지 추가 테스트."""
        # 세션 생성
        session = temp_db.create_session(title="Test Session")

        # 메시지 추가
        message = ChatMessage(
            role="user",
            content="Hello, world!",
            session_id=session.session_id,
        )
        temp_db.add_message(session.session_id, message)

        # 메시지 조회
        messages = temp_db.get_messages(session.session_id)

        assert len(messages) == 1
        assert messages[0].role == "user"
        assert messages[0].content == "Hello, world!"

    def test_get_messages(self, temp_db):
        """메시지 목록 조회 테스트."""
        # 세션 생성
        session = temp_db.create_session(title="Test Session")

        # 여러 메시지 추가
        temp_db.add_message(
            session.session_id,
            ChatMessage(role="user", content="Message 1", session_id=session.session_id),
        )
        temp_db.add_message(
            session.session_id,
            ChatMessage(role="assistant", content="Message 2", session_id=session.session_id),
        )
        temp_db.add_message(
            session.session_id,
            ChatMessage(role="user", content="Message 3", session_id=session.session_id),
        )

        # 조회
        messages = temp_db.get_messages(session.session_id)

        assert len(messages) == 3
        assert messages[0].content == "Message 1"
        assert messages[1].content == "Message 2"
        assert messages[2].content == "Message 3"

    def test_delete_session(self, temp_db):
        """세션 삭제 테스트."""
        # 세션 생성
        session = temp_db.create_session(title="Test Session")

        # 메시지 추가
        temp_db.add_message(
            session.session_id,
            ChatMessage(role="user", content="Test", session_id=session.session_id),
        )

        # 삭제
        temp_db.delete_session(session.session_id)

        # 삭제 확인
        deleted_session = temp_db.get_session(session.session_id)
        assert deleted_session is None

        # 메시지도 삭제되었는지 확인
        messages = temp_db.get_messages(session.session_id)
        assert len(messages) == 0

    def test_message_count_update(self, temp_db):
        """메시지 카운트 업데이트 테스트."""
        # 세션 생성
        session = temp_db.create_session(title="Test Session")

        # 초기 카운트 확인
        assert session.message_count == 0

        # 메시지 추가
        temp_db.add_message(
            session.session_id,
            ChatMessage(role="user", content="Test", session_id=session.session_id),
        )

        # 카운트 업데이트 확인
        updated_session = temp_db.get_session(session.session_id)
        assert updated_session.message_count == 1

    def test_message_timestamp(self, temp_db):
        """메시지 타임스탬프 테스트."""
        # 세션 생성
        session = temp_db.create_session(title="Test Session")

        # 메시지 추가
        message = ChatMessage(role="user", content="Test", session_id=session.session_id)
        temp_db.add_message(session.session_id, message)

        # 조회
        messages = temp_db.get_messages(session.session_id)

        assert len(messages) == 1
        assert isinstance(messages[0].timestamp, datetime)

    def test_session_ordering(self, temp_db):
        """세션 정렬 테스트 (최신순)."""
        import time

        # 시간차를 두고 세션 생성
        session1 = temp_db.create_session(title="Session 1")
        time.sleep(0.1)
        session2 = temp_db.create_session(title="Session 2")
        time.sleep(0.1)
        session3 = temp_db.create_session(title="Session 3")

        # 목록 조회 (최신순)
        sessions = temp_db.list_sessions()

        # 세션 3이 가장 먼저 와야 함
        assert sessions[0].session_id == session3.session_id
        assert sessions[1].session_id == session2.session_id
        assert sessions[2].session_id == session1.session_id
