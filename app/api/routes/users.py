from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
def get_user(user_id: int, current_user=Depends(get_current_user)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email}


@router.get("")
def get_users(current_user=Depends(get_current_user)):
    users = db.query(Users).all()
    return users


@router.get("/search")
def search_users(email: str, current_user=Depends(get_current_user)):
    users = db.query(Users).filter(Users.email.contains(email)).all()
    return users
