from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from backend.database import get_db
from backend.models.diary import Diary
from backend.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/mood-timeline")
def mood_timeline(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return diary entries with mood for chart rendering."""
    rows = (
        db.query(Diary)
        .filter(Diary.user_id == user_id)
        .order_by(Diary.created_at.asc())
        .all()
    )
    return [
        {
            "id": r.id,
            "title": r.title,
            "mood": r.mood,
            "emotion_score": r.emotion_score,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]


@router.get("/stats")
def mood_stats(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return aggregate mood statistics."""
    rows = (
        db.query(Diary.mood, func.count(Diary.id))
        .filter(Diary.user_id == user_id, Diary.mood.isnot(None))
        .group_by(Diary.mood)
        .all()
    )
    return [{"mood": mood, "count": cnt} for mood, cnt in rows]
