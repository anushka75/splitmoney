from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.routes.expenses.controllers import (
    create_expense as create_expense_controller,
    get_expense as get_expense_controller,
    get_expenses as get_expenses_controller,
    update_expense as update_expense_controller,
    delete_expense as delete_expense_controller,
)
from app.api.routes.expenses.models import ExpenseCreate
from app.services.db.service import get_db

router = APIRouter(prefix="/groups/{group_id}/expenses", tags=["Expenses"])


@router.post("")
def create_expense(
    group_id: int,
    expense_data: ExpenseCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_expense_controller(db, current_user, group_id, expense_data)


@router.get("")
def get_expenses(
    group_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_expenses_controller(db, group_id, current_user)


@router.get("/{expense_id}")
def get_expense(
    group_id: int,
    expense_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_expense_controller(db, expense_id, current_user)


@router.put("/{expense_id}")
def update_expense(
    group_id: int,
    expense_id: int,
    expense_data: ExpenseCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_expense_controller(db, expense_id, expense_data, current_user)


@router.delete("/{expense_id}")
def delete_expense(
    group_id: int,
    expense_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_expense_controller(db, expense_id, current_user)
