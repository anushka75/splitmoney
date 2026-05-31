from app.services.db.postgres.user import User
from typing import Optional
from pydantic import BaseModel


class SignupRequest(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
