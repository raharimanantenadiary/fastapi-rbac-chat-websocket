"""
Schémas Pydantic pour Message
Validation des données entrantes/sortantes
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    """Schéma de base pour Message"""
    contenu: str = Field(min_length=1, max_length=2000)
    type_message: str = Field(default="texte", max_length=20)
    url_fichier: Optional[str] = None


class MessageCreer(MessageBase):
    """Schéma pour créer un nouveau message"""
    canal_id: int


class MessageModifier(BaseModel):
    """Schéma pour modifier un message"""
    contenu: Optional[str] = Field(None, min_length=1, max_length=2000)


class MessageLire(MessageBase):
    """Schéma pour lire un message"""
    id: int
    auteur_id: int
    canal_id: int
    est_modifie: bool
    est_supprime: bool
    date_creation: datetime
    date_modification: Optional[datetime]

    class Config:
        from_attributes = True


class MessageAvecAuteur(MessageLire):
    """Schéma message avec informations de l'auteur"""
    auteur_nom_utilisateur: str
    auteur_prenom: Optional[str] = None
    auteur_nom: Optional[str] = None


class MessageWebSocket(BaseModel):
    """Schéma pour les messages WebSocket"""
    type: str  # "message", "connexion", "deconnexion", "erreur"
    canal_id: int
    contenu: str
    auteur_nom_utilisateur: Optional[str] = None
    date_creation: Optional[datetime] = None
