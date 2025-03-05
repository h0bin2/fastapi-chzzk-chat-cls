from typing import Optional
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from db.connection import get_db
from views import user_view
from schemas.user_schema import *

from core.config import settings
from datetime import datetime, timedelta, timezone

user = APIRouter(
    prefix="/user"
)

templates = Jinja2Templates(directory="./templates")

# 사용자 생성을 위한 API
@user.post("/register")
async def create_user(user_register: UserRegister, db: Session = Depends(get_db)):
    res = user_view.post_user_register(user_data = user_register, db=db)  

    if res['status_code'] != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="회원가입 에러")  

    return RedirectResponse(url='/login')

@user.post('/login')
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    res = user_view.post_user_login(user_data = user_login, db=db)

    if res['status_code'] != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="일치하는 사용자가 존재하지 않습니다")

    response = JSONResponse(content=res, status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="access_token",
        value=res['token'],
        httponly=True,
        expires=datetime.now(timezone.utc) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)),  # 만료 시간
    )
    print(f"post login", res)
    return response

@user.get('/login')
async def login(request: Request):
    return templates.TemplateResponse('login.html', {'request':request})

@user.get('/register')
async def register(request:Request):
    return templates.TemplateResponse('register.html', {'request':request})

@user.get('/test')
async def test(request: Request):
    return request.state.user