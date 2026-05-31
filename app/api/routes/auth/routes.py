from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.auth import get_current_user
from app.services.db.service import get_db
from app.api.routes.auth.models import SignupRequest, LoginRequest
from app.api.routes.auth.controllers import (
    signup as signup_controller,
    login as login_controller,
    get_user as get_user_controller,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    return signup_controller(db, payload)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_controller(db, payload)


@router.get("/me")
def get_user(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_controller(db, current_user.id)
