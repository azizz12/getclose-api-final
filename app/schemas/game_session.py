# =============================================================
# Schemas Pydantic pour GameSession.
# =============================================================
from datetime import datetime

from pydantic import BaseModel


class GameSessionCreate(BaseModel):
    """Rien à fournir par le client : le user_id vient du token JWT,
    jamais du corps de la requête (sinon on pourrait créer une partie
    au nom de quelqu'un d'autre)."""
    pass


class GameSessionUpdate(BaseModel):
    """Champs modifiables — tous optionnels (PATCH, pas PUT)."""
    score_total: int | None = None
    finished: bool | None = None


class GameSessionOut(BaseModel):
    id: int
    user_id: int
    score_total: int
    finished: bool
    started_at: datetime
    finished_at: datetime | None

    model_config = {"from_attributes": True}
