# =============================================================
# Point d'entrée de l'application FastAPI.
# Ce fichier reste volontairement court : il ne fait que créer l'app
# et brancher les routers de chaque ressource. La vraie logique vit
# dans routers/ (routes HTTP) et services/ (logique métier).
# =============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, sessions

# Crée les tables en base si elles n'existent pas encore (simple pour un
# projet étudiant ; un vrai projet utiliserait des migrations Alembic).
# Importer les modèles avant ce create_all est indispensable : SQLAlchemy
# ne connaît une table que si sa classe Python a été chargée au moins une fois.
from app.models import game_session, user  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GetClose API",
    description="API backend du jeu de géographie GetClose — comptes joueurs, "
    "parties, manches, score et classement.",
    version="0.1.0",
)

# Autorise le frontend React (en dev, sur localhost) à appeler cette API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Route simple pour vérifier que l'API répond, sans toucher à la DB."""
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(sessions.router)

# À mesure que chaque étudiant crée son router, on le branche ici, par exemple :
# from app.routers import locations, categories
# app.include_router(locations.router)
# app.include_router(categories.router)
