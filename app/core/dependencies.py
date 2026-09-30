# =============================================================
# Dépendance FastAPI réutilisable : identifie l'utilisateur connecté
# à partir du token JWT envoyé dans l'en-tête Authorization.
# Toute route qui déclare `current_user: User = Depends(get_current_user)`
# est automatiquement protégée par l'authentification.
# =============================================================
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User

# Dit à Swagger UI d'afficher un simple champ pour coller le token
# (bouton "Authorize" → champ "Value").
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_error

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_error

    return user