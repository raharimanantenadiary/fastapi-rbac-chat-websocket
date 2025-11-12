"""
Routes pour la gestion des canaux de chat
CRUD complet avec vérification des permissions
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import obtenir_session
from app.modeles.utilisateur import Utilisateur
from app.modeles.canal import Canal
from app.schemas.canal import CanalCreer, CanalLire, CanalModifier
from app.services.auth import obtenir_utilisateur_courant
from app.utils.permissions import exiger_permission

router = APIRouter(prefix="/canaux", tags=["Canaux"])


@router.post("/", response_model=CanalLire, status_code=status.HTTP_201_CREATED)
async def creer_canal(
    canal_data: CanalCreer,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("creer_canaux"))
):
    """
    Créer un nouveau canal
    Permission requise : creer_canaux
    """
    # Vérifier si le nom existe déjà
    statement = select(Canal).where(Canal.nom == canal_data.nom)
    canal_existant = session.exec(statement).first()
    if canal_existant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce nom de canal existe déjà"
        )
    
    nouveau_canal = Canal(
        **canal_data.model_dump(),
        createur_id=utilisateur_courant.id
    )
    
    session.add(nouveau_canal)
    session.commit()
    session.refresh(nouveau_canal)
    
    return nouveau_canal


@router.get("/", response_model=List[CanalLire])
async def lire_canaux(
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_canaux")),
    skip: int = 0,
    limit: int = 100
):
    """
    Récupérer la liste de tous les canaux
    Permission requise : lire_canaux
    """
    statement = select(Canal).where(Canal.est_actif == True).offset(skip).limit(limit)
    canaux = session.exec(statement).all()
    return canaux


@router.get("/{canal_id}", response_model=CanalLire)
async def lire_canal(
    canal_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_canaux"))
):
    """
    Récupérer un canal par son ID
    Permission requise : lire_canaux
    """
    canal = session.get(Canal, canal_id)
    if not canal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canal introuvable"
        )
    return canal


@router.patch("/{canal_id}", response_model=CanalLire)
async def modifier_canal(
    canal_id: int,
    canal_data: CanalModifier,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("modifier_canaux"))
):
    """
    Modifier un canal existant
    Permission requise : modifier_canaux
    """
    canal = session.get(Canal, canal_id)
    if not canal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canal introuvable"
        )
    
    donnees = canal_data.model_dump(exclude_unset=True)
    for key, value in donnees.items():
        setattr(canal, key, value)
    
    canal.date_modification = datetime.utcnow()
    
    session.add(canal)
    session.commit()
    session.refresh(canal)
    
    return canal


@router.delete("/{canal_id}")
async def supprimer_canal(
    canal_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("supprimer_canaux"))
):
    """
    Supprimer un canal
    Permission requise : supprimer_canaux
    """
    canal = session.get(Canal, canal_id)
    if not canal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canal introuvable"
        )
    
    session.delete(canal)
    session.commit()
    
    return {"message": "Canal supprimé avec succès"}
