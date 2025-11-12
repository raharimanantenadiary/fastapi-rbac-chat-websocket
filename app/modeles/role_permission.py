"""
Modèle RolePermission
Table d'association entre Role et Permission (relation Many-to-Many)
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modeles.role import Role
    from app.modeles.permission import Permission


class RolePermission(SQLModel, table=True):
   
    __tablename__ = "roles_permissions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Clés étrangères
    role_id: int = Field(foreign_key="roles.id", index=True)
    permission_id: int = Field(foreign_key="permissions.id", index=True)
    
    # Date d'attribution de la permission au rôle
    date_attribution: datetime = Field(default_factory=datetime.utcnow)
    
    # Relations
    role: "Role" = Relationship(back_populates="permissions_associees")
    permission: "Permission" = Relationship(back_populates="roles_associes")
