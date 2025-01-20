from typing import Optional
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from db.connection import get_db
from views import user_view
from schemas.user_schema import *

from core.config import settings
from datetime import datetime, timedelta, timezone


chzzk = APIRouter(
    prefix="/chzzk"
)

@chzzk.get('/top20')
def chzzk_top20_List(request: Request):
    
    return None