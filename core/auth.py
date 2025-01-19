import jwt
from datetime import datetime, timedelta, timezone

from core.config import settings

def verify_access_token(token: str) -> dict:
    print(settings.SECRETKEY, settings.ALGORITHM)
    try:
        payload = jwt.decode(token, settings.SECRETKEY, algorithms=[settings.ALGORITHM])
        if datetime.now(timezone.utc) > datetime.utcfromtimestamp(payload["exp"]):
            raise HTTPException(status_code=401, detail="Token has expired")
        print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")