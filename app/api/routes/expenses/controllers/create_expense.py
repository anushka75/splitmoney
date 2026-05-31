from sqlalchemy.orm import Session
from app.api.routes.expenses.models import ExpenseCreate
from app.services.db.postgres.expenses import Expenses
from app.services.db.postgres.expense_splits import ExpenseSplits
from sqlalchemy.exc import SQLAlchemyError


def create_expense(db: Session, current_user, group_id: int, expense_data: ExpenseCreate):
    try:
        expense = Expenses(
            group_id=group_id,
            amount=expense_data.amount,
            title=expense_data.title,
            description=expense_data.description,
            paid_by=expense_data.paid_by,
            created_by=current_user.id,
            split_type=expense_data.split_type,
        )
        db.add(expense)
        db.flush()

        if expense_data.split_type == "equal":
            split_amount = expense.amount / len(expense_data.participants)
            for participant in expense_data.participants:
                db.add(
                    ExpenseSplits(
                        expense_id=expense.id,
                        user_id=participant.user_id,
                        amount_owed=split_amount,
                    )
                )
        else:
            for participant in expense_data.participants:
                split_amount = (participant.ratio or 0) * expense.amount
                db.add(
                    ExpenseSplits(
                        expense_id=expense.id,
                        user_id=participant.user_id,
                        amount_owed=split_amount,
                    )
                )

        db.commit()
        db.refresh(expense)
        return {
            "id": expense.id,
            "group_id": expense.group_id,
            "amount": expense.amount,
            "title": expense.title,
            "description": expense.description,
            "paid_by": expense.paid_by,
            "created_by": expense.created_by,
            "split_type": expense.split_type,
        }
    except SQLAlchemyError:
        db.rollback()
        raise
