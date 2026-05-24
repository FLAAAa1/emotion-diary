from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func

from backend.database import Base


class Diary(Base):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    title = Column(String(100), nullable=False)
    content = Column(String(5000), nullable=False)
    mood = Column(String(50), nullable=True)
    emotion_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
