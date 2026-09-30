# =============================================================
# Ressource CRUD : User (le joueur, avec un compte authentifiable)
# =============================================================
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    pseudo = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    # On ne stocke JAMAIS le mot de passe en clair — seulement son hash.
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relation 1-N : un User possède plusieurs GameSession.
    # "back_populates" crée le lien dans les deux sens (user.sessions
    # et, côté GameSession, session.user).
    sessions = relationship(
        "GameSession", back_populates="user", cascade="all, delete-orphan"
    )
