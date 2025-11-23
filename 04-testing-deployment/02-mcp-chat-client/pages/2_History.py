"""MCP Chat Client - 대화 기록 페이지.

저장된 모든 세션과 메시지를 조회하고 관리합니다.
"""

import streamlit as st

from backend import ChatDatabase, settings

# 페이지 설정
st.set_page_config(
    page_title=f"History - {settings.page_title}",
    page_icon="📚",
    layout="wide",
)


# 데이터베이스 초기화
@st.cache_resource
def get_database() -> ChatDatabase:
    """데이터베이스 인스턴스 가져오기 (캐시됨)."""
    return ChatDatabase()


db = get_database()

# 타이틀
st.title("📚 대화 기록")
st.caption("저장된 모든 세션과 메시지를 조회합니다")

# 사이드바: 필터 및 정렬
with st.sidebar:
    st.header("🔍 필터 및 정렬")

    sort_order = st.selectbox(
        "정렬 순서",
        options=["최신순", "오래된 순", "메시지 많은 순"],
        index=0,
    )

    show_limit = st.slider("표시할 세션 수", min_value=5, max_value=100, value=20, step=5)

    st.divider()

    # 통계
    st.subheader("📊 통계")
    all_sessions = db.list_sessions()
    total_messages = sum(session.message_count for session in all_sessions)

    st.metric("전체 세션 수", len(all_sessions))
    st.metric("전체 메시지 수", total_messages)

    if all_sessions:
        avg_messages = total_messages / len(all_sessions)
        st.metric("평균 메시지 수", f"{avg_messages:.1f}")


# 세션 목록 가져오기
sessions = db.list_sessions()

# 정렬 적용
if sort_order == "최신순":
    sessions = sorted(sessions, key=lambda s: s.created_at, reverse=True)
elif sort_order == "오래된 순":
    sessions = sorted(sessions, key=lambda s: s.created_at)
elif sort_order == "메시지 많은 순":
    sessions = sorted(sessions, key=lambda s: s.message_count, reverse=True)

# 제한 적용
sessions = sessions[:show_limit]

# 세션이 없는 경우
if not sessions:
    st.info("아직 저장된 대화가 없습니다. 채팅 페이지에서 대화를 시작하세요!")
    st.page_link("pages/1_Chat.py", label="➡️ 채팅 페이지로 이동", icon="💬")
    st.stop()

# 세션 목록 표시
st.subheader(f"📋 세션 목록 ({len(sessions)}개)")

for idx, session in enumerate(sessions, start=1):
    with st.expander(
        f"**{idx}. {session.title}** ({session.message_count}개 메시지) - {session.created_at.strftime('%Y-%m-%d %H:%M')}",
        expanded=(idx == 1),  # 첫 번째만 기본 확장
    ):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.text(f"세션 ID: {session.session_id}")

        with col2:
            st.text(f"생성일: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

        with col3:
            # 삭제 버튼
            if st.button("🗑️ 삭제", key=f"delete_{session.session_id}"):
                db.delete_session(session.session_id)
                st.success(f"세션 삭제됨: {session.session_id[:8]}...")
                st.rerun()

        st.divider()

        # 메시지 표시
        messages = db.get_messages(session.session_id)

        if not messages:
            st.info("이 세션에는 메시지가 없습니다.")
        else:
            for msg_idx, msg in enumerate(messages, start=1):
                role_icon = "👤" if msg.role == "user" else "🤖"
                role_color = "#1f77b4" if msg.role == "user" else "#ff7f0e"

                st.markdown(
                    f"""
                    <div style="border-left: 3px solid {role_color}; padding-left: 10px; margin-bottom: 10px;">
                        <strong>{role_icon} {msg.role.capitalize()}</strong>
                        <small style="color: gray;"> ({msg.timestamp.strftime('%H:%M:%S')})</small>
                        <p>{msg.content}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # 이 세션 불러오기 버튼
        st.divider()
        if st.button("📂 이 세션 불러오기", key=f"load_{session.session_id}"):
            # 세션 상태에 저장
            st.session_state.session_id = session.session_id
            st.session_state.messages = [
                {"role": msg.role, "content": msg.content} for msg in messages
            ]
            st.success(f"세션 불러옴: {session.session_id[:8]}...")
            st.info("채팅 페이지로 이동하여 대화를 이어가세요.")
            st.page_link("pages/1_Chat.py", label="➡️ 채팅 페이지로 이동", icon="💬")

# 하단 안내
st.divider()
st.caption(
    """
💡 **Tip:** 세션을 불러온 후 채팅 페이지에서 이어서 대화할 수 있습니다.
"""
)
