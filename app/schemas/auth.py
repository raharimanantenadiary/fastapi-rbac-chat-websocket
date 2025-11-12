"""
Schémas Pydantic pour l'authentification
Login, Token, etc.
"""
from typing import Optional
from pydantic import BaseModel


class LoginForm(BaseModel):
    """Schéma pour le formulaire de connexion"""
    nom_utilisateur: str
    mot_de_passe: str


class Token(BaseModel):
    """Schéma pour le token JWT"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schéma pour les données contenues dans le token"""
    nom_utilisateur: Optional[str] = None
    user_id: Optional[int] = None


class ChangerMotDePasse(BaseModel):
    """Schéma pour changer le mot de passe"""
    ancien_mot_de_passe: str
    nouveau_mot_de_passe: str
