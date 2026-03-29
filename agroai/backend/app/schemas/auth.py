"""
Auth request/response schemas.
Location: backend/app/schemas/auth.py
"""

from pydantic import BaseModel, Field
from app.core.constants import UserRole


class UserRegister(BaseModel):
    phone: str = Field(..., pattern=r"^\d{10}$", examples=["9876543210"])
    name: str = Field(..., min_length=2, max_length=100, examples=["Ramesh Kumar"])
    role: UserRole = UserRole.FARMER
    pincode: str = Field(None, pattern=r"^\d{6}$", examples=["141001"])
    language_pref: str = Field("hi", pattern=r"^(hi|en)$")


class OTPRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\d{10}$")


class OTPVerify(BaseModel):
    phone: str = Field(..., pattern=r"^\d{10}$")
    otp: str = Field(..., pattern=r"^\d{4}$")


class TokenResponse(BaseModel):
    token: str
    user_id: str
    name: str
    role: str
