"""SQLite database for chat history storage."""

import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import ChatMessage, ChatSession


class ChatDatabase:
    """SQLite 기반 채팅 기록 데이터베이스."""

    def __init__(self, db_path: str = "./chat_history.db") -> None:
        """데이터베이스 초기화."""
        self.db_path = Path(db_path)
        self.connection: sqlite3.Connection | None = None
        self._init_db()

    def _init_db(self) -> None:
        """데이터베이스 테이블 생성."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                message_count INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)

        conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        """데이터베이스 연결 가져오기."""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def create_session(self, title: str = "New Conversation") -> ChatSession:
        """새 채팅 세션 생성."""
        conn = self._get_connection()
        cursor = conn.cursor()

        session_id = str(uuid.uuid4())
        now = datetime.now()

        cursor.execute(
            "INSERT INTO sessions (session_id, title, created_at, updated_at, message_count) VALUES (?, ?, ?, ?, 0)",
            (session_id, title, now, now),
        )
        conn.commit()

        return ChatSession(
            session_id=session_id,
            title=title,
            created_at=now,
            updated_at=now,
            message_count=0,
        )

    def get_session(self, session_id: str) -> ChatSession | None:
        """세션 조회."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return ChatSession(
            session_id=row["session_id"],
            title=row["title"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            message_count=row["message_count"],
        )

    def list_sessions(self, limit: int = 50) -> list[ChatSession]:
        """세션 목록 조회."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sessions ORDER BY updated_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()

        return [
            ChatSession(
                session_id=row["session_id"],
                title=row["title"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                message_count=row["message_count"],
            )
            for row in rows
        ]

    def add_message(self, session_id: str, message: ChatMessage) -> None:
        """메시지 추가."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, message.role, message.content, message.timestamp),
        )

        cursor.execute(
            "UPDATE sessions SET updated_at = ?, message_count = message_count + 1 WHERE session_id = ?",
            (datetime.now(), session_id),
        )

        conn.commit()

    def get_messages(self, session_id: str, limit: int = 100) -> list[ChatMessage]:
        """세션의 메시지 조회."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC LIMIT ?",
            (session_id, limit),
        )
        rows = cursor.fetchall()

        return [
            ChatMessage(
                role=row["role"],
                content=row["content"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                session_id=row["session_id"],
            )
            for row in rows
        ]

    def delete_session(self, session_id: str) -> None:
        """세션 삭제."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))

        conn.commit()

    def close(self) -> None:
        """데이터베이스 연결 종료."""
        if self.connection:
            self.connection.close()
            self.connection = None
