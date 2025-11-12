"""
Schémas Pydantic pour Role
Validation des données entrantes/sortantes
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """Schéma de base pour Role"""
    nom: str = Field(min_length=2, max_length=50)
    description: Optional[str] = None


class RoleCreer(RoleBase):
    """Schéma pour créer un nouveau rôle"""
    est_actif: bool = True


class RoleModifier(BaseModel):
    """Schéma pour modifier un rôle"""
    nom: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = None
    est_actif: Optional[bool] = None


class RoleLire(RoleBase):
    """Schéma pour lire un rôle"""
    id: int
    est_actif: bool
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class RoleAvecPermissions(RoleLire):
    """Schéma rôle avec liste des permissions"""
    permissions: list[str] = []
