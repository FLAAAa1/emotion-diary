from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.diary import Diary
from backend.schemas.diary import DiaryCreate, DiaryOut
from backend.auth import get_current_user

router = APIRouter(prefix="/diary", tags=["diary"])


@router.post("/", response_model=DiaryOut, status_code=status.HTTP_201_CREATED)
def create_diary(
    payload: DiaryCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    diary = Diary(
        user_id=user_id,
        title=payload.title,
        content=payload.content,
        mood=payload.mood,
        emotion_score=payload.emotion_score,
        conversation_id=payload.conversation_id,
    )
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary


@router.get("/", response_model=List[DiaryOut])
def list_diaries(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Diary)
        .filter(Diary.user_id == user_id)
        .order_by(Diary.created_at.desc())
        .all()
    )


@router.get("/{diary_id}", response_model=DiaryOut)
def get_diary(
    diary_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    diary = db.query(Diary).filter(Diary.id == diary_id, Diary.user_id == user_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diary(
    diary_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    diary = db.query(Diary).filter(Diary.id == diary_id, Diary.user_id == user_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    db.delete(diary)
    db.commit()
