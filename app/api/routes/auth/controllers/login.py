from sqlalchemy.orm import Session
from app.api.routes.auth.models import LoginRequest
from app.services.auth.auth_service import AuthService


def login(db: Session, payload: LoginRequest):
    return AuthService.login(db, payload)
