"""MCP Chat Client - 설정 페이지.

API 키, MCP 서버 설정 관리
"""

import json
import os
from pathlib import Path

import streamlit as st

from backend import settings

# 페이지 설정
st.set_page_config(
    page_title=f"Settings - {settings.page_title}",
    page_icon="⚙️",
    layout="wide",
)

# 타이틀
st.title("⚙️ 설정")

# 탭 구성
tab1, tab2 = st.tabs(["🔑 API 설정", "🔌 MCP 서버"])

# ============================================================================
# 탭 1: API 설정
# ============================================================================
with tab1:
    st.header("🔑 OpenAI 호환 API 설정")

    # 현재 설정 표시
    col1, col2 = st.columns(2)

    with col1:
        st.metric("API Base URL", settings.openai_api_base)
        st.metric("Model Name", settings.model_name)

    with col2:
        api_key_display = "***" + settings.openai_api_key[-4:] if len(settings.openai_api_key) > 4 else "미설정"
        st.metric("API Key", api_key_display)

        if settings.is_ollama:
            st.success("✅ Ollama 모드")
        else:
            st.warning("⚠️ OpenAI 모드")

    st.divider()

    # 설정 변경 폼
    st.subheader("✏️ 설정 변경")

    with st.form("api_settings_form"):
        api_base = st.text_input(
            "API Base URL",
            value=settings.openai_api_base,
            help="예: http://localhost:11434/v1 (Ollama)",
        )

        api_key = st.text_input(
            "API Key",
            value=settings.openai_api_key,
            type="password",
            help="Ollama는 임의의 값 가능",
        )

        model_name = st.text_input(
            "Model Name",
            value=settings.model_name,
            help="예: qwen2.5:3b",
        )

        submitted = st.form_submit_button("💾 저장", type="primary")

        if submitted:
            # .env 파일 업데이트
            env_path = Path(".env")
            env_content = f"""# MCP Chat Client 환경변수
OPENAI_API_BASE={api_base}
OPENAI_API_KEY={api_key}
MODEL_NAME={model_name}

# 데이터베이스
DATABASE_URL={settings.database_url}

# MCP 서버
MCP_SERVERS_CONFIG_PATH={settings.mcp_servers_config_path}
"""
            env_path.write_text(env_content, encoding="utf-8")

            st.success("✅ 설정이 저장되었습니다!")
            st.info("앱을 다시 시작하세요 (Ctrl+C 후 재실행)")

    st.divider()

    # Ollama 간단 가이드
    with st.expander("📖 Ollama 설치"):
        st.markdown(
            """
        ```bash
        # 설치
        curl -fsSL https://ollama.com/install.sh | sh

        # 모델 다운로드
        ollama pull qwen2.5:3b
        ```
        """
        )

# ============================================================================
# 탭 2: MCP 서버 설정
# ============================================================================
with tab2:
    st.header("🔌 MCP 서버 설정")

    # MCP 서버 설정 파일 읽기
    config_path = Path(settings.mcp_servers_config_path)

    if not config_path.exists():
        st.warning(f"설정 파일이 없습니다: {config_path}")

        if st.button("📄 기본 설정 생성"):
            default_config = {
                "servers": [
                    {
                        "name": "basic-server",
                        "description": "Part 3 기본 MCP 서버",
                        "transport": "stdio",
                        "command": "uv",
                        "args": ["run", "python", "../03-mcp-tools/01-basic-server/server.py"],
                        "enabled": False,
                    },
                    {
                        "name": "tools-server",
                        "description": "Part 3 도구 서버",
                        "transport": "stdio",
                        "command": "uv",
                        "args": ["run", "python", "../03-mcp-tools/02-tools/server.py"],
                        "enabled": True,
                    },
                ]
            }

            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(json.dumps(default_config, indent=2, ensure_ascii=False), encoding="utf-8")
            st.success("기본 설정 파일이 생성되었습니다!")
            st.rerun()

    else:
        # 설정 파일 표시
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        st.subheader("📋 등록된 MCP 서버")

        if "servers" not in config or not config["servers"]:
            st.warning("등록된 서버가 없습니다.")
        else:
            for idx, server in enumerate(config["servers"]):
                with st.expander(
                    f"**{server['name']}** - {'✅ 활성' if server.get('enabled', False) else '❌ 비활성'}",
                    expanded=server.get("enabled", False),
                ):
                    st.markdown(f"**설명:** {server.get('description', 'N/A')}")
                    st.code(f"{server.get('command', 'N/A')} {' '.join(server.get('args', []))}")

                    # 활성화/비활성화 토글
                    enabled = st.checkbox(
                        "활성화",
                        value=server.get("enabled", False),
                        key=f"enable_{idx}",
                    )

                    if enabled != server.get("enabled", False):
                        # 설정 업데이트
                        config["servers"][idx]["enabled"] = enabled
                        config_path.write_text(
                            json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
                        )
                        st.success(f"{'✅ 활성화' if enabled else '❌ 비활성화'}되었습니다!")
                        st.rerun()
