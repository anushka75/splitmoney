import secrets

from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.routes.groups.models import GroupInviteCreate
from app.services.db.postgres.group_invitations import GroupInvitation
from app.services.db.postgres.group_members import GroupMembers
from app.services.db.postgres.groups import Groups
from app.services.db.postgres.user import User
from app.services.email.email import send_group_invitation_email


def invite_user(
    db: Session,
    group_id: int,
    current_user,
    payload: GroupInviteCreate,
    background_tasks: BackgroundTasks,
):
    group = (
        db.query(Groups)
        .filter(
            Groups.id == group_id,
            Groups.deleted == 0,
        )
        .first()
    )

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    is_member = (
        db.query(GroupMembers)
        .filter(
            GroupMembers.group_id == group_id,
            GroupMembers.user_id == current_user.id,
            GroupMembers.deleted == 0,
        )
        .first()
    )

    if not is_member:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this group",
        )

    existing_invite = (
        db.query(GroupInvitation)
        .filter(
            GroupInvitation.group_id == group_id,
            GroupInvitation.email == payload.email,
            GroupInvitation.status == "pending",
        )
        .first()
    )

    if existing_invite:
        raise HTTPException(
            status_code=400,
            detail="Invitation already exists",
        )

    invited_user = (
        db.query(User)
        .filter(
            User.email == payload.email,
            User.deleted == 0,
        )
        .first()
    )

    if invited_user:
        existing_member = (
            db.query(GroupMembers)
            .filter(
                GroupMembers.group_id == group_id,
                GroupMembers.user_id == invited_user.id,
                GroupMembers.deleted == 0,
            )
            .first()
        )

        if existing_member:
            raise HTTPException(
                status_code=400,
                detail="User is already in the group",
            )

    token = secrets.token_urlsafe(32)

    invitation = GroupInvitation(
        group_id=group_id,
        invited_by=current_user.id,
        email=payload.email,
        token=token,
        status="pending",
    )

    try:
        # TRANSACTION START
        db.add(invitation)
        db.commit()
        db.refresh(invitation)
        # TRANSACTION END

    except Exception:
        db.rollback()
        raise

    invite_link = (
        f"https://splitmoney-frontend.vercel.app/signup"
        f"?invite_token={invitation.token}"
    )

    try:
        if background_tasks:
            background_tasks.add_task(
                send_group_invitation_email,
                recipient_email=payload.email,
                inviter_name=f"{current_user.first_name} {current_user.last_name}",
                group_name=group.name,
                invite_link=invite_link,
            )
        else:
            send_group_invitation_email(
                recipient_email=payload.email,
                inviter_name=f"{current_user.first_name} {current_user.last_name}",
                group_name=group.name,
                invite_link=invite_link,
            )
    except Exception as e:
        print(f"Email sending failed: {e}")

    return {
        "message": "Invitation sent",
        "invitation": {
            "id": invitation.id,
            "group_id": invitation.group_id,
            "email": invitation.email,
            "status": invitation.status,
        },
    }
