from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db.service import get_db
from app.api.dependencies.auth import get_current_user
from app.api.routes.group_members.controllers import (
    get_group_members as get_group_members_controller,
    add_group_member as add_group_member_controller,
    delete_group_member as remove_group_member_controller,
)
from app.api.routes.group_members.models import GroupMemberCreate

router = APIRouter(prefix="/groups/{group_id}/members", tags=["Group Members"])


@router.get("")
def get_group_members(
    group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_group_members_controller(db, group_id, current_user)


@router.post("")
def add_group_members(
    group_id: int,
    group_member_data: GroupMemberCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return add_group_member_controller(db, group_id, current_user, group_member_data)


@router.delete("/{user_id}")
def remove_group_member(
    group_id: int,
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return remove_group_member_controller(db, group_id, user_id, current_user)
