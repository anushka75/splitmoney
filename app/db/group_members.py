from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime

from app.core.database import Base


class GroupMembers(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    deleted = Column(Integer, default=0)
