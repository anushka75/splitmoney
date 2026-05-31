from sqlalchemy.orm import Session
from app.services.db.postgres.groups import Groups


def get_groups(db: Session, current_user):
    groups = db.query(Groups).filter(Groups.created_by == current_user.id, Groups.deleted == 0).all()
    return [
        {
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'created_by': group.created_by,
            'created_at': group.created_at,
            'updated_at': group.updated_at,
        }
        for group in groups
    ]
