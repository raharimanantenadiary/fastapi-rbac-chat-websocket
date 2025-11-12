"""
Routes pour la gestion des utilisateurs
CRUD complet avec vérification des permissions
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import obtenir_session
from app.modeles.utilisateur import Utilisateur
from app.schemas.utilisateur import (
    UtilisateurCreer,
    UtilisateurLire,
    UtilisateurModifier,
    UtilisateurAvecRole
)
from app.services.auth import obtenir_utilisateur_courant
from app.services.securite import hacher_mot_de_passe
from app.utils.permissions import exiger_permission

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])


@router.post("/", response_model=UtilisateurLire, status_code=status.HTTP_201_CREATED)
async def creer_utilisateur(
    utilisateur_data: UtilisateurCreer,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("creer_utilisateurs"))
):
    """
    Créer un nouvel utilisateur
    Permission requise : creer_utilisateurs
    """
    # Vérifier si le nom d'utilisateur existe déjà
    statement = select(Utilisateur).where(Utilisateur.nom_utilisateur == utilisateur_data.nom_utilisateur)
    utilisateur_existant = session.exec(statement).first()
    if utilisateur_existant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce nom d'utilisateur existe déjà"
        )
    
    # Vérifier si l'email existe déjà
    statement = select(Utilisateur).where(Utilisateur.email == utilisateur_data.email)
    email_existant = session.exec(statement).first()
    if email_existant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email existe déjà"
        )
    
    # Créer l'utilisateur
    mot_de_passe_hash = hacher_mot_de_passe(utilisateur_data.mot_de_passe)
    nouvel_utilisateur = Utilisateur(
        nom_utilisateur=utilisateur_data.nom_utilisateur,
        email=utilisateur_data.email,
        mot_de_passe_hash=mot_de_passe_hash,
        prenom=utilisateur_data.prenom,
        nom=utilisateur_data.nom,
        role_id=utilisateur_data.role_id
    )
    
    session.add(nouvel_utilisateur)
    session.commit()
    session.refresh(nouvel_utilisateur)
    
    return nouvel_utilisateur


@router.get("/", response_model=List[UtilisateurLire])
async def lire_utilisateurs(
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_utilisateurs")),
    skip: int = 0,
    limit: int = 100
):
    """
    Récupérer la liste de tous les utilisateurs
    Permission requise : lire_utilisateurs
    """
    statement = select(Utilisateur).offset(skip).limit(limit)
    utilisateurs = session.exec(statement).all()
    return utilisateurs


@router.get("/{utilisateur_id}", response_model=UtilisateurLire)
async def lire_utilisateur(
    utilisateur_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_utilisateurs"))
):
    """
    Récupérer un utilisateur par son ID
    Permission requise : lire_utilisateurs
    """
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )
    return utilisateur


@router.patch("/{utilisateur_id}", response_model=UtilisateurLire)
async def modifier_utilisateur(
    utilisateur_id: int,
    utilisateur_data: UtilisateurModifier,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("modifier_utilisateurs"))
):
    """
    Modifier un utilisateur existant
    Permission requise : modifier_utilisateurs
    """
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )
    
    # Mettre à jour les champs fournis
    donnees = utilisateur_data.model_dump(exclude_unset=True)
    for key, value in donnees.items():
        setattr(utilisateur, key, value)
    
    utilisateur.date_modification = datetime.utcnow()
    
    session.add(utilisateur)
    session.commit()
    session.refresh(utilisateur)
    
    return utilisateur


@router.delete("/{utilisateur_id}")
async def supprimer_utilisateur(
    utilisateur_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("supprimer_utilisateurs"))
):
    """
    Supprimer un utilisateur
    Permission requise : supprimer_utilisateurs
    """
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )
    
    # Empêcher de se supprimer soi-même
    if utilisateur.id == utilisateur_courant.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous ne pouvez pas supprimer votre propre compte"
        )
    
    session.delete(utilisateur)
    session.commit()
    
    return {"message": "Utilisateur supprimé avec succès"}
