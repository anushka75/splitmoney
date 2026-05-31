from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.expenses import Expenses


def delete_expense(db: Session, expense_id: int, current_user):
    expense = db.query(Expenses).filter(Expenses.id == expense_id, Expenses.created_by == current_user.id, Expenses.is_deleted == 0).first()
    if not expense:
        raise HTTPException(status_code=404, detail='Expense not found')
    expense.is_deleted = 1
    db.commit()
    return {'detail': 'Expense deleted'}
