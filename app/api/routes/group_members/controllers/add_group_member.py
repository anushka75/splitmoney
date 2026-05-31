from sqlalchemy.orm import Session
from app.services.db.postgres.group_members import GroupMembers


def add_group_member(db: Session, group_id: int, current_user, group_member_data):
    group_member = GroupMembers(group_id=group_id, user_id=current_user.id)
    db.add(group_member)
    db.commit()
    db.refresh(group_member)
    return group_member
