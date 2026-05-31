from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import SignupRequest, LoginRequest
from app.services.auth.auth_service import AuthService
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    return AuthService.signup(db, payload)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login(db, payload)
