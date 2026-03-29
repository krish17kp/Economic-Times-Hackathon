"""
Test fixtures: test database, test client.
Location: backend/tests/conftest.py

Strategy: Override DATABASE_URL env var BEFORE importing any app module
so SQLAlchemy engine is created with SQLite (not PostgreSQL) in tests.
"""

import os
import pytest

# Use an in-memory database for tests to ensure full isolation
import sqlalchemy.pool as pool

# ⚠️ Must set BEFORE any app.* imports — config.py will read from os.environ
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient               # noqa: E402
from sqlalchemy import create_engine                    # noqa: E402
from sqlalchemy.orm import sessionmaker                 # noqa: E402

from app.main import app                                # noqa: E402
from app.models import Base                             # noqa: E402
from app.core.database import get_engine                # noqa: E402
from app.dependencies import get_db                     # noqa: E402

# Build the test-specific SQLite in-memory engine
_test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=pool.StaticPool,
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test, drop them after."""
    Base.metadata.create_all(bind=_test_engine)
    yield
    Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture
def db():
    """Fresh DB session for each test."""
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    """TestClient with overridden DB dependency pointing at SQLite."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
