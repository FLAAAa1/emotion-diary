from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from backend.database import Base

class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    avatar = Column(String(10), default='🤖')
    personality = Column(Text, nullable=False)
    speaking_style = Column(Text, nullable=False)
    example_dialogue = Column(Text, default='')
    is_preset = Column(Boolean, default=False, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
