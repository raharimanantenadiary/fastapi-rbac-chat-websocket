"""
Modèle Permission
Table des permissions (lire, écrire, supprimer, etc.)
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modeles.role_permission import RolePermission


class Permission(SQLModel, table=True):
   
    __tablename__ = "permissions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True, max_length=100)
    nom: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    
    # Catégorie de la permission (utilisateurs, messages, canaux, etc.)
    categorie: Optional[str] = Field(default=None, max_length=50)
    
    est_actif: bool = Field(default=True)
    
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    # Relations
    roles_associes: list["RolePermission"] = Relationship(back_populates="permission")
