from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.settings import UserSettings
from backend.models.user import User
from backend.schemas.settings import UserSettingsOut, UserSettingsUpdate
from backend.schemas.agent import SwitchAgentRequest
from backend.auth import get_current_user

router = APIRouter(prefix='/api/settings', tags=['settings'])

DEFAULTS = {
    'language': 'zh', 'theme': 'light', 'ai_style': 'empathetic',
    'ai_nickname': '朋友', 'history_retention_days': 30,
    'crisis_sensitivity': 'medium', 'emotion_scale': '1-10',
    'font_size': 14, 'daily_reminder_enabled': 0,
}

def get_or_create_settings(user_id: int, db: Session) -> UserSettings:
    s = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if not s:
        s = UserSettings(user_id=user_id, **DEFAULTS)
        db.add(s)
        db.commit()
        db.refresh(s)
    return s

@router.get('', response_model=UserSettingsOut)
def get_settings(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    s = get_or_create_settings(user_id, db)
    user = db.query(User).filter(User.id == user_id).first()
    return UserSettingsOut(
        language=s.language, theme=s.theme, ai_style=s.ai_style,
        ai_nickname=s.ai_nickname, history_retention_days=s.history_retention_days,
        crisis_sensitivity=s.crisis_sensitivity, emotion_scale=s.emotion_scale,
        font_size=s.font_size, daily_reminder_enabled=s.daily_reminder_enabled,
        daily_reminder_time=user.daily_reminder_time.strftime('%H:%M') if user and user.daily_reminder_time else None,
    )

@router.put('', response_model=UserSettingsOut)
def update_settings(payload: UserSettingsUpdate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    s = get_or_create_settings(user_id, db)
    user = db.query(User).filter(User.id == user_id).first()
    update_data = payload.model_dump(exclude_unset=True)

    reminder_time = update_data.pop('daily_reminder_time', None)
    for key, value in update_data.items():
        if hasattr(s, key):
            setattr(s, key, value.value if hasattr(value, 'value') else value)

    if reminder_time is not None and user:
        from datetime import time as dt_time
        try:
            h, m = reminder_time.split(':')
            user.daily_reminder_time = dt_time(int(h), int(m))
        except (ValueError, AttributeError):
            user.daily_reminder_time = None

    db.commit()
    db.refresh(s)
    if user:
        db.refresh(user)
    return UserSettingsOut(
        language=s.language, theme=s.theme, ai_style=s.ai_style,
        ai_nickname=s.ai_nickname, history_retention_days=s.history_retention_days,
        crisis_sensitivity=s.crisis_sensitivity, emotion_scale=s.emotion_scale,
        font_size=s.font_size, daily_reminder_enabled=s.daily_reminder_enabled,
        daily_reminder_time=user.daily_reminder_time.strftime('%H:%M') if user and user.daily_reminder_time else None,
    )

@router.put('/agent')
def switch_agent(payload: SwitchAgentRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    s = get_or_create_settings(user_id, db)
    s.current_agent_id = payload.agent_id
    db.commit()
    return {'current_agent_id': payload.agent_id}
