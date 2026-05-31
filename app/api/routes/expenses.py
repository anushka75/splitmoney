from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("")
def create_expense(expense_data: ExpenseCreate, current_user=Depends(get_current_user)):
    expense = Expense(created_by=current_user.id, **expense_data.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    if expense_data.split_type == 'equal':
        split_amount = expense.amount / len(expense_data.participants)
        for participant in expense_data.participants:
            expense_split = ExpenseSplit(
                expense_id=expense.id, user_id=participant, amount_owed=split_amount
            )
            db.add(expense_split)
        db.commit()
    else:
        for participant in expense_data.participants:
            split_amount = participant.ratio * expense.amount
            expense_split = ExpenseSplit(
                expense_id=expense.id, user_id=participant, amount_owed=split_amount
            )
            db.add(expense_split)
        db.commit()

    return expense


@router.get("/{expense_id}")
def get_expense(expense_id: int, current_user=Depends(get_current_user)):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.created_by == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}")
def update_expense(
    expense_id: int, expense_data: ExpenseCreate, current_user=Depends(get_current_user)
):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.created_by == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in expense_data.dict().items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, current_user=Depends(get_current_user)):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.created_by == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense.is_deleted = True
    db.commit()
    return {"detail": "Expense deleted"}
