"""
Routes d'authentification
Login, logout, changement de mot de passe
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database import obtenir_session
from app.schemas.auth import Token, LoginForm, ChangerMotDePasse
from app.schemas.utilisateur import UtilisateurLire
from app.services.auth import (
    authentifier_utilisateur,
    creer_token_acces,
    obtenir_utilisateur_courant
)
from app.services.securite import hacher_mot_de_passe, verifier_mot_de_passe
from app.config import parametres

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(obtenir_session)
):
    """
    Connexion d'un utilisateur et génération du token JWT
    """
    utilisateur = authentifier_utilisateur(
        session, 
        form_data.username, 
        form_data.password
    )
    
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not utilisateur.est_actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé"
        )
    
    # Créer le token JWT
    access_token_expires = timedelta(minutes=parametres.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = creer_token_acces(
        data={"sub": utilisateur.nom_utilisateur, "user_id": utilisateur.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/moi", response_model=UtilisateurLire)
async def lire_utilisateur_courant(
    utilisateur_courant = Depends(obtenir_utilisateur_courant)
):
    """
    Récupère les informations de l'utilisateur connecté
    """
    return utilisateur_courant


@router.post("/changer-mot-de-passe")
async def changer_mot_de_passe(
    donnees: ChangerMotDePasse,
    utilisateur_courant = Depends(obtenir_utilisateur_courant),
    session: Session = Depends(obtenir_session)
):
    """
    Permet à un utilisateur de changer son mot de passe
    """
    # Vérifier l'ancien mot de passe
    if not verifier_mot_de_passe(donnees.ancien_mot_de_passe, utilisateur_courant.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ancien mot de passe incorrect"
        )
    
    # Hacher et enregistrer le nouveau mot de passe
    utilisateur_courant.mot_de_passe_hash = hacher_mot_de_passe(donnees.nouveau_mot_de_passe)
    session.add(utilisateur_courant)
    session.commit()
    
    return {"message": "Mot de passe modifié avec succès"}
