# =============================================================
# Sécurité : hash du mot de passe + création/vérification des JWT.
# Aucune route n'est ici — juste des fonctions pures, réutilisables
# par n'importe quel router.
# =============================================================
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# bcrypt : algorithme de hash à sens unique, conçu pour être lent
# exprès (résiste aux attaques par force brute).
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Transforme un mot de passe en clair en hash irréversible à stocker en base."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu'un mot de passe tapé correspond au hash stocké, sans jamais
    déchiffrer ce hash (bcrypt ne se déchiffre pas : on re-hash et on compare)."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Génère un JWT signé, valable JWT_EXPIRE_MINUTES, qui identifie ce user_id."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int | None:
    """Décode et vérifie un JWT. Renvoie l'id utilisateur s'il est valide,
    None si le token est invalide, expiré, ou falsifié."""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None
