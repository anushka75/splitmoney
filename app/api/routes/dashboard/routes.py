from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.api.routes.dashboard.controllers import (
    get_dashboard as get_dashboard_controller,
)
from app.services.db.service import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def get_dashboard(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_dashboard_controller(db, current_user)
