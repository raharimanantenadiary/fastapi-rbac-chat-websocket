"""
Modèle Role
Table des rôles (admin, utilisateur, modérateur, etc.)
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modeles.utilisateur import Utilisateur
    from app.modeles.role_permission import RolePermission


class Role(SQLModel, table=True):
   
    __tablename__ = "roles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    
    est_actif: bool = Field(default=True)
    
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    # Relations
    utilisateurs: list["Utilisateur"] = Relationship(back_populates="role")
    permissions_associees: list["RolePermission"] = Relationship(back_populates="role")
