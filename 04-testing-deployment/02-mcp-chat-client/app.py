"""MCP Chat Client - Streamlit 메인 앱.

Streamlit + LangGraph + MCP 통합 채팅 애플리케이션
"""

import asyncio
import os

import streamlit as st

from backend import ChatDatabase, ChatMessage, get_agent, settings

# 페이지 설정
st.set_page_config(
    page_title=settings.page_title,
    page_icon=settings.page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)


# 데이터베이스 초기화
@st.cache_resource
def get_database() -> ChatDatabase:
    """데이터베이스 인스턴스 가져오기 (캐시됨)."""
    return ChatDatabase()


db = get_database()


# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    # 새 세션 생성
    session = db.create_session(title="New Conversation")
    st.session_state.session_id = session.session_id


# 타이틀
st.title(f"{settings.page_icon} MCP Chat Client")
st.caption("Streamlit + LangGraph + Part 3 MCP 서버")

# 사이드바: 설정 정보
with st.sidebar:
    st.header("⚙️ 설정")

    st.info(f"**API Base:** `{settings.openai_api_base}`")
    st.info(f"**Model:** `{settings.model_name}`")

    if settings.is_ollama:
        st.success("✅ Ollama 모드 (무료)")
    else:
        st.warning("⚠️ OpenAI 모드 (유료)")

    st.divider()

    # 세션 정보
    st.subheader("📝 현재 세션")
    current_session = db.get_session(st.session_state.session_id)
    if current_session:
        st.text(f"ID: {current_session.session_id[:8]}...")
        st.text(f"메시지: {current_session.message_count}개")

    st.divider()

    # 사용 방법
    st.subheader("💡 사용 방법")
    st.markdown("""
1. Part 3 MCP 서버 실행
2. 채팅 입력창에 메시지 입력
3. MCP 도구가 자동 호출

**예시 메시지:**
- "5 + 3 계산해줘"
- "서울 날씨 알려줘"
    """)

    st.divider()

    # 초기화 버튼
    if st.button("🔄 대화 초기화", type="secondary"):
        st.session_state.messages = []
        # 새 세션 생성
        session = db.create_session(title="New Conversation")
        st.session_state.session_id = session.session_id
        st.rerun()


# 메시지 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 데이터베이스에 저장
    user_msg = ChatMessage(role="user", content=prompt, session_id=st.session_state.session_id)
    db.add_message(st.session_state.session_id, user_msg)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("🤔 생각 중..."):
            try:
                # 에이전트 가져오기 및 응답 생성
                agent = asyncio.run(get_agent())
                response = asyncio.run(
                    agent.chat(prompt, history=st.session_state.messages[:-1])
                )
            except Exception as e:
                response = f"❌ 오류 발생: {str(e)}\n\n"
                response += "**해결 방법:**\n"
                response += "1. Ollama가 실행 중인지 확인하세요\n"
                response += "2. 환경변수가 올바른지 확인하세요\n"
                response += f"   - OPENAI_API_BASE={settings.openai_api_base}\n"
                response += f"   - OPENAI_API_KEY={settings.openai_api_key}\n"

            st.markdown(response)

    # 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response})

    # 데이터베이스에 저장
    assistant_msg = ChatMessage(
        role="assistant", content=response, session_id=st.session_state.session_id
    )
    db.add_message(st.session_state.session_id, assistant_msg)

# 하단 안내
st.divider()
st.caption("""
💡 **Tip:** 환경변수를 `.env` 파일로 설정할 수 있습니다.
📖 자세한 내용은 [README.md](./README.md) 참조
""")
