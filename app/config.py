"""
Configuration de l'application
Charge les variables d'environnement depuis le fichier .env
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Parametres(BaseSettings):
    DATABASE_URL: str
    
    # Configuration JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuration application
    PROJECT_NAME: str = "Gestion RBAC Chat"
    DEBUG: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


parametres = Parametres()
