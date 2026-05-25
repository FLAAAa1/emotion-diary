import streamlit as st
from frontend.api import send_message, get_chat_history, list_agents, switch_agent, create_agent, delete_agent, get_current_agent

if "token" not in st.session_state:
    st.warning("请先登录")
    st.switch_page("pages/login.py")
    st.stop()

from frontend.theme import load_and_apply
load_and_apply()

# ---- Sidebar: Agent Selector ----
with st.sidebar:
    st.subheader("🎭 陪伴角色")
    agents = list_agents()
    current = get_current_agent()

    if current:
        st.caption(f"当前：{current['avatar']} {current['name']}")
    else:
        st.caption("当前：🌿 默认·小树")

    for agent in agents:
        label = f"{agent['avatar']} {agent['name']}"
        is_current = current and current['id'] == agent['id']
        btn_label = f"{label} ✓" if is_current else label
        if st.button(btn_label, key=f"agent_{agent['id']}", use_container_width=True,
                     type="primary" if is_current else "secondary"):
            switch_agent(agent['id'] if not is_current else None)
            st.session_state.pop("_settings", None)
            st.rerun()
        if is_current:
            with st.expander("详情"):
                st.caption(agent['personality'][:100] + "...")

    st.divider()

    # Create custom agent
    with st.expander("➕ 创建角色"):
        with st.form("create_agent"):
            name = st.text_input("角色名", max_chars=20)
            avatar = st.text_input("头像 Emoji", value="🤖", max_chars=10)
            personality = st.text_area("性格描述", max_chars=500, height=80)
            speaking = st.text_area("说话风格", max_chars=500, height=80)
            if st.form_submit_button("创建", use_container_width=True):
                if name and personality and speaking:
                    result = create_agent(name, avatar, personality, speaking)
                    if result:
                        st.success("创建成功！")
                        st.rerun()
                    else:
                        st.error("创建失败，名称可能已存在")
                else:
                    st.warning("请填写完整")

    st.divider()
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ---- Main Chat Area ----
if current:
    st.title(f"{current['avatar']} 与 {current['name']} 对话")
else:
    st.title("🌿 树洞对话")
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
