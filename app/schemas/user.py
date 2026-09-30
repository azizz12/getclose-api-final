# =============================================================
# Schemas Pydantic : ce que l'API accepte en entrée et renvoie en sortie
# pour la ressource User. Séparés du modèle SQLAlchemy exprès : on ne
# veut jamais renvoyer le hashed_password dans une réponse JSON.
# =============================================================
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Ce que le client envoie pour créer un compte."""
    pseudo: str = Field(min_length=2, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    """Ce que le client envoie pour se connecter."""
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Ce que l'API renvoie — jamais le mot de passe, même hashé."""
    id: int
    pseudo: str
    email: EmailStr
    created_at: datetime

    # Autorise Pydantic à lire directement un objet SQLAlchemy (User),
    # pas seulement un dict — indispensable pour renvoyer un modèle ORM.
    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Ce que /auth/login renvoie : le JWT à réutiliser dans les requêtes suivantes."""
    access_token: str
    token_type: str = "bearer"
