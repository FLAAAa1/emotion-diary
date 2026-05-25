from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AgentOut(BaseModel):
    id: int
    name: str
    avatar: str
    personality: str
    speaking_style: str
    example_dialogue: str = ''
    is_preset: bool
    creator_id: Optional[int] = None
    model_config = {'from_attributes': True}

class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    avatar: str = Field(default='🤖', max_length=10)
    personality: str = Field(..., min_length=1, max_length=500)
    speaking_style: str = Field(..., min_length=1, max_length=500)

class AgentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    avatar: Optional[str] = Field(default=None, max_length=10)
    personality: Optional[str] = Field(default=None, min_length=1, max_length=500)
    speaking_style: Optional[str] = Field(default=None, min_length=1, max_length=500)

class SwitchAgentRequest(BaseModel):
    agent_id: Optional[int] = None
