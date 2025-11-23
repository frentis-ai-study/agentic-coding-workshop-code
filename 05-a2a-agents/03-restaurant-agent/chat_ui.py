"""Streamlit 채팅 UI

레스토랑 추천 시스템을 위한 웹 기반 채팅 인터페이스
"""

import json
import sys
from pathlib import Path

import httpx
import streamlit as st

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 페이지 설정
st.set_page_config(
    page_title="레스토랑 추천 채팅",
    page_icon="🍽️",
    layout="centered"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "user"

# 타이틀
st.title("🍽️ 레스토랑 추천 에이전트")
st.caption("A2A 기반 레스토랑 추천 및 예약 정보 시스템")

# 사이드바 - 사용자 설정
with st.sidebar:
    st.header("⚙️ 설정")

    # 사용자 ID 입력
    user_id = st.text_input(
        "사용자 ID",
        value=st.session_state.user_id,
        help="각 사용자별로 선호도가 저장됩니다"
    )
    if user_id != st.session_state.user_id:
        st.session_state.user_id = user_id

    # 서버 URL 설정
    recommender_url = st.text_input(
        "추천 서버 URL",
        value="http://localhost:8100",
        help="추천 에이전트 서버 주소"
    )

    booking_url = st.text_input(
        "예약 서버 URL",
        value="http://localhost:8101",
        help="예약 에이전트 서버 주소"
    )

    st.divider()

    # 사용 가이드
    st.subheader("📖 사용 가이드")
    st.markdown("""
    **1. 선호도 저장**
    - "이탈리안 좋아해"
    - "매운 음식 좋아해"

    **2. 레스토랑 추천**
    - "배고파"
    - "레스토랑 추천해줘"

    **3. 예약 정보**
    - "La Trattoria 영업시간"
    - "전화번호 알려줘"
    """)

    st.divider()

    # 서버 상태 확인
    st.subheader("🔌 서버 상태")

    # 추천 서버 상태
    try:
        response = httpx.get(f"{recommender_url}/.well-known/agent-card.json", timeout=2)
        if response.status_code == 200:
            st.success("✅ 추천 서버 (8100)")
            agent_info = response.json()
            st.caption(f"📍 {agent_info.get('name', 'Unknown')}")
        else:
            st.error("❌ 추천 서버 오류")
    except Exception:
        st.error("❌ 추천 서버 (8100) 연결 실패")
        st.caption("서버가 실행 중인지 확인하세요")

    # 예약 서버 상태
    try:
        response = httpx.get(f"{booking_url}/.well-known/agent-card.json", timeout=2)
        if response.status_code == 200:
            st.success("✅ 예약 서버 (8101)")
            agent_info = response.json()
            st.caption(f"📍 {agent_info.get('name', 'Unknown')}")
        else:
            st.error("❌ 예약 서버 오류")
    except Exception:
        st.error("❌ 예약 서버 (8101) 연결 실패")

    # 서버 실행 가이드
    with st.expander("💡 서버 실행 방법"):
        st.code("./run_servers.sh", language="bash")
        st.caption("또는 수동으로 각 서버 실행:")
        st.code("uv run python agents/recommender_agent.py\nuv run python agents/booking_agent.py", language="bash")

    # 대화 초기화 버튼
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # 메모리 뷰어 (간략 버전)
    st.subheader("🧠 저장된 메모리")

    try:
        # HTTP API를 통해 서버에서 메모리 조회
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{recommender_url}/memories/{st.session_state.user_id}")

            if response.status_code == 200:
                data = response.json()
                user_memories = data.get("memories", [])

                if user_memories:
                    st.caption(f"총 {len(user_memories)}개의 메모리")

                    # 최대 3개만 미리보기
                    preview_count = min(3, len(user_memories))
                    for idx in range(preview_count):
                        st.caption(f"• {user_memories[idx]}")

                    if len(user_memories) > 3:
                        st.caption(f"... 외 {len(user_memories) - 3}개")

                    st.page_link(
                        "pages/memory_viewer.py",
                        label="📋 전체 메모리 보기",
                        use_container_width=True
                    )
                else:
                    st.info("저장된 메모리가 없습니다.")
                    st.caption("💡 \"이탈리안 좋아해\"처럼 선호도를 말해보세요!")
            else:
                st.warning(f"메모리 조회 실패 (HTTP {response.status_code})")

    except httpx.TimeoutException as e:
        st.warning("⏱️ 서버 응답 시간 초과")
        st.caption(f"서버가 느리게 응답하고 있습니다: {str(e)}")
    except httpx.ConnectError as e:
        st.error("❌ 서버 연결 실패")
        st.caption("서버가 실행 중인지 확인하세요")
        st.code("./run_servers.sh", language="bash")
    except Exception as e:
        st.error(f"❌ 메모리 조회 오류")
        st.caption(f"상세: {type(e).__name__}: {str(e)}")

# 대화 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # A2A 호출 정보 표시 (있는 경우)
        if message["role"] == "assistant" and "a2a_calls" in message and message["a2a_calls"]:
            with st.expander(f"🔗 A2A 호출 내역 ({len(message['a2a_calls'])}건)", expanded=False):
                for idx, call in enumerate(message["a2a_calls"], 1):
                    st.markdown(f"**[{idx}] {call['target_agent']}**")
                    st.caption(f"🕐 {call['timestamp']}")
                    st.caption(f"📍 {call['target_url']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**📤 요청**")
                        st.json(call["request"], expanded=False)
                    with col2:
                        st.markdown("**📥 응답**")
                        st.json(call["response"], expanded=False)

                    if idx < len(message["a2a_calls"]):
                        st.divider()

# 채팅 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 에이전트 응답
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        a2a_calls = []

        try:
            # 추천 에이전트에 요청 (Mem0 Cloud로 빠른 응답)
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{recommender_url}/tasks/send",
                    json={
                        "task_id": f"task_{len(st.session_state.messages)}",
                        "message": prompt,
                        "user_id": st.session_state.user_id
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    agent_response = result.get("response", "응답 없음")
                    a2a_calls = result.get("a2a_calls", [])
                else:
                    agent_response = f"❌ 오류: HTTP {response.status_code}"

        except httpx.RequestError as e:
            agent_response = f"❌ 서버 연결 실패: {str(e)}\n\n서버가 실행 중인지 확인하세요:\n```bash\n./run_servers.sh\n```"
        except Exception as e:
            agent_response = f"❌ 예상치 못한 오류: {str(e)}"

        message_placeholder.markdown(agent_response)

        # A2A 호출 정보 표시
        if a2a_calls:
            with st.expander(f"🔗 A2A 호출 내역 ({len(a2a_calls)}건)", expanded=False):
                for idx, call in enumerate(a2a_calls, 1):
                    st.markdown(f"**[{idx}] {call['target_agent']}**")
                    st.caption(f"🕐 {call['timestamp']}")
                    st.caption(f"📍 {call['target_url']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**📤 요청**")
                        st.json(call["request"], expanded=False)
                    with col2:
                        st.markdown("**📥 응답**")
                        st.json(call["response"], expanded=False)

                    if idx < len(a2a_calls):
                        st.divider()

    # 응답 메시지 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": agent_response,
        "a2a_calls": a2a_calls
    })

# 하단 정보
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"👤 사용자: {st.session_state.user_id}")
with col2:
    st.caption(f"💬 메시지: {len(st.session_state.messages)}")
with col3:
    st.caption("🤖 A2A Agents")
