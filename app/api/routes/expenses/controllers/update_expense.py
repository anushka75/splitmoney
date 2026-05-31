from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.routes.expenses.models import ExpenseCreate
from app.services.db.postgres.expenses import Expenses


def update_expense(
    db: Session, expense_id: int, expense_data: ExpenseCreate, current_user
):
    expense = (
        db.query(Expenses)
        .filter(
            Expenses.id == expense_id,
            Expenses.created_by == current_user.id,
            Expenses.is_deleted == 0,
        )
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in expense_data.dict().items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense
