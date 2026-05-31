from sqlalchemy.orm import Session
from app.api.routes.groups.models import GroupCreate
from app.services.db.postgres.groups import Groups
from app.services.db.postgres.group_members import GroupMembers


def create_group(db: Session, current_user, group_data: GroupCreate):
    try:
        group = Groups(created_by=current_user.id, **group_data.dict())
        db.add(group)
        db.flush()

        group_members = GroupMembers(group_id=group.id, user_id=current_user.id)
        db.add(group_members)

        db.commit()
        db.refresh(group)
    except Exception:
        db.rollback()
        raise

    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "created_by": group.created_by,
        "created_at": group.created_at,
        "updated_at": group.updated_at,
    }
