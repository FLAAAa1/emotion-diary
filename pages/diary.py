import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from frontend.api import list_diaries, create_diary, delete_diary

st.set_page_config(page_title="情绪日记", page_icon="📔")

if "token" not in st.session_state:
    st.warning("请先登录")
    st.switch_page("pages/login.py")
    st.stop()

from frontend.theme import load_and_apply
load_and_apply()

st.title("N 情绪日记")
with st.sidebar:
    st.header("✍️ 写日记")
    title = st.text_input("标题")
    content = st.text_area("内容", height=150)
    mood = st.selectbox("心情", ["K 开心", "L 难过", "M 生气", "N 平静", "O 兴奋", "P 焦虑"])
    if st.button("保存日记", use_container_width=True):
        if title and content:
            result = create_diary(title=title, content=content, mood=mood)
            if result:
                st.success("日记已保存！")
                st.rerun()
            else:
                st.error("保存失败")
        else:
            st.warning("请填写标题和内容")
st.header("📖 我的日记")
diaries = list_diaries()
if not diaries:
    st.info("还没有日记，去写一篇吧！")
for entry in diaries:
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader(f"{entry.get('mood', '')} {entry['title']}")
        with col2:
            if st.button("I 删除", key=f"del_{entry['id']}"):
                if delete_diary(entry["id"]):
                    st.rerun()
        st.caption(entry["created_at"])
        st.write(entry["content"])
