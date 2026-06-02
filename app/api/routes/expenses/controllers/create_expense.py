from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.routes.expenses.models import ExpenseCreate
from app.services.db.postgres.expenses import Expenses
from app.services.db.postgres.expense_splits import ExpenseSplits
from app.services.db.postgres.group_members import GroupMembers
from app.services.db.postgres.user import User
from sqlalchemy.exc import SQLAlchemyError


def create_expense(
    db: Session, current_user, group_id: int, expense_data: ExpenseCreate
):
    try:
        payer = (
            db.query(User)
            .filter(User.id == expense_data.paid_by, User.deleted == 0)
            .first()
        )
        if not payer:
            raise HTTPException(status_code=400, detail="Invalid paid_by user")

        member_user_ids = {
            row.user_id
            for row in db.query(GroupMembers.user_id)
            .filter(
                GroupMembers.group_id == group_id,
                GroupMembers.deleted == 0,
            )
            .all()
        }

        if expense_data.paid_by not in member_user_ids:
            raise HTTPException(status_code=400, detail="Payer must be a group member")

        participant_ids = {
            participant.user_id for participant in expense_data.participants
        }
        if not participant_ids.issubset(member_user_ids):
            raise HTTPException(
                status_code=400,
                detail="All participants must be members of the group",
            )

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
