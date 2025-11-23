"""채팅 메시지 컴포넌트.

채팅 메시지를 일관된 형식으로 표시하는 재사용 가능한 컴포넌트
"""

from datetime import datetime
from typing import Literal

import streamlit as st


def render_chat_message(
    role: Literal["user", "assistant", "system"],
    content: str,
    timestamp: datetime | None = None,
    show_timestamp: bool = True,
    markdown: bool = True,
) -> None:
    """채팅 메시지를 렌더링합니다.

    Args:
        role: 메시지 역할 (user, assistant, system)
        content: 메시지 내용
        timestamp: 메시지 타임스탬프 (None이면 현재 시간)
        show_timestamp: 타임스탬프 표시 여부
        markdown: 마크다운 렌더링 여부
    """
    # 아이콘 및 색상 설정
    role_config = {
        "user": {"icon": "👤", "color": "#1f77b4", "name": "User"},
        "assistant": {"icon": "🤖", "color": "#ff7f0e", "name": "Assistant"},
        "system": {"icon": "⚙️", "color": "#2ca02c", "name": "System"},
    }

    config = role_config.get(role, role_config["system"])

    # 타임스탬프 포맷
    if timestamp is None:
        timestamp = datetime.now()

    time_str = timestamp.strftime("%H:%M:%S")

    # 메시지 렌더링
    with st.chat_message(role):
        # 헤더 (역할 + 타임스탬프)
        if show_timestamp:
            st.caption(f"{config['icon']} **{config['name']}** • {time_str}")

        # 내용
        if markdown:
            st.markdown(content)
        else:
            st.text(content)


def render_message_with_border(
    role: Literal["user", "assistant", "system"],
    content: str,
    timestamp: datetime | None = None,
) -> None:
    """테두리가 있는 메시지를 렌더링합니다.

    대화 기록 페이지에서 사용하기 적합합니다.

    Args:
        role: 메시지 역할
        content: 메시지 내용
        timestamp: 메시지 타임스탬프
    """
    # 아이콘 및 색상 설정
    role_config = {
        "user": {"icon": "👤", "color": "#1f77b4", "name": "User"},
        "assistant": {"icon": "🤖", "color": "#ff7f0e", "name": "Assistant"},
        "system": {"icon": "⚙️", "color": "#2ca02c", "name": "System"},
    }

    config = role_config.get(role, role_config["system"])

    # 타임스탬프 포맷
    if timestamp is None:
        timestamp = datetime.now()

    time_str = timestamp.strftime("%H:%M:%S")

    # HTML로 렌더링
    st.markdown(
        f"""
        <div style="
            border-left: 3px solid {config['color']};
            padding-left: 10px;
            margin-bottom: 10px;
            background-color: rgba(0, 0, 0, 0.05);
            border-radius: 5px;
            padding: 10px;
        ">
            <strong>{config['icon']} {config['name']}</strong>
            <small style="color: gray;"> ({time_str})</small>
            <p style="margin-top: 5px;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_typing_indicator() -> None:
    """타이핑 중 표시 애니메이션."""
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="
                width: 8px;
                height: 8px;
                background-color: #888;
                border-radius: 50%;
                animation: typing 1.4s infinite both;
            "></div>
            <div style="
                width: 8px;
                height: 8px;
                background-color: #888;
                border-radius: 50%;
                animation: typing 1.4s infinite both;
                animation-delay: 0.2s;
            "></div>
            <div style="
                width: 8px;
                height: 8px;
                background-color: #888;
                border-radius: 50%;
                animation: typing 1.4s infinite both;
                animation-delay: 0.4s;
            "></div>
        </div>

        <style>
        @keyframes typing {
            0%, 60%, 100% {
                opacity: 0.3;
                transform: translateY(0);
            }
            30% {
                opacity: 1;
                transform: translateY(-10px);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
