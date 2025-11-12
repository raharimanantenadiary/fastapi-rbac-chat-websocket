"""
Modèle Message
Table des messages du chat
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modeles.utilisateur import Utilisateur
    from app.modeles.canal import Canal


class Message(SQLModel, table=True):
   
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    contenu: str = Field(max_length=2000)
    
    # Clés étrangères
    auteur_id: int = Field(foreign_key="utilisateurs.id", index=True)
    canal_id: int = Field(foreign_key="canaux.id", index=True)
    
    # Metadata
    est_modifie: bool = Field(default=False)
    est_supprime: bool = Field(default=False)
    
    # Type de message : texte, image, fichier, système
    type_message: str = Field(default="texte", max_length=20)
    
    # URL si c'est une image ou un fichier
    url_fichier: Optional[str] = Field(default=None, max_length=500)
    
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: Optional[datetime] = Field(default=None)
    
    # Relations
    auteur: "Utilisateur" = Relationship(back_populates="messages")
    canal: "Canal" = Relationship(back_populates="messages")
