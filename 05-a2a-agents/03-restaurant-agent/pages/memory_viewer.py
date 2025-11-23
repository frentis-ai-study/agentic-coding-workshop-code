"""Memory Viewer Page

사용자 메모리를 관리하고 삭제하는 페이지
"""

import httpx
import streamlit as st

st.set_page_config(
    page_title="메모리 뷰어",
    page_icon="🧠",
    layout="wide"
)

# 세션 상태 가져오기 (main app에서 공유)
if "user_id" not in st.session_state:
    st.session_state.user_id = "user"

# 서버 URL 설정
recommender_url = "http://localhost:8100"

st.title("🧠 메모리 뷰어")
st.caption("저장된 메모리를 관리하고 삭제할 수 있습니다")

# 사용자 ID 표시
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"👤 사용자: {st.session_state.user_id}")
with col2:
    if st.button("🔄 새로고침", use_container_width=True):
        st.rerun()

st.divider()

# 메모리 조회
try:
    with httpx.Client(timeout=10.0) as client:
        response = client.get(f"{recommender_url}/memories/{st.session_state.user_id}/details")

        if response.status_code == 200:
            data = response.json()
            memories = data.get("memories", [])

            if memories:
                st.success(f"✅ 총 {len(memories)}개의 메모리가 저장되어 있습니다")

                # 전체 삭제 버튼
                col1, col2, col3 = st.columns([2, 2, 1])
                with col3:
                    if st.button("🗑️ 전체 초기화", type="secondary", use_container_width=True):
                        st.session_state.confirm_delete_all = True

                # 전체 삭제 확인
                if st.session_state.get("confirm_delete_all", False):
                    st.warning("⚠️ 모든 메모리를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ 예, 전체 삭제", type="primary", use_container_width=True):
                            try:
                                delete_response = client.delete(
                                    f"{recommender_url}/memories/{st.session_state.user_id}"
                                )
                                if delete_response.status_code == 200:
                                    st.success("✅ 모든 메모리가 삭제되었습니다")
                                    st.session_state.confirm_delete_all = False
                                    st.rerun()
                                else:
                                    st.error(f"❌ 삭제 실패: HTTP {delete_response.status_code}")
                            except Exception as e:
                                st.error(f"❌ 삭제 오류: {str(e)}")
                    with col2:
                        if st.button("❌ 취소", use_container_width=True):
                            st.session_state.confirm_delete_all = False
                            st.rerun()

                st.divider()

                # 메모리 목록
                for idx, memory in enumerate(memories, 1):
                    with st.container():
                        col1, col2 = st.columns([4, 1])

                        with col1:
                            st.markdown(f"**{idx}. {memory['memory']}**")
                            st.caption(f"ID: `{memory['id']}`")

                        with col2:
                            delete_key = f"delete_{memory['id']}"
                            if st.button("🗑️ 삭제", key=delete_key, use_container_width=True):
                                try:
                                    delete_response = client.delete(
                                        f"{recommender_url}/memories/{st.session_state.user_id}/{memory['id']}"
                                    )
                                    if delete_response.status_code == 200:
                                        st.success(f"✅ 메모리가 삭제되었습니다")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ 삭제 실패: HTTP {delete_response.status_code}")
                                except Exception as e:
                                    st.error(f"❌ 삭제 오류: {str(e)}")

                        if idx < len(memories):
                            st.divider()

            else:
                st.info("📭 저장된 메모리가 없습니다")
                st.caption("💡 채팅 페이지에서 \"이탈리안 좋아해\"처럼 선호도를 말해보세요!")

        else:
            st.error(f"❌ 메모리 조회 실패: HTTP {response.status_code}")

except httpx.TimeoutException:
    st.error("⏱️ 서버 응답 시간 초과")
    st.caption("서버가 느리게 응답하고 있습니다")

except httpx.ConnectError:
    st.error("❌ 서버 연결 실패")
    st.caption("서버가 실행 중인지 확인하세요")
    st.code("./run_servers.sh", language="bash")

except Exception as e:
    st.error(f"❌ 예상치 못한 오류: {str(e)}")

# 하단 버튼
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.page_link(
        "chat_ui.py",
        label="⬅️ 채팅으로 돌아가기",
        use_container_width=True
    )
with col2:
    st.link_button(
        "📖 API 문서",
        url=f"{recommender_url}/docs",
        use_container_width=True
    )
