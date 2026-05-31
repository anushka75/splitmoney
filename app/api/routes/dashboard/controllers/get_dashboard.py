from sqlalchemy.orm import Session

from app.services.db.postgres.expenses import Expenses
from app.services.db.postgres.group_members import GroupMembers
from app.services.db.postgres.groups import Groups


def get_dashboard(db: Session, current_user):
    total_groups = (
        db.query(Groups)
        .join(GroupMembers, GroupMembers.group_id == Groups.id)
        .filter(
            GroupMembers.user_id == current_user.id,
            GroupMembers.deleted == 0,
            Groups.deleted == 0,
        )
        .count()
    )

    total_expenses = (
        db.query(Expenses)
        .filter(
            (Expenses.created_by == current_user.id)
            | (Expenses.paid_by == current_user.id),
            Expenses.is_deleted == 0,
        )
        .count()
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
