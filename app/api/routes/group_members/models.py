from typing import Optional
from pydantic import BaseModel
from app.services.db.postgres.group_members import GroupMembers


class GroupMemberCreate(BaseModel):
    pass
