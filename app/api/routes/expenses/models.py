from typing import List, Optional
from pydantic import BaseModel
from app.services.db.postgres.expenses import Expenses
from app.services.db.postgres.expense_splits import ExpenseSplits


class ExpenseParticipant(BaseModel):
    user_id: int
    ratio: Optional[float] = None


class ExpenseCreate(BaseModel):
    amount: float
    title: str
    description: Optional[str] = None
    paid_by: int
    split_type: str = "equal"
    participants: List[ExpenseParticipant]
