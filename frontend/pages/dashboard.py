import streamlit as st
import pandas as pd
from frontend.api import get_mood_timeline, get_mood_stats

if "token" not in st.session_state:
    st.warning("请先登录")
    st.switch_page("pages/login.py")
    st.stop()

from frontend.theme import load_and_apply
load_and_apply()

st.header("情绪时间线")
timeline = get_mood_timeline()
if timeline:
    df = pd.DataFrame(timeline)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df = df.sort_values("created_at")
    if "emotion_score" in df.columns and df["emotion_score"].notna().any():
        st.line_chart(df.set_index("created_at")["emotion_score"])
    else:
        st.info("暂无情绪评分数据")
    st.dataframe(df[["created_at","title","mood","emotion_score"]], use_container_width=True, hide_index=True)
else:
    st.info("暂无日记数据")

st.header("心情分布")
stats = get_mood_stats()
if stats:
    st.bar_chart(pd.DataFrame(stats).set_index("mood"))
else:
    st.info("暂无心情分布数据")
