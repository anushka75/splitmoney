from sqlalchemy import func
from sqlalchemy.orm import Session

from app.services.db.postgres.expenses import Expenses
from app.services.db.postgres.expense_splits import ExpenseSplits
from app.services.db.postgres.group_members import GroupMembers
from app.services.db.postgres.groups import Groups


def get_dashboard(db: Session, current_user):
    total_groups = (
        db.query(Groups.id)
        .join(GroupMembers, Groups.id == GroupMembers.group_id)
        .filter(
            GroupMembers.user_id == current_user.id,
            Groups.deleted == 0,
        )
        .count()
    )

    total_expenses = (
        db.query(func.coalesce(func.sum(ExpenseSplits.amount_owed), 0))
        .join(Expenses, ExpenseSplits.expense_id == Expenses.id)
        .join(Groups, Expenses.group_id == Groups.id)
        .join(
            GroupMembers,
            (GroupMembers.group_id == Groups.id)
            & (GroupMembers.user_id == current_user.id),
        )
        .filter(
            ExpenseSplits.user_id == current_user.id,
            ExpenseSplits.is_deleted == 0,
            ExpenseSplits.is_settled == 0,
            Groups.deleted == 0,
        )
        .scalar()
    )

    return {
        "user": {
            "id": current_user.id,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email,
        },
        "stats": {
            "total_groups": total_groups,
            "total_expenses": total_expenses,
        },
    }
