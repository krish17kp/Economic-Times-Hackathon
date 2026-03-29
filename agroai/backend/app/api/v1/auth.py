"""
Authentication endpoints (OTP-based, no passwords).
Location: backend/app/api/v1/auth.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth import UserRegister, OTPRequest, OTPVerify, TokenResponse
from app.schemas.common import MessageResponse
from app.models.user import User
from app.core.security import create_access_token

router = APIRouter()

# In-memory OTP store (replace with Redis in production)
_otp_store: dict = {}


@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.phone == data.phone).first()
    if existing:
        raise HTTPException(status_code=409, detail="Phone already registered")

    user = User(
        phone=data.phone,
        name=data.name,
        role=data.role,
        pincode=data.pincode,
        language_pref=data.language_pref,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id), user.role.value)

    return TokenResponse(token=token, user_id=str(user.id), name=user.name, role=user.role.value)


@router.post("/send-otp", response_model=MessageResponse)
def send_otp(data: OTPRequest):
    # In dev: always use "1234". In production: integrate MSG91/Twilio
    _otp_store[data.phone] = "1234"
    return MessageResponse(message="OTP sent")


@router.post("/login", response_model=TokenResponse)
def login(data: OTPVerify, db: Session = Depends(get_db)):
    stored_otp = _otp_store.get(data.phone)
    if not stored_otp or stored_otp != data.otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="Phone not registered")

    # Clear OTP after use
    del _otp_store[data.phone]

    token = create_access_token(str(user.id), user.role.value)

    return TokenResponse(token=token, user_id=str(user.id), name=user.name, role=user.role.value)
