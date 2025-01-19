from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.connection import get_db
from views import user_view

user = APIRouter(
    prefix="/user"
)


# 사용자 생성을 위한 API
@user.post("/")
async def create_user(request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()

    res = user_view.create_user(user_data=user_data, db=db)
    return res
    

# 사용자 조회를 위한 API
@user.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    res = user_view.get_user_by_id(user_id=user_id, db=db)
    return res