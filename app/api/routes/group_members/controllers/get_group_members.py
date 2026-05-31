from sqlalchemy.orm import Session
from app.services.db.postgres.group_members import GroupMembers


def get_group_members(db: Session, group_id: int, current_user):
    return (
        db.query(GroupMembers)
        .filter(
            GroupMembers.group_id == group_id,
            GroupMembers.user_id == current_user.id,
            GroupMembers.deleted == 0,
        )
        .all()
    )
