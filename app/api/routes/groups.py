from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("")
def get_groups(current_user=Depends(get_current_user)):
    user_groups = (
        db.query(UserGroup)
        .filter(UserGroup.user_id == current_user.id, UserGroup.is_deleted == False)
        .all()
    )
    return user_groups


@router.post("")
def create_group(group_data: GroupCreate, current_user=Depends(get_current_user)):
    user_group = UserGroup(user_id=current_user.id, **group_data.dict())
    db.add(user_group)
    db.commit()
    db.refresh(user_group)
    return user_group


@router.get("/{group_id}")
def get_group(group_id: int, current_user=Depends(get_current_user)):
    user_group = (
        db.query(UserGroup)
        .filter(UserGroup.id == group_id, UserGroup.user_id == current_user.id)
        .first()
    )
    if not user_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return user_group


@router.put("/{group_id}")
def update_group(
    group_id: int, group_data: GroupCreate, current_user=Depends(get_current_user)
):
    user_group = (
        db.query(UserGroup)
        .filter(UserGroup.id == group_id, UserGroup.user_id == current_user.id)
        .first()
    )
    if not user_group:
        raise HTTPException(status_code=404, detail="Group not found")
    for key, value in group_data.dict().items():
        setattr(user_group, key, value)
    db.commit()
    db.refresh(user_group)
    return user_group


@router.delete("/{group_id}")
def delete_group(group_id: int, current_user=Depends(get_current_user)):
    user_group = (
        db.query(UserGroup)
        .filter(UserGroup.id == group_id, UserGroup.user_id == current_user.id)
        .first()
    )
    if not user_group:
        raise HTTPException(status_code=404, detail="Group not found")
    user_group.is_deleted = True
    db.commit()
    return {"detail": "Group deleted"}
