from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from backend.database import Base

class UserSettings(Base):
    __tablename__ = 'user_settings'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    language = Column(String(10), default='zh', nullable=False)
    theme = Column(String(10), default='light', nullable=False)
    ai_style = Column(String(20), default='empathetic', nullable=False)
    ai_nickname = Column(String(30), default='朋友', nullable=False)
    history_retention_days = Column(Integer, default=30, nullable=False)
    crisis_sensitivity = Column(String(10), default='medium', nullable=False)
    emotion_scale = Column(String(5), default='1-10', nullable=False)
    font_size = Column(Integer, default=14, nullable=False)
    daily_reminder_enabled = Column(Integer, default=0, nullable=False)
    current_agent_id = Column(Integer, ForeignKey('agents.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

