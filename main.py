from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.bootstrap.bootstrap import bootstrap
from app.config import get_config
from app.api.routes.auth import router as auth_router
from app.api.routes.users.routes import router as user_router
from app.api.routes.groups.routes import router as group_router
from app.api.routes.expenses import router as expense_router
from app.api.routes.group_members import router as group_members_router
from app.api.routes.dashboard import router as dashboard_router
from app.services.db.service import Base, get_engine

bootstrap()

app = FastAPI()

cors_origins = [
    origin.strip() for origin in get_config().get("cors_origins") if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(group_router)
app.include_router(expense_router)
app.include_router(group_members_router)
app.include_router(dashboard_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=get_engine())
