"""Database connection and request-scoped sessions."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load Backend/.env regardless of where the command is run.
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Add it to Backend/.env "
        "or your hosting environment variables."
    )

engine_options = {
    "pool_pre_ping": True,
}

if DATABASE_URL.startswith(("postgresql", "postgres")):
    engine_options.update(
        pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "5")),
        pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "10")),
        pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "1800")),
        connect_args={
            "connect_timeout": int(
                os.getenv("DB_CONNECT_TIMEOUT", "10")
            ),
        },
    )

engine = create_engine(DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db():
    """Give each request its own session and close it afterward."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create missing tables without deleting existing records."""
    from database import models_db  # noqa: F401

    Base.metadata.create_all(bind=engine)
