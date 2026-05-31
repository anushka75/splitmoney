from sqlalchemy.orm import Session
from app.api.routes.groups.models import GroupCreate
from app.services.db.postgres.groups import Groups


def create_group(db: Session, current_user, group_data: GroupCreate):
    group = Groups(created_by=current_user.id, **group_data.dict())
    db.add(group)
    db.commit()
    db.refresh(group)
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "created_by": group.created_by,
        "created_at": group.created_at,
        "updated_at": group.updated_at,
    }
