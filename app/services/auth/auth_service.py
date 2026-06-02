from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.db.postgres.user import User
from app.services.db.postgres.group_invitations import GroupInvitation
from app.services.db.postgres.group_members import GroupMembers
from app.services.auth.utils import hash_password, verify_password, create_access_token


class AuthService:
    @staticmethod
    def signup(db: Session, payload):
        existing_user = db.query(User).filter(User.email == payload.email).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
        )

        try:
            db.add(user)

            db.flush()

            if getattr(payload, "invite_token", None):
                token_invite = (
                    db.query(GroupInvitation)
                    .filter(
                        GroupInvitation.token == payload.invite_token,
                        GroupInvitation.email == user.email,
                        GroupInvitation.status == "pending",
                    )
                    .first()
                )
                if not token_invite:
                    raise HTTPException(
                        status_code=400, detail="Invalid invitation token"
                    )

                if not (
                    db.query(GroupMembers)
                    .filter(
                        GroupMembers.group_id == token_invite.group_id,
                        GroupMembers.user_id == user.id,
                        GroupMembers.deleted == 0,
                    )
                    .first()
                ):
                    db.add(
                        GroupMembers(group_id=token_invite.group_id, user_id=user.id)
                    )

                token_invite.status = "accepted"

            pending_invites = (
                db.query(GroupInvitation)
                .filter(
                    GroupInvitation.email == user.email,
                    GroupInvitation.status == "pending",
                )
                .all()
            )

            for invite in pending_invites:
                existing_membership = (
                    db.query(GroupMembers)
                    .filter(
                        GroupMembers.group_id == invite.group_id,
                        GroupMembers.user_id == user.id,
                        GroupMembers.deleted == 0,
                    )
                    .first()
                )

                if not existing_membership:
                    db.add(GroupMembers(group_id=invite.group_id, user_id=user.id))
                invite.status = "accepted"

            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            raise

        token = create_access_token({"sub": str(user.id)})

        return {"access_token": token}

    @staticmethod
    def login(db: Session, payload):
        user = db.query(User).filter(User.email == payload.email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id)})

        return {"access_token": token}
