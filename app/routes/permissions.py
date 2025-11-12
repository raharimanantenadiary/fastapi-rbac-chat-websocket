"""
Routes pour la gestion des permissions
CRUD et association avec les rôles
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import obtenir_session
from app.modeles.utilisateur import Utilisateur
from app.modeles.permission import Permission
from app.modeles.role_permission import RolePermission
from app.schemas.permission import PermissionCreer, PermissionLire, PermissionModifier
from app.schemas.role_permission import AttribuerPermissions
from app.utils.permissions import exiger_permission

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/", response_model=PermissionLire, status_code=status.HTTP_201_CREATED)
async def creer_permission(
    permission_data: PermissionCreer,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("gerer_permissions"))
):
    """
    Créer une nouvelle permission
    Permission requise : gerer_permissions
    """
    # Vérifier si le code existe déjà
    statement = select(Permission).where(Permission.code == permission_data.code)
    permission_existante = session.exec(statement).first()
    if permission_existante:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce code de permission existe déjà"
        )
    
    nouvelle_permission = Permission(**permission_data.model_dump())
    session.add(nouvelle_permission)
    session.commit()
    session.refresh(nouvelle_permission)
    
    return nouvelle_permission


@router.get("/", response_model=List[PermissionLire])
async def lire_permissions(
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_permissions")),
    skip: int = 0,
    limit: int = 100
):
    """
    Récupérer la liste de toutes les permissions
    Permission requise : lire_permissions
    """
    statement = select(Permission).offset(skip).limit(limit)
    permissions = session.exec(statement).all()
    return permissions


@router.get("/{permission_id}", response_model=PermissionLire)
async def lire_permission(
    permission_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_permissions"))
):
    """
    Récupérer une permission par son ID
    Permission requise : lire_permissions
    """
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission introuvable"
        )
    return permission


@router.patch("/{permission_id}", response_model=PermissionLire)
async def modifier_permission(
    permission_id: int,
    permission_data: PermissionModifier,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("gerer_permissions"))
):
    """
    Modifier une permission existante
    Permission requise : gerer_permissions
    """
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission introuvable"
        )
    
    donnees = permission_data.model_dump(exclude_unset=True)
    for key, value in donnees.items():
        setattr(permission, key, value)
    
    permission.date_modification = datetime.utcnow()
    
    session.add(permission)
    session.commit()
    session.refresh(permission)
    
    return permission


@router.delete("/{permission_id}")
async def supprimer_permission(
    permission_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("gerer_permissions"))
):
    """
    Supprimer une permission
    Permission requise : gerer_permissions
    """
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission introuvable"
        )
    
    # Supprimer d'abord toutes les associations RolePermission
    statement = select(RolePermission).where(RolePermission.permission_id == permission_id)
    associations = session.exec(statement).all()
    for association in associations:
        session.delete(association)
    
    session.delete(permission)
    session.commit()
    
    return {"message": "Permission supprimée avec succès"}


@router.post("/attribuer", status_code=status.HTTP_200_OK)
async def attribuer_permissions_a_role(
    donnees: AttribuerPermissions,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("gerer_permissions"))
):
    """
    Attribuer plusieurs permissions à un rôle
    Permission requise : gerer_permissions
    """
    # Supprimer les anciennes associations
    statement = select(RolePermission).where(RolePermission.role_id == donnees.role_id)
    anciennes_associations = session.exec(statement).all()
    for association in anciennes_associations:
        session.delete(association)
    
    # Créer les nouvelles associations
    for permission_id in donnees.permissions_ids:
        nouvelle_association = RolePermission(
            role_id=donnees.role_id,
            permission_id=permission_id
        )
        session.add(nouvelle_association)
    
    session.commit()
    
    return {"message": f"{len(donnees.permissions_ids)} permission(s) attribuée(s) avec succès"}
