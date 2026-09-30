# =============================================================
# Configuration partagée des tests : une base SQLite temporaire,
# recréée à chaque lancement de pytest, pour ne jamais toucher à la
# vraie base PostgreSQL pendant les tests.
# =============================================================
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    """Recrée des tables vides avant CHAQUE test, pour que les tests
    ne dépendent jamais de l'ordre dans lequel ils s'exécutent."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)
