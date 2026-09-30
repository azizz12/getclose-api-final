# =============================================================
# Configuration centralisée du projet.
# Toutes les valeurs sensibles (secret JWT, URL de la base) sont lues
# depuis le fichier .env plutôt qu'écrites en dur dans le code — c'est
# ce qui permet de ne jamais committer de secret dans Git.
# =============================================================
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Une seule instance, importée partout ailleurs dans le projet.
settings = Settings()
