from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.db.postgres.user import User


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id, User.deleted == 0).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email}
