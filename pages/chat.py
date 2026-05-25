import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from frontend.api import send_message, get_chat_history, list_agents, switch_agent, create_agent, delete_agent, get_current_agent

if "token" not in st.session_state:
    st.warning("请先登录")
    st.switch_page("pages/login.py")
    st.stop()

from frontend.theme import load_and_apply
load_and_apply()

st.subheader("🎭 陪伴角色")
try:
    agents = list_agents()
    current = get_current_agent()
except Exception:
    agents = []
    current = None

if agents:
    cols = st.columns(min(len(agents), 5) or 5)
    for i, agent in enumerate(agents):
        with cols[i % 5]:
            label = f"{agent['avatar']} {agent['name']}"
            is_current = current and current.get('id') == agent['id']
            btn_label = f"{label} ✓" if is_current else label
            if st.button(btn_label, key=f"agent_{agent['id']}", use_container_width=True):
                try:
                    switch_agent(agent['id'] if not is_current else None)
                    st.session_state.pop("_settings", None)
                except Exception:
                    st.error("切换失败")
                st.rerun()
else:
    st.caption("⚠️ 无法加载角色列表")

with st.expander("➕ 创建自定义角色"):
    with st.form("create_agent"):
        c1, c2 = st.columns(2)
        with c1: name = st.text_input("角色名", max_chars=20)
        with c2: avatar = st.text_input("头像 Emoji", value="🤖", max_chars=10)
        personality = st.text_area("性格描述", max_chars=500, height=60)
        speaking = st.text_area("说话风格", max_chars=500, height=60)
        if st.form_submit_button("创建角色", use_container_width=True):
            if name and personality and speaking:
                result = create_agent(name, avatar, personality, speaking)
                if result:
                    st.success("创建成功！")
                    st.rerun()
                else:
                    st.error("创建失败")
            else:
                st.warning("请填写完整")

st.divider()

if current:
    st.caption(f"正在与 {current['avatar']} {current['name']} 对话")
else:
    st.caption("🌿 正在与 默认·小树 对话")

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
