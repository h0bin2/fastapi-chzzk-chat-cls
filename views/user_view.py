from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime
from db.models.user_model import User


# 사용자 조회를 위한 API
def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.userid == user_id).first()

    if user is not None:
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "사용자 조회 성공",
            "data": user
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="일치하는 사용자가 존재하지 않습니다")