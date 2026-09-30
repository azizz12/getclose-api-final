# =============================================================
# Ressource CRUD : GameSession (une partie jouée par un User)
# =============================================================
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    # ForeignKey : chaque partie appartient à exactement un joueur.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score_total = Column(Integer, default=0, nullable=False)
    finished = Column(Boolean, default=False, nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)

    # Côté relation inverse : session.user donne l'objet User propriétaire.
    user = relationship("User", back_populates="sessions")
