from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DiaryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=5000)
    mood: Optional[str] = None
    emotion_score: Optional[float] = None
    conversation_id: Optional[int] = None


class DiaryOut(BaseModel):
    id: int
    title: str
    content: str
    mood: Optional[str] = None
    emotion_score: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}
