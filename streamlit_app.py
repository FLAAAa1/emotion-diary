import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import streamlit as st

st.set_page_config(page_title='情绪日记', page_icon='N', layout='wide')

if 'token' not in st.session_state:
    st.warning('请先登录或注册')
    st.page_link('pages/login.py', label='前往登录页面', icon='L')
    st.stop()

from frontend.theme import load_and_apply
load_and_apply()

st.success(f'欢迎回来，**{st.session_state.get(\"nickname\", \"用户\")}**！')

st.markdown('### 快速导航')
col1, col2, col3, col4 = st.columns(4)
with col1: st.page_link('pages/chat.py', label='I 树洞对话')
with col2: st.page_link('pages/diary.py', label='N 情绪日记')
with col3: st.page_link('pages/dashboard.py', label='E 情绪仪表盘')
with col4: st.page_link('pages/Settings.py', label='O 设置')

st.divider()
if st.sidebar.button('T 退出登录', use_container_width=True):
    st.session_state.clear()
    st.rerun()
