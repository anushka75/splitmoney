from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.routes.groups.models import GroupCreate
from app.db.groups import Groups


def update_group(db: Session, group_id: int, group_data: GroupCreate, current_user):
    group = db.query(Groups).filter(Groups.id == group_id, Groups.created_by == current_user.id, Groups.deleted == 0).first()
    if not group:
        raise HTTPException(status_code=404, detail='Group not found')
    for key, value in group_data.dict().items():
        setattr(group, key, value)
    db.commit()
    db.refresh(group)
    return {
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'created_by': group.created_by,
        'created_at': group.created_at,
        'updated_at': group.updated_at,
    }
