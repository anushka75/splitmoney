from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.db.postgres.groups import Groups


def delete_group(db: Session, group_id: int, current_user):
    group = (
        db.query(Groups)
        .filter(
            Groups.id == group_id,
            Groups.created_by == current_user.id,
            Groups.deleted == 0,
        )
        .first()
    )
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    group.deleted = 1
    db.commit()
    return {"detail": "Group deleted"}
