"""
Routes pour la gestion des rôles
CRUD complet avec vérification des permissions
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import obtenir_session
from app.modeles.utilisateur import Utilisateur
from app.modeles.role import Role
from app.schemas.role import RoleCreer, RoleLire, RoleModifier
from app.utils.permissions import exiger_permission

router = APIRouter(prefix="/roles", tags=["Rôles"])


@router.post("/", response_model=RoleLire, status_code=status.HTTP_201_CREATED)
async def creer_role(
    role_data: RoleCreer,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("gerer_roles"))
):
    """
    Créer un nouveau rôle
    Permission requise : gerer_roles
    """
    # Vérifier si le nom existe déjà
    statement = select(Role).where(Role.nom == role_data.nom)
    role_existant = session.exec(statement).first()
    if role_existant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce nom de rôle existe déjà"
        )
    
    nouveau_role = Role(**role_data.model_dump())
    session.add(nouveau_role)
    session.commit()
    session.refresh(nouveau_role)
    
    return nouveau_role


@router.get("/", response_model=List[RoleLire])
async def lire_roles(
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_roles")),
    skip: int = 0,
    limit: int = 100
):
    """
    Récupérer la liste de tous les rôles
    Permission requise : lire_roles
    """
    statement = select(Role).offset(skip).limit(limit)
    roles = session.exec(statement).all()
    return roles


@router.get("/{role_id}", response_model=RoleLire)
async def lire_role(
    role_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_roles"))
):
    """
    Récupérer un rôle par son ID
    Permission requise : lire_roles
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rôle introuvable"
        )
    return role


@router.patch("/{role_id}", response_model=RoleLire)
async def modifier_role(
    role_id: int,
    role_data: RoleModifier,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("gerer_roles"))
):
    """
    Modifier un rôle existant
    Permission requise : gerer_roles
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rôle introuvable"
        )
    
    donnees = role_data.model_dump(exclude_unset=True)
    for key, value in donnees.items():
        setattr(role, key, value)
    
    role.date_modification = datetime.utcnow()
    
    session.add(role)
    session.commit()
    session.refresh(role)
    
    return role


@router.delete("/{role_id}")
async def supprimer_role(
    role_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("gerer_roles"))
):
    """
    Supprimer un rôle
    Permission requise : gerer_roles
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rôle introuvable"
        )
    
    # Vérifier qu'aucun utilisateur n'a ce rôle
    statement = select(Utilisateur).where(Utilisateur.role_id == role_id)
    utilisateurs_avec_role = session.exec(statement).first()
    if utilisateurs_avec_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de supprimer un rôle attribué à des utilisateurs"
        )
    
    session.delete(role)
    session.commit()
    
    return {"message": "Rôle supprimé avec succès"}
