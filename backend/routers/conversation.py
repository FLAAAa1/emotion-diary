from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.conversation import Conversation
from backend.schemas.conversation import ChatMessage, MessageOut
from backend.auth import get_current_user
from backend.llm import get_llm_provider, build_messages

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=MessageOut)
def send_message(
    payload: ChatMessage,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Send a message to the tree-hole and get an AI reply."""
    # Save user message
    user_msg = Conversation(user_id=user_id, role="user", content=payload.content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # Fetch recent conversation history for context
    history = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.asc())
        .all()
    )
    history_dicts = [{"role": m.role, "content": m.content} for m in history]

    # Build messages with system prompt + history + current message
    messages = build_messages(payload.content, history_dicts[:-1])  # exclude the just-saved msg

    # Call LLM
    llm = get_llm_provider()
    reply_content = llm.chat(messages)

    # Save assistant reply
    assistant_reply = Conversation(
        user_id=user_id,
        role="assistant",
        content=reply_content,
    )
    db.add(assistant_reply)
    db.commit()
    db.refresh(assistant_reply)

    return MessageOut(
        id=assistant_reply.id,
        role=assistant_reply.role,
        content=assistant_reply.content,
        created_at=assistant_reply.created_at.isoformat(),
    )


@router.get("/history", response_model=List[MessageOut])
def get_history(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    messages = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.asc())
        .all()
    )
    return [
        MessageOut(
            id=m.id,
            role=m.role,
            content=m.content,
            created_at=m.created_at.isoformat(),
        )
        for m in messages
    ]

@router.delete('/history', status_code=204)
def clear_history(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Conversation).filter(Conversation.user_id == user_id).delete()
    db.commit()
