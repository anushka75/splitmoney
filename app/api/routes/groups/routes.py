from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.auth import get_current_user
from app.core.database import get_db
from app.api.routes.groups.models import GroupCreate
from app.api.routes.groups.controllers import (
    create_group as create_group_controller,
    get_groups as get_groups_controller,
    get_group as get_group_controller,
    update_group as update_group_controller,
    delete_group as delete_group_controller,
)

router = APIRouter(prefix='/groups', tags=['Groups'])


@router.get('')
def get_groups(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_groups_controller(db, current_user)


@router.post('')
def create_group(group_data: GroupCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_group_controller(db, current_user, group_data)


@router.get('/{group_id}')
def get_group(group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_group_controller(db, group_id, current_user)


@router.put('/{group_id}')
def update_group(group_id: int, group_data: GroupCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_group_controller(db, group_id, group_data, current_user)


@router.delete('/{group_id}')
def delete_group(group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_group_controller(db, group_id, current_user)
