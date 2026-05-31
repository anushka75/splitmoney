from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.group_members import GroupMembers


def delete_group_member(db: Session, group_id: int, user_id: int, current_user):
    group_member = db.query(GroupMembers).filter(
        GroupMembers.group_id == group_id,
        GroupMembers.user_id == user_id,
        GroupMembers.deleted == 0,
    ).first()
    if not group_member:
        raise HTTPException(status_code=404, detail='Group member not found')
    group_member.deleted = 1
    db.commit()
    return {'detail': 'Group member deleted'}
