from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.models.settings import UserSettings
from backend.schemas.user import UserRegister, UserLogin, TokenResponse, UserOut
from backend.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.nickname == payload.nickname).first():
        raise HTTPException(status_code=400, detail='Nickname already taken')

    user = User(nickname=payload.nickname, password_hash=hash_password(payload.password))
    db.add(user)
    db.flush()

    settings = UserSettings(user_id=user.id)
    db.add(settings)
    db.commit()
    db.refresh(user)
    return user


@router.post('/login', response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nickname == payload.nickname).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid nickname or password')

    token = create_access_token(user.id)
    return TokenResponse(access_token=token)
