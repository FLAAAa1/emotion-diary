from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.conversation import Conversation
from backend.models.settings import UserSettings
from backend.models.agent import Agent
from backend.schemas.conversation import ChatMessage, MessageOut
from backend.auth import get_current_user
from backend.llm import get_llm_provider
from backend.prompts import build_agent_prompt, build_default_prompt

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/', response_model=MessageOut)
def send_message(
    payload: ChatMessage,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_msg = Conversation(user_id=user_id, role='user', content=payload.content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    history = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.asc())
        .all()
    )
    history_dicts = [{'role': m.role, 'content': m.content} for m in history]

    # Load agent prompt
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    agent = None
    if settings and settings.current_agent_id:
        agent = db.query(Agent).filter(Agent.id == settings.current_agent_id).first()

    system_prompt = build_agent_prompt(agent) if agent else build_default_prompt()
    messages = [{'role': 'system', 'content': system_prompt}]
    for msg in history_dicts[-20:-1]:
        messages.append({'role': msg['role'], 'content': msg['content']})
    messages.append({'role': 'user', 'content': payload.content})

    llm = get_llm_provider()
    reply_content = llm.chat(messages)

    assistant_reply = Conversation(user_id=user_id, role='assistant', content=reply_content)
    db.add(assistant_reply)
    db.commit()
    db.refresh(assistant_reply)

    return MessageOut(
        id=assistant_reply.id, role=assistant_reply.role,
        content=assistant_reply.content, created_at=assistant_reply.created_at.isoformat(),
    )


@router.get('/history', response_model=List[MessageOut])
def get_history(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    messages = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.asc())
        .all()
    )
    return [
        MessageOut(id=m.id, role=m.role, content=m.content, created_at=m.created_at.isoformat())
        for m in messages
    ]


@router.delete('/history', status_code=204)
def clear_history(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Conversation).filter(Conversation.user_id == user_id).delete()
    db.commit()
