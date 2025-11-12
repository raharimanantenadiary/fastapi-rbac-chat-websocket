"""
Modèle Canal
Table des canaux de chat (général, support, admin, etc.)
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modeles.message import Message


class Canal(SQLModel, table=True):
   
    __tablename__ = "canaux"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    
    # Type de canal : public, privé, groupe
    type_canal: str = Field(default="public", max_length=20)
    
    # Restriction d'accès par rôle (optionnel)
    # Si None, accessible à tous
    role_minimum_requis: Optional[str] = Field(default=None, max_length=50)
    
    est_actif: bool = Field(default=True)
    
    # ID du créateur du canal
    createur_id: Optional[int] = Field(default=None, foreign_key="utilisateurs.id")
    
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    # Relations
    messages: list["Message"] = Relationship(back_populates="canal")
