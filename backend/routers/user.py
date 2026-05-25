from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.settings import UserSettings
from backend.schemas.settings import ChangePasswordRequest
from backend.auth import get_current_user, hash_password, verify_password, validate_password

router = APIRouter(prefix='/api/user', tags=['user'])

@router.put('/password')
def change_password(payload: ChangePasswordRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(payload.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail='Old password is incorrect')

    err = validate_password(payload.new_password)
    if err:
        raise HTTPException(status_code=400, detail=err)

    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {'message': 'Password updated'}

@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
def delete_account(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(UserSettings).filter(UserSettings.user_id == user_id).delete()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
