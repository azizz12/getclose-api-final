# =============================================================
# Routes d'authentification : inscription et connexion.
# Ces routes restent volontairement légères — elles délèguent le
# travail à security.py (hash, JWT) et se contentent de lire/écrire
# en base et de renvoyer la bonne réponse HTTP.
# =============================================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # On vérifie l'unicité nous-mêmes pour renvoyer un message clair,
    # plutôt que de laisser la base renvoyer une erreur SQL brute.
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte existe déjà avec cet email.",
        )

    user = User(
        pseudo=payload.pseudo,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # récupère l'id généré par la base
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    # Même message d'erreur que le mot de passe soit faux OU l'email
    # inconnu — ne jamais révéler si un email existe déjà en base.
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou mot de passe incorrect.",
    )
    if not user or not verify_password(payload.password, user.hashed_password):
        raise invalid_credentials

    token = create_access_token(user_id=user.id)
    return Token(access_token=token)
