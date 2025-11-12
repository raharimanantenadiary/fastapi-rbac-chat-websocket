"""
Modèle Utilisateur
Table qui stocke tous les utilisateurs du système
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modeles.role import Role
    from app.modeles.message import Message


class Utilisateur(SQLModel, table=True):
   
    __tablename__ = "utilisateurs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_utilisateur: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, index=True, max_length=100)
    mot_de_passe_hash: str = Field(max_length=255)
    
    prenom: Optional[str] = Field(default=None, max_length=100)
    nom: Optional[str] = Field(default=None, max_length=100)
    
    est_actif: bool = Field(default=True)
    est_verifie: bool = Field(default=False)
    
    # Clé étrangère vers Role
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    # Relations
    role: Optional["Role"] = Relationship(back_populates="utilisateurs")
    messages: list["Message"] = Relationship(back_populates="auteur")
