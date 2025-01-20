import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from starlette.responses import Response
from datetime import datetime, timedelta, timezone

from routers.user_router import user

from core.config import settings

import jwt

def create_app() -> FastAPI:
    _app = FastAPI()
    _app.include_router(user)

    return _app


app = create_app()
templates = Jinja2Templates(directory="/home/user/study/chzzk-fastapi/templates")

def verify_access_token(token: str) -> dict:
    payload = jwt.decode(token, settings.SECRETKEY, algorithms=[settings.ALGORITHM])
    if datetime.now(timezone.utc) > datetime.utcfromtimestamp(payload["exp"]).replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=401, detail="Token has expired")
    
    return payload

@app.middleware("http")
async def add_jwt_authentication(request: Request, call_next):
    # 예외를 두고 싶은 경로 설정
    excluded_paths = ["/user/login", "/user/register"]  # 예외 처리할 경로 목록

    # 경로가 예외 목록에 있으면 JWT 인증을 건너뛰기
    if request.url.path in excluded_paths:
        response = await call_next(request)
        return response

    # 그 외의 경로에 대해 JWT 토큰 확인
    token = request.cookies.get("access_token")  # 쿠키에서 토큰 읽기
    
    if not token:
        response = RedirectResponse(url='/user/login')
        return response
    
    try:
        user = verify_access_token(token)
        
        request.state.user = user  # 인증된 사용자 정보를 요청에 저장
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # JWT 인증이 성공하면, 요청을 처리하고 응답을 반환
    response = await call_next(request)
    return response

@app.get('/')
async def index(request:Request):
    user_info = getattr(request.state, "user", None)
    return templates.TemplateResponse('index.html', {'request':request, "user_info":user_info})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)