from fastapi import FastAPI
from app.bootstrap.bootstrap import bootstrap
from app.api.routes.auth import router as auth_router
from app.api.routes.users.routes import router as user_router
from app.api.routes.groups.routes import router as group_router
from app.api.routes.expenses import router as expense_router
from app.api.routes.group_members import router as group_members_router
from app.services.db_service import Base, get_engine

bootstrap()

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(group_router)
app.include_router(expense_router)
app.include_router(group_members_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=get_engine())
