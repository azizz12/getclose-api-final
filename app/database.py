# =============================================================
# Connexion à PostgreSQL avec SQLAlchemy.
# Chaque routeur importe `get_db` pour obtenir une session de base de
# données valide le temps d'une requête HTTP, puis la referme
# automatiquement — même si une erreur survient en cours de route.
# =============================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Toutes les classes de modèles (User, Location, ...) hériteront de Base.
Base = declarative_base()


def get_db():
    """Dépendance FastAPI : fournit une session DB à une route, la ferme après."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
