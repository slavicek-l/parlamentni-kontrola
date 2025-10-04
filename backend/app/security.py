from fastapi import Header, HTTPException, Depends
from .config import settings
from datetime import datetime, timedelta
import jwt

def api_key_auth(x_api_key: str | None = Header(default=None)):
    if settings.API_AUTH_MODE == "apikey":
        allowed = [k.strip() for k in settings.API_KEYS.split(",") if k.strip()]
        if not x_api_key or x_api_key not in allowed:
            raise HTTPException(status_code=401, detail="Invalid API key")
    return True

def jwt_auth(authorization: str | None = Header(default=None)):
    if settings.API_AUTH_MODE != "jwt":
        return True
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ",1)[1]
    try:
        jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True
