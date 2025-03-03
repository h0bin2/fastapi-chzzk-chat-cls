from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime
from db.models.user_model import User
from passlib.context import CryptContext

import jwt
from datetime import datetime, timedelta, timezone
from typing import Any

from core.config import settings

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    print(to_encode, settings.SECRETKEY, settings.ALGORITHM)
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRETKEY, algorithm=settings.ALGORITHM)
    except Exception as e:
        raise ValueError(f'jwt error ' , e)

    return encoded_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


#회원가입 API
def post_user_login(user_data: User, db: Session):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    
    if db_user is None or not verify_password(user_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"email": db_user.email, 'username':db_user.username})
    
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "사용자 로그인 성공",
        "token":access_token
    }

def post_user_register(user_data: User, db: Session):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(user_data.password)

    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "사용자 회원가입 성공",
    }