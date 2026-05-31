from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/groups/{group_id}/members", tags=["Group Members"])


@router.get("")
def get_group_members(group_id: int, current_user=Depends(get_current_user)):
    group_members = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == current_user.id,
            GroupMember.is_deleted == False,
        )
        .all()
    )
    return group_members


@router.post("")
def add_group_members(
    group_id: int,
    group_member_data: GroupMemberCreate,
    current_user=Depends(get_current_user),
):
    group_member = GroupMember(
        group_id=group_id, user_id=current_user.id, **group_member_data.dict()
    )
    db.add(group_member)
    db.commit()
    db.refresh(group_member)
    return group_member


@router.delete("/{user_id}")
def delete_group_member(group_id: int, user_id: int, current_user=Depends(get_current_user)):
    group_member = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
            GroupMember.is_deleted == False,
        )
        .first()
    )
    if not group_member:
        raise HTTPException(status_code=404, detail="Group member not found")
    group_member.is_deleted = True
    db.commit()
    return {"detail": "Group member deleted"}
