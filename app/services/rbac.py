"""
Service RBAC (Role-Based Access Control)
Gestion des permissions et vérification des accès
"""
from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.modeles.utilisateur import Utilisateur
from app.modeles.role import Role
from app.modeles.permission import Permission
from app.modeles.role_permission import RolePermission


def obtenir_permissions_utilisateur(session: Session, utilisateur: Utilisateur) -> List[str]:
   
    if not utilisateur.role_id:
        return []
    
    # Requête pour récupérer toutes les permissions du rôle de l'utilisateur
    statement = (
        select(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .where(RolePermission.role_id == utilisateur.role_id)
        .where(Permission.est_actif == True)
    )
    
    permissions = session.exec(statement).all()
    return list(permissions)


def utilisateur_a_permission(
    session: Session, 
    utilisateur: Utilisateur, 
    permission_requise: str
) -> bool:
   
    permissions = obtenir_permissions_utilisateur(session, utilisateur)
    return permission_requise in permissions


def verifier_permission(
    session: Session, 
    utilisateur: Utilisateur, 
    permission_requise: str
) -> None:
    
    if not utilisateur_a_permission(session, utilisateur, permission_requise):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission refusée. Permission requise : {permission_requise}"
        )


def utilisateur_a_role(utilisateur: Utilisateur, nom_role: str, session: Session) -> bool:
   
    if not utilisateur.role_id:
        return False
    
    statement = select(Role).where(Role.id == utilisateur.role_id)
    role = session.exec(statement).first()
    
    if not role:
        return False
    
    return role.nom.lower() == nom_role.lower()


def verifier_role(utilisateur: Utilisateur, nom_role: str, session: Session) -> None:
   
    if not utilisateur_a_role(utilisateur, nom_role, session):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Accès refusé. Rôle requis : {nom_role}"
        )
