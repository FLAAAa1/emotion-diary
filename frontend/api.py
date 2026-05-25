import streamlit as st
import requests
import os
from typing import Optional, List, Dict, Any

# Read API_URL from env var (local) or Streamlit secrets (Cloud)
API_URL = os.getenv("API_URL", "")
if not API_URL:
    try:
        API_URL = st.secrets["API_URL"]
    except Exception:
        pass


def _api_url() -> str:
    if API_URL:
        return API_URL
    return "http://127.0.0.1:8000"


def _headers() -> dict:
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


# ── Auth ──────────────────────────────────────────────────────────────────

def register(nickname: str, password: str) -> dict:
    resp = requests.post(f"{_api_url()}/auth/register", json={
        "nickname": nickname, "password": password,
    })
    return resp.json() if resp.ok else {"error": resp.json().get("detail", resp.text)}


def login(nickname: str, password: str) -> dict:
    resp = requests.post(f"{_api_url()}/auth/login", json={
        "nickname": nickname, "password": password,
    })
    return resp.json() if resp.ok else {"error": resp.json().get("detail", resp.text)}


# ── Chat ──────────────────────────────────────────────────────────────────

def send_message(content: str) -> Optional[dict]:
    resp = requests.post(f"{_api_url()}/chat/", json={"content": content}, headers=_headers())
    return resp.json() if resp.ok else None


def get_chat_history() -> List[dict]:
    resp = requests.get(f"{_api_url()}/chat/history", headers=_headers())
    return resp.json() if resp.ok else []


# ── Diary ─────────────────────────────────────────────────────────────────

def create_diary(title: str, content: str, mood: str = None,
                 emotion_score: float = None, conversation_id: int = None) -> Optional[dict]:
    payload = {"title": title, "content": content}
    if mood:
        payload["mood"] = mood
    if emotion_score is not None:
        payload["emotion_score"] = emotion_score
    if conversation_id is not None:
        payload["conversation_id"] = conversation_id
    resp = requests.post(f"{_api_url()}/diary/", json=payload, headers=_headers())
    return resp.json() if resp.ok else None


def list_diaries() -> List[dict]:
    resp = requests.get(f"{_api_url()}/diary/", headers=_headers())
    return resp.json() if resp.ok else []


def get_diary(diary_id: int) -> Optional[dict]:
    resp = requests.get(f"{_api_url()}/diary/{diary_id}", headers=_headers())
    return resp.json() if resp.ok else None


def delete_diary(diary_id: int) -> bool:
    resp = requests.delete(f"{_api_url()}/diary/{diary_id}", headers=_headers())
    return resp.status_code == 204


# ── Dashboard ─────────────────────────────────────────────────────────────

def get_mood_timeline() -> List[dict]:
    resp = requests.get(f"{_api_url()}/dashboard/mood-timeline", headers=_headers())
    return resp.json() if resp.ok else []


def get_mood_stats() -> List[dict]:
    resp = requests.get(f"{_api_url()}/dashboard/stats", headers=_headers())
    return resp.json() if resp.ok else []

# ---- Settings ----

def get_settings() -> dict:
    resp = requests.get(f"{_api_url()}/api/settings", headers=_headers())
    return resp.json() if resp.ok else {}

def update_settings(**kwargs) -> bool:
    resp = requests.put(f"{_api_url()}/api/settings", json=kwargs, headers=_headers())
    return resp.ok

def change_password(old_pw: str, new_pw: str) -> bool:
    resp = requests.put(f"{_api_url()}/api/user/password", json={
        "old_password": old_pw, "new_password": new_pw,
    }, headers=_headers())
    return resp.ok

def delete_account() -> bool:
    resp = requests.delete(f"{_api_url()}/api/user", headers=_headers())
    return resp.status_code == 204

def clear_chat_history() -> bool:
    resp = requests.delete(f"{_api_url()}/chat/history", headers=_headers())
    return resp.ok

# ---- Agents ----

def list_agents() -> list:
    resp = requests.get(f"{_api_url()}/api/agents", headers=_headers())
    return resp.json() if resp.ok else []

def create_agent(name: str, avatar: str, personality: str, speaking_style: str) -> dict | None:
    resp = requests.post(f"{_api_url()}/api/agents", json={
        "name": name, "avatar": avatar, "personality": personality, "speaking_style": speaking_style,
    }, headers=_headers())
    return resp.json() if resp.ok else None

def delete_agent(agent_id: int) -> bool:
    resp = requests.delete(f"{_api_url()}/api/agents/{agent_id}", headers=_headers())
    return resp.status_code == 204

def switch_agent(agent_id: int | None) -> bool:
    resp = requests.put(f"{_api_url()}/api/settings/agent", json={"agent_id": agent_id}, headers=_headers())
    return resp.ok

def get_current_agent() -> dict | None:
    settings = get_settings()
    aid = settings.get("current_agent_id")
    if aid:
        agents_list = list_agents()
        for a in agents_list:
            if a["id"] == aid:
                return a
    return None
