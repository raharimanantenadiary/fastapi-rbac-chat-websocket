"""
Dépendances FastAPI pour la vérification des permissions
À utiliser avec Depends() dans les routes
"""
from typing import Callable
from fastapi import Depends
from sqlmodel import Session

from app.database import obtenir_session
from app.modeles.utilisateur import Utilisateur
from app.services.auth import obtenir_utilisateur_courant
from app.services.rbac import verifier_permission, verifier_role


def exiger_permission(permission_requise: str) -> Callable:
    
    async def verification_permission(
        utilisateur: Utilisateur = Depends(obtenir_utilisateur_courant),
        session: Session = Depends(obtenir_session)
    ) -> Utilisateur:
        verifier_permission(session, utilisateur, permission_requise)
        return utilisateur
    
    return verification_permission


def exiger_role(nom_role: str) -> Callable:
   
    async def verification_role(
        utilisateur: Utilisateur = Depends(obtenir_utilisateur_courant),
        session: Session = Depends(obtenir_session)
    ) -> Utilisateur:
        verifier_role(utilisateur, nom_role, session)
        return utilisateur
    
    return verification_role


def exiger_plusieurs_permissions(*permissions_requises: str) -> Callable:
   
    async def verification_permissions_multiples(
        utilisateur: Utilisateur = Depends(obtenir_utilisateur_courant),
        session: Session = Depends(obtenir_session)
    ) -> Utilisateur:
        for permission in permissions_requises:
            verifier_permission(session, utilisateur, permission)
        return utilisateur
    
    return verification_permissions_multiples
