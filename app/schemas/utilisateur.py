"""
Schémas Pydantic pour Utilisateur
Validation des données entrantes/sortantes
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UtilisateurBase(BaseModel):
    """Schéma de base pour Utilisateur"""
    nom_utilisateur: str = Field(min_length=3, max_length=50)
    email: EmailStr
    prenom: Optional[str] = None
    nom: Optional[str] = None


class UtilisateurCreer(UtilisateurBase):
    """Schéma pour créer un nouvel utilisateur"""
    mot_de_passe: str = Field(min_length=8, max_length=100)
    role_id: Optional[int] = None


class UtilisateurModifier(BaseModel):
    """Schéma pour modifier un utilisateur"""
    nom_utilisateur: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    prenom: Optional[str] = None
    nom: Optional[str] = None
    est_actif: Optional[bool] = None
    est_verifie: Optional[bool] = None
    role_id: Optional[int] = None


class UtilisateurLire(UtilisateurBase):
    """Schéma pour lire un utilisateur"""
    id: int
    est_actif: bool
    est_verifie: bool
    role_id: Optional[int]
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class UtilisateurAvecRole(UtilisateurLire):
    """Schéma utilisateur avec informations du rôle"""
    role_nom: Optional[str] = None
