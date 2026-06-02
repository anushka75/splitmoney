from typing import Optional

from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None


class GroupInviteCreate(BaseModel):
    email: str
