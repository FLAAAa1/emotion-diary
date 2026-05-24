import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from frontend.api import login, register

st.title("🔐 欢迎来到情绪日记")

tab1, tab2 = st.tabs(["登录", "注册"])

with tab1:
    with st.form("login_form"):
        nick = st.text_input("昵称", key="login_nick")
        pw = st.text_input("密码", type="password", key="login_pw")
        submitted = st.form_submit_button("登录", use_container_width=True)
        if submitted:
            if not nick or not pw:
                st.warning("请填写昵称和密码")
            else:
                result = login(nick, pw)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.session_state.token = result["access_token"]
                    st.session_state.nickname = nick
                    st.success("登录成功！")
                    st.rerun()

with tab2:
    with st.form("register_form"):
        nick = st.text_input("昵称", key="reg_nick")
        pw = st.text_input("密码", type="password", key="reg_pw")
        pw2 = st.text_input("确认密码", type="password", key="reg_pw2")
        submitted = st.form_submit_button("注册", use_container_width=True)
        if submitted:
            if not nick or not pw:
                st.warning("请填写昵称和密码")
            elif pw != pw2:
                st.warning("两次密码不一致")
            else:
                result = register(nick, pw)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("注册成功！请切换到登录标签页")
