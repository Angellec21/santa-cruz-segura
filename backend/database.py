from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config import settings

_is_remote = settings.DB_HOST not in ("localhost", "127.0.0.1")
_connect_args = {"ssl": {"ssl_disabled": False}} if _is_remote else {}

engine = create_engine(
    settings.database_url,
    connect_args=_connect_args,
    pool_size=5,
    max_overflow=5,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_timeout=30,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
