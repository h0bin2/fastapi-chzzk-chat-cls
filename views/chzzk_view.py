from core.chzzk import Top
from fastapi import HTTPException, status

top = Top()

def get_chzzk_top20_list():
    try:
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "Chzzk Top20 방송 불러오기 성공",
            "data":{
                'top20':top[:20]
            }
        }
    except:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "detail": "Chzzk Top20 방송 불러오기 실패"
        }