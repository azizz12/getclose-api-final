# =============================================================
# CRUD complet pour GameSession — toutes les routes sont protégées :
# on ne peut créer/lire/modifier/supprimer que SES PROPRES parties.
# =============================================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.game_session import GameSession
from app.models.user import User
from app.schemas.game_session import GameSessionOut, GameSessionUpdate

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _get_owned_session_or_404(session_id: int, user: User, db: Session) -> GameSession:
    """Récupère une GameSession en vérifiant qu'elle appartient bien à
    l'utilisateur connecté. Fonction interne, réutilisée par plusieurs routes."""
    game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if game_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partie introuvable.")
    if game_session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ce n'est pas votre partie.")
    return game_session


@router.post("", response_model=GameSessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Démarre une nouvelle partie pour l'utilisateur connecté.
    Le user_id vient du token, jamais du corps de la requête."""
    game_session = GameSession(user_id=current_user.id)
    db.add(game_session)
    db.commit()
    db.refresh(game_session)
    return game_session


@router.get("", response_model=list[GameSessionOut])
def list_my_sessions(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Liste uniquement les parties de l'utilisateur connecté (pas toutes les parties)."""
    return db.query(GameSession).filter(GameSession.user_id == current_user.id).all()


@router.get("/{session_id}", response_model=GameSessionOut)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_owned_session_or_404(session_id, current_user, db)


@router.patch("/{session_id}", response_model=GameSessionOut)
def update_session(
    session_id: int,
    payload: GameSessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game_session = _get_owned_session_or_404(session_id, current_user, db)

    # exclude_unset=True : on ne touche que les champs réellement envoyés
    # par le client, pas ceux laissés à None par défaut dans le schema.
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(game_session, field, value)

    db.commit()
    db.refresh(game_session)
    return game_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game_session = _get_owned_session_or_404(session_id, current_user, db)
    db.delete(game_session)
    db.commit()
