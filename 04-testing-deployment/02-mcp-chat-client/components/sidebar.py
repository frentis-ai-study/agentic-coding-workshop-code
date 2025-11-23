"""사이드바 컴포넌트.

일관된 사이드바 UI를 제공하는 재사용 가능한 컴포넌트
"""

from typing import Any

import streamlit as st

from backend import ChatDatabase, settings


def render_api_info() -> None:
    """API 설정 정보를 표시합니다."""
    st.header("⚙️ API 설정")

    st.info(f"**Base:** `{settings.openai_api_base}`")
    st.info(f"**Model:** `{settings.model_name}`")

    if settings.is_ollama:
        st.success("✅ Ollama (무료)")
    else:
        st.warning("⚠️ OpenAI (유료)")


def render_session_info(db: ChatDatabase) -> None:
    """현재 세션 정보를 표시합니다.

    Args:
        db: 데이터베이스 인스턴스
    """
    st.header("📝 현재 세션")

    if "session_id" not in st.session_state:
        st.warning("세션이 초기화되지 않았습니다.")
        return

    current_session = db.get_session(st.session_state.session_id)

    if current_session:
        col1, col2 = st.columns(2)

        with col1:
            st.metric("세션 ID", current_session.session_id[:8] + "...")

        with col2:
            st.metric("메시지 수", current_session.message_count)

        st.text(f"생성: {current_session.created_at.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.error("세션을 찾을 수 없습니다.")


def render_usage_guide() -> None:
    """사용 방법 가이드를 표시합니다."""
    st.header("💡 사용 방법")

    st.markdown(
        """
**1단계: MCP 서버 실행**
```bash
cd 03-mcp-tools/02-tools
uv run python server.py
```

**2단계: 채팅**
- 메시지 입력창에 질문 입력
- MCP 도구가 자동으로 호출됨

**예시 메시지:**
- "5 + 3을 계산해줘"
- "서울 날씨는 어때?"
- "현재 디렉토리 파일 목록"
    """
    )


def render_statistics(db: ChatDatabase) -> None:
    """전체 통계를 표시합니다.

    Args:
        db: 데이터베이스 인스턴스
    """
    st.header("📊 통계")

    all_sessions = db.list_sessions()
    total_messages = sum(session.message_count for session in all_sessions)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("총 세션", len(all_sessions))

    with col2:
        st.metric("총 메시지", total_messages)

    if all_sessions:
        avg_messages = total_messages / len(all_sessions)
        st.metric("평균 메시지/세션", f"{avg_messages:.1f}")


def render_new_chat_button() -> bool:
    """새 대화 시작 버튼을 렌더링합니다.

    Returns:
        버튼이 클릭되었는지 여부
    """
    return st.button("🔄 새 대화 시작", type="primary", use_container_width=True)


def render_reset_button() -> bool:
    """대화 초기화 버튼을 렌더링합니다.

    Returns:
        버튼이 클릭되었는지 여부
    """
    return st.button("🗑️ 대화 초기화", type="secondary", use_container_width=True)


def render_complete_sidebar(db: ChatDatabase, show_stats: bool = False) -> dict[str, Any]:
    """완전한 사이드바를 렌더링합니다.

    Args:
        db: 데이터베이스 인스턴스
        show_stats: 통계 표시 여부

    Returns:
        사이드바 상태 (버튼 클릭 여부 등)
    """
    state = {"new_chat_clicked": False, "reset_clicked": False}

    with st.sidebar:
        # API 정보
        render_api_info()
        st.divider()

        # 세션 정보
        render_session_info(db)
        st.divider()

        # 버튼들
        state["new_chat_clicked"] = render_new_chat_button()
        state["reset_clicked"] = render_reset_button()

        st.divider()

        # 통계 (선택사항)
        if show_stats:
            render_statistics(db)
            st.divider()

        # 사용 가이드
        render_usage_guide()

    return state
