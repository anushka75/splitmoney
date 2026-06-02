from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.db.postgres.group_members import GroupMembers


def add_group_member(db: Session, group_id: int, current_user, group_member_data):
    try:
        existing_member = (
            db.query(GroupMembers)
            .filter(
                GroupMembers.group_id == group_id,
                GroupMembers.user_id == current_user.id,
                GroupMembers.deleted == 0,
            )
            .with_for_update()
            .first()
        )
        if existing_member:
            raise HTTPException(status_code=400, detail="User is already in the group")

        group_member = GroupMembers(group_id=group_id, user_id=current_user.id)
        db.add(group_member)
        db.commit()
        db.refresh(group_member)
        return group_member
    except Exception:
        db.rollback()
        raise
