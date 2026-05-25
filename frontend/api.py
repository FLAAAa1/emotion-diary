import streamlit as st
import requests
import os
from typing import Optional, List

API_URL = os.getenv("API_URL", "")
if not API_URL:
    try: API_URL = st.secrets["API_URL"]
    except Exception: pass

def _api_url(): return API_URL or "http://127.0.0.1:8000"

def _headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

def _get(path):
    try:
        r = requests.get(f"{_api_url()}{path}", headers=_headers(), timeout=10)
        return r.json() if r.ok else []
    except Exception: return []

def _post(path, data):
    try:
        r = requests.post(f"{_api_url()}{path}", json=data, headers=_headers(), timeout=10)
        return r.json() if r.ok else {"error": r.text[:200] if r.text else f"status {r.status_code}"}
    except requests.exceptions.ConnectionError: return {"error": "无法连接后端"}
    except Exception as e: return {"error": str(e)}

def _put(path, data=None):
    try:
        r = requests.put(f"{_api_url()}{path}", json=data, headers=_headers(), timeout=10)
        return r.ok
    except Exception: return False

def _delete(path):
    try:
        r = requests.delete(f"{_api_url()}{path}", headers=_headers(), timeout=10)
        return r.status_code == 204
    except Exception: return False

# Auth
def register(nickname, password):
    return _post("/auth/register", {"nickname": nickname, "password": password})

def login(nickname, password):
    return _post("/auth/login", {"nickname": nickname, "password": password})

# Chat
def send_message(content):
    r = _post("/chat/", {"content": content})
    return r if "error" not in r else None

def get_chat_history():
    return _get("/chat/history")

# Diary
def create_diary(title, content, mood=None, emotion_score=None, conversation_id=None):
    d = {"title": title, "content": content}
    if mood: d["mood"] = mood
    if emotion_score is not None: d["emotion_score"] = emotion_score
    if conversation_id is not None: d["conversation_id"] = conversation_id
    r = _post("/diary/", d)
    return r if "error" not in r else None

def list_diaries(): return _get("/diary/")
def delete_diary(did): return _delete(f"/diary/{did}")

# Dashboard
def get_mood_timeline(): return _get("/dashboard/mood-timeline")
def get_mood_stats(): return _get("/dashboard/stats")

# Settings
def get_settings(): return _get("/api/settings") or {}
def update_settings(**kw): return _put("/api/settings", kw)
def change_password(old, new): return _put("/api/user/password", {"old_password": old, "new_password": new})
def delete_account(): return _delete("/api/user")
def clear_chat_history(): return _delete("/chat/history")

# Agents
def list_agents(): return _get("/api/agents")
def create_agent(name, avatar, personality, speaking_style):
    r = _post("/api/agents", {"name": name, "avatar": avatar, "personality": personality, "speaking_style": speaking_style})
    return r if "error" not in r else None
def delete_agent(aid): return _delete(f"/api/agents/{aid}")
def switch_agent(aid): return _put("/api/settings/agent", {"agent_id": aid})
def get_current_agent():
    settings = get_settings()
    aid = settings.get("current_agent_id")
    if aid:
        for a in list_agents():
            if a.get("id") == aid: return a
    return None
