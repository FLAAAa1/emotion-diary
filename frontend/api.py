import streamlit as st
import requests
import os
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse

API_URL = os.getenv("API_URL", "")

def _api_url() -> str:
    if API_URL:
        return API_URL
    try:
        host = urlparse(st.context.server.address).hostname if st.context.server.address else None
    except Exception:
        host = None
    if not host or host in ("0.0.0.0", "::"):
        host = "127.0.0.1"
    return f"http://{host}:8000"


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
