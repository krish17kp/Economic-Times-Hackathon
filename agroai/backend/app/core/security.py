"""
JWT token creation and verification + password hashing.
Location: backend/app/core/security.py
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.config import settings

ALGORITHM = "HS256"


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.jwt_expire_days)
    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
