from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.db.postgres.expenses import Expenses


def get_expenses(db: Session, group_id: int, current_user):
    expenses = (
        db.query(Expenses)
        .filter(
            Expenses.group_id == group_id,
            Expenses.created_by == current_user.id,
            Expenses.is_deleted == 0,
        )
        .order_by(Expenses.created_at.desc())
        .all()
    )
    return expenses
