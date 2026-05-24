import streamlit as st

st.set_page_config(page_title="情绪日记", page_icon="📔", layout="wide")

if "token" not in st.session_state:
    login_page = st.Page("pages/login.py", title="登录", icon="🔐")
    pg = st.navigation([login_page])
    pg.run()
    st.stop()

from frontend.theme import load_and_apply
load_and_apply()

from frontend.api import get_settings
settings = get_settings()
lang = settings.get("language", "zh") if settings else "zh"

if lang == "zh":
    pages = {
        "chat": st.Page("pages/chat.py", title="树洞对话", icon="🕳️"),
        "diary": st.Page("pages/diary.py", title="情绪日记", icon="📔"),
        "dashboard": st.Page("pages/dashboard.py", title="情绪仪表盘", icon="📊"),
        "settings": st.Page("pages/settings_page.py", title="设置", icon="⚙️"),
    }
else:
    pages = {
        "chat": st.Page("pages/chat.py", title="Chat", icon="🕳️"),
        "diary": st.Page("pages/diary.py", title="Diary", icon="📔"),
        "dashboard": st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
        "settings": st.Page("pages/settings_page.py", title="Settings", icon="⚙️"),
    }

pg = st.navigation(list(pages.values()), position="sidebar")
pg.run()

with st.sidebar:
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.clear()
        st.rerun()
