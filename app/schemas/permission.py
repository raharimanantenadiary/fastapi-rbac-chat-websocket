"""
Schémas Pydantic pour Permission
Validation des données entrantes/sortantes
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    """Schéma de base pour Permission"""
    code: str = Field(min_length=3, max_length=100)
    nom: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    categorie: Optional[str] = None


class PermissionCreer(PermissionBase):
    """Schéma pour créer une nouvelle permission"""
    est_actif: bool = True


class PermissionModifier(BaseModel):
    """Schéma pour modifier une permission"""
    code: Optional[str] = Field(None, min_length=3, max_length=100)
    nom: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    categorie: Optional[str] = None
    est_actif: Optional[bool] = None


class PermissionLire(PermissionBase):
    """Schéma pour lire une permission"""
    id: int
    est_actif: bool
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True
