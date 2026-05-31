from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db.service import get_db
from app.api.routes.expenses.controllers import (
    create_expense as create_expense_controller,
    get_expense as get_expense_controller,
    update_expense as update_expense_controller,
    delete_expense as delete_expense_controller,
)
from app.api.routes.expenses.models import ExpenseCreate
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("")
def create_expense(expense_data: ExpenseCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_expense_controller(db, current_user, expense_data)


@router.get("/{expense_id}")
def get_expense(expense_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_expense_controller(db, expense_id, current_user)


@router.put("/{expense_id}")
def update_expense(expense_id: int, expense_data: ExpenseCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_expense_controller(db, expense_id, expense_data, current_user)


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_expense_controller(db, expense_id, current_user)
