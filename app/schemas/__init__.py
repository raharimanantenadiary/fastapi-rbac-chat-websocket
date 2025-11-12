"""
Package des schémas Pydantic
Exporte tous les schémas pour validation
"""
from app.schemas.utilisateur import (
    UtilisateurBase,
    UtilisateurCreer,
    UtilisateurModifier,
    UtilisateurLire,
    UtilisateurAvecRole
)
from app.schemas.role import (
    RoleBase,
    RoleCreer,
    RoleModifier,
    RoleLire,
    RoleAvecPermissions
)
from app.schemas.permission import (
    PermissionBase,
    PermissionCreer,
    PermissionModifier,
    PermissionLire
)
from app.schemas.role_permission import (
    RolePermissionCreer,
    RolePermissionLire,
    AttribuerPermissions
)
from app.schemas.canal import (
    CanalBase,
    CanalCreer,
    CanalModifier,
    CanalLire,
    CanalAvecStats
)
from app.schemas.message import (
    MessageBase,
    MessageCreer,
    MessageModifier,
    MessageLire,
    MessageAvecAuteur,
    MessageWebSocket
)
from app.schemas.auth import (
    LoginForm,
    Token,
    TokenData,
    ChangerMotDePasse
)

__all__ = [
    # Utilisateur
    "UtilisateurBase",
    "UtilisateurCreer",
    "UtilisateurModifier",
    "UtilisateurLire",
    "UtilisateurAvecRole",
    # Role
    "RoleBase",
    "RoleCreer",
    "RoleModifier",
    "RoleLire",
    "RoleAvecPermissions",
    # Permission
    "PermissionBase",
    "PermissionCreer",
    "PermissionModifier",
    "PermissionLire",
    # RolePermission
    "RolePermissionCreer",
    "RolePermissionLire",
    "AttribuerPermissions",
    # Canal
    "CanalBase",
    "CanalCreer",
    "CanalModifier",
    "CanalLire",
    "CanalAvecStats",
    # Message
    "MessageBase",
    "MessageCreer",
    "MessageModifier",
    "MessageLire",
    "MessageAvecAuteur",
    "MessageWebSocket",
    # Auth
    "LoginForm",
    "Token",
    "TokenData",
    "ChangerMotDePasse"
]
