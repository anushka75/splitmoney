from sqlalchemy.orm import Session
from app.services.db.postgres.user import User


def get_users(db: Session):
    users = db.query(User).filter(User.deleted == 0).all()
    return [{"id": user.id, "email": user.email} for user in users]
