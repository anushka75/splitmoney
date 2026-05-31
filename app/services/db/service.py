from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import get_config


class Base(DeclarativeBase):
    pass


class DBService:
    def __init__(self):
        self.config = None
        self.engine = None
        self.SessionLocal = None

    def setup(self, config=None):
        self.config = config or get_config()
        self.engine = create_engine(
            self.config["database_url"],
            echo=True,
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
        )

    def get_db(self):
        if self.SessionLocal is None:
            self.setup()
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


db_service = DBService()


def setup(config=None):
    db_service.setup(config)


def get_db():
    yield from db_service.get_db()


def get_engine():
    if db_service.engine is None:
        raise RuntimeError("Database service not initialized. Call bootstrap first.")
    return db_service.engine


__all__ = ["Base", "DBService", "db_service", "get_db", "get_engine", "setup"]
