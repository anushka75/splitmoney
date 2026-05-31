from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.auth import get_current_user
from app.services.db.service import get_db
from app.api.routes.users.controllers import (
    get_user as get_user_controller,
    get_users as get_users_controller,
    search_users as search_users_controller,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
def get_user(user_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_controller(db, user_id)


@router.get("")
def list_users(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_users_controller(db)


@router.get("/search")
def search_users(email: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return search_users_controller(db, email)
