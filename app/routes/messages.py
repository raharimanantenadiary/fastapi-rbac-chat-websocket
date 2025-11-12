"""
Routes pour la gestion des messages
CRUD et récupération de l'historique
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import obtenir_session
from app.modeles.utilisateur import Utilisateur
from app.modeles.message import Message
from app.modeles.canal import Canal
from app.schemas.message import MessageCreer, MessageLire, MessageModifier, MessageAvecAuteur
from app.services.auth import obtenir_utilisateur_courant
from app.utils.permissions import exiger_permission

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=MessageLire, status_code=status.HTTP_201_CREATED)
async def creer_message(
    message_data: MessageCreer,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("envoyer_messages"))
):
    """
    Créer un nouveau message dans un canal
    Permission requise : envoyer_messages
    """
    # Vérifier que le canal existe
    canal = session.get(Canal, message_data.canal_id)
    if not canal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canal introuvable"
        )
    
    nouveau_message = Message(
        **message_data.model_dump(),
        auteur_id=utilisateur_courant.id
    )
    
    session.add(nouveau_message)
    session.commit()
    session.refresh(nouveau_message)
    
    return nouveau_message


@router.get("/canal/{canal_id}", response_model=List[MessageAvecAuteur])
async def lire_messages_canal(
    canal_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_messages")),
    skip: int = 0,
    limit: int = 100
):
    """
    Récupérer les messages d'un canal
    Permission requise : lire_messages
    """
    # Vérifier que le canal existe
    canal = session.get(Canal, canal_id)
    if not canal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canal introuvable"
        )
    
    statement = (
        select(Message, Utilisateur)
        .join(Utilisateur, Message.auteur_id == Utilisateur.id)
        .where(Message.canal_id == canal_id)
        .where(Message.est_supprime == False)
        .order_by(Message.date_creation.desc())
        .offset(skip)
        .limit(limit)
    )
    
    resultats = session.exec(statement).all()
    
    messages_avec_auteur = []
    for message, auteur in resultats:
        messages_avec_auteur.append(
            MessageAvecAuteur(
                **message.model_dump(),
                auteur_nom_utilisateur=auteur.nom_utilisateur,
                auteur_prenom=auteur.prenom,
                auteur_nom=auteur.nom
            )
        )
    
    return messages_avec_auteur


@router.get("/{message_id}", response_model=MessageLire)
async def lire_message(
    message_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("lire_messages"))
):
    """
    Récupérer un message par son ID
    Permission requise : lire_messages
    """
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message introuvable"
        )
    return message


@router.patch("/{message_id}", response_model=MessageLire)
async def modifier_message(
    message_id: int,
    message_data: MessageModifier,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("modifier_messages"))
):
    """
    Modifier un message existant
    Permission requise : modifier_messages
    """
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message introuvable"
        )
    
    # Vérifier que l'utilisateur est l'auteur du message
    if message.auteur_id != utilisateur_courant.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez modifier que vos propres messages"
        )
    
    donnees = message_data.model_dump(exclude_unset=True)
    for key, value in donnees.items():
        setattr(message, key, value)
    
    message.est_modifie = True
    message.date_modification = datetime.utcnow()
    
    session.add(message)
    session.commit()
    session.refresh(message)
    
    return message


@router.delete("/{message_id}")
async def supprimer_message(
    message_id: int,
    session: Session = Depends(obtenir_session),
    utilisateur_courant: Utilisateur = Depends(exiger_permission("supprimer_messages"))
):
    """
    Supprimer un message (soft delete)
    Permission requise : supprimer_messages
    """
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message introuvable"
        )
    
    # Marquer comme supprimé au lieu de supprimer réellement
    message.est_supprime = True
    message.date_modification = datetime.utcnow()
    
    session.add(message)
    session.commit()
    
    return {"message": "Message supprimé avec succès"}
