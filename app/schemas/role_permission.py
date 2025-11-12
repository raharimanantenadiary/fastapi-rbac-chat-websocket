"""
Schémas Pydantic pour RolePermission
Validation des données entrantes/sortantes
"""
from datetime import datetime
from pydantic import BaseModel


class RolePermissionCreer(BaseModel):
    """Schéma pour associer une permission à un rôle"""
    role_id: int
    permission_id: int


class RolePermissionLire(RolePermissionCreer):
    """Schéma pour lire une association rôle-permission"""
    id: int
    date_attribution: datetime

    class Config:
        from_attributes = True


class AttribuerPermissions(BaseModel):
    """Schéma pour attribuer plusieurs permissions à un rôle"""
    role_id: int
    permissions_ids: list[int]
