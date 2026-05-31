from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.db.postgres.groups import Groups


def get_group(db: Session, group_id: int, current_user):
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
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "created_by": group.created_by,
        "created_at": group.created_at,
        "updated_at": group.updated_at,
    }
