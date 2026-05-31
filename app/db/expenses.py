from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.core.database import Base


class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    paid_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    split_type = Column(String(50), nullable=False, server_default="equal")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Integer, default=0)
