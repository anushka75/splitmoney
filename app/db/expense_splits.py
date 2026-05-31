from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric
from datetime import datetime

from app.core.database import Base


class ExpenseSplits(Base):
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount_owed = Column(Numeric(10, 2), nullable=False)
    is_settled = Column(Integer, default=0)
    settled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Integer, default=0)
