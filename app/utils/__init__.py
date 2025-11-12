"""
Package des utilitaires
Fonctions et dépendances utiles
"""
from app.utils.permissions import (
    exiger_permission,
    exiger_role,
    exiger_plusieurs_permissions
)

__all__ = [
    "exiger_permission",
    "exiger_role",
    "exiger_plusieurs_permissions"
]
