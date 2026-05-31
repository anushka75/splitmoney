from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router

from app.core.database import Base, engine

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
