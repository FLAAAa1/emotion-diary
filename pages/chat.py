import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from frontend.api import send_message, get_chat_history

if "token" not in st.session_state:
    st.warning("请先登录")
    st.switch_page("pages/login.py")
    st.stop()

from frontend.theme import load_and_apply
load_and_apply()

st.title("🕳️ 树洞对话")
st.caption("在这里倾诉，我会认真倾听。")

for msg in get_chat_history():
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("说点什么吧..."):
    with st.chat_message("user"):
        st.write(prompt)
    result = send_message(prompt)
    if result:
        with st.chat_message("assistant"):
            st.write(result["content"])
        st.rerun()
    else:
        st.error("消息发送失败")
