"""
Database engine and session factory.
Location: backend/app/core/database.py

Engine is resolved lazily so test fixtures can override DATABASE_URL
via os.environ before any app module is imported.
"""

from sqlalchemy import create_engine as _create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

_engine = None
_SessionLocal = None


def _build_engine():
    """Build SQLAlchemy engine from current settings (reads env at call time)."""
    from app.config import settings   # Imported inside function — intentional
    url = settings.database_url
    kwargs: dict = {"pool_pre_ping": True}
    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    else:
        kwargs["pool_size"] = 10
        kwargs["max_overflow"] = 20
    return _create_engine(url, **kwargs)


def get_engine():
    """Return the shared SQLAlchemy engine, creating it on first call."""
    global _engine
    if _engine is None:
        _engine = _build_engine()
    return _engine


def get_session_factory():
    """Return the shared session factory, creating it on first call."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = _sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


def SessionLocal():
    """Create and return a new database session."""
    return get_session_factory()()


# 'engine' alias — used by Alembic, seed_db, and conftest
# This is a callable property-like object; call get_engine() when you need
# the real Engine (e.g. Base.metadata.create_all(bind=get_engine()))
engine = None   # Placeholder; use get_engine() for direct Engine access
