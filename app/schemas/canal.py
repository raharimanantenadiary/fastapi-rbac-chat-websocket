"""
Schémas Pydantic pour Canal
Validation des données entrantes/sortantes
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CanalBase(BaseModel):
    """Schéma de base pour Canal"""
    nom: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    type_canal: str = Field(default="public", max_length=20)
    role_minimum_requis: Optional[str] = None


class CanalCreer(CanalBase):
    """Schéma pour créer un nouveau canal"""
    est_actif: bool = True


class CanalModifier(BaseModel):
    """Schéma pour modifier un canal"""
    nom: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    type_canal: Optional[str] = None
    role_minimum_requis: Optional[str] = None
    est_actif: Optional[bool] = None


class CanalLire(CanalBase):
    """Schéma pour lire un canal"""
    id: int
    est_actif: bool
    createur_id: Optional[int]
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class CanalAvecStats(CanalLire):
    """Schéma canal avec statistiques"""
    nombre_messages: int = 0
    dernier_message: Optional[datetime] = None
