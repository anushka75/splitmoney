from sqlalchemy.orm import Session
from app.services.db.postgres.user import User


def search_users(db: Session, email: str):
    users = db.query(User).filter(User.deleted == 0, User.email.contains(email)).all()
    return [{"id": user.id, "email": user.email} for user in users]
