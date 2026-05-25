from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class LanguageEnum(str, Enum):
    zh = 'zh'
    en = 'en'

class ThemeEnum(str, Enum):
    light = 'light'
    dark = 'dark'

class AIStyleEnum(str, Enum):
    empathetic = 'empathetic'
    rational = 'rational'
    humorous = 'humorous'
    concise = 'concise'

class CrisisSensitivityEnum(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class EmotionScaleEnum(str, Enum):
    scale_1_5 = '1-5'
    scale_1_10 = '1-10'

class UserSettingsOut(BaseModel):
    language: str = 'zh'
    theme: str = 'light'
    ai_style: str = 'empathetic'
    ai_nickname: str = '朋友'
    history_retention_days: int = 30
    crisis_sensitivity: str = 'medium'
    emotion_scale: str = '1-10'
    font_size: int = 14
    daily_reminder_enabled: int = 0
    daily_reminder_time: Optional[str] = None
    current_agent_id: Optional[int] = None
    model_config = {'from_attributes': True}

class UserSettingsUpdate(BaseModel):
    language: Optional[LanguageEnum] = None
    theme: Optional[ThemeEnum] = None
    ai_style: Optional[AIStyleEnum] = None
    ai_nickname: Optional[str] = Field(default=None, max_length=30)
    history_retention_days: Optional[int] = Field(default=None, ge=1, le=365)
    crisis_sensitivity: Optional[CrisisSensitivityEnum] = None
    emotion_scale: Optional[EmotionScaleEnum] = None
    font_size: Optional[int] = Field(default=None, ge=10, le=24)
    daily_reminder_enabled: Optional[int] = Field(default=None, ge=0, le=1)
    daily_reminder_time: Optional[str] = None
    current_agent_id: Optional[int] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=4, max_length=100)

