from sqlalchemy.orm import Session
from app.api.routes.auth.models import SignupRequest
from app.services.auth.auth_service import AuthService


def signup(db: Session, payload: SignupRequest):
    return AuthService.signup(db, payload)
