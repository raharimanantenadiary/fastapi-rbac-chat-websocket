"""
Service d'authentification JWT
Gestion des tokens JWT et authentification des utilisateurs
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.config import parametres
from app.database import obtenir_session
from app.modeles.utilisateur import Utilisateur
from app.schemas.auth import TokenData
from app.services.securite import verifier_mot_de_passe


# Schéma OAuth2 pour récupérer le token depuis le header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def creer_token_acces(data: dict, expires_delta: Optional[timedelta] = None) -> str:
   
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=parametres.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, parametres.SECRET_KEY, algorithm=parametres.ALGORITHM)
    
    return encoded_jwt


def decoder_token(token: str) -> TokenData:
 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, parametres.SECRET_KEY, algorithms=[parametres.ALGORITHM])
        nom_utilisateur: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if nom_utilisateur is None:
            raise credentials_exception
            
        token_data = TokenData(nom_utilisateur=nom_utilisateur, user_id=user_id)
        return token_data
        
    except JWTError:
        raise credentials_exception


def authentifier_utilisateur(
    session: Session, 
    nom_utilisateur: str, 
    mot_de_passe: str
) -> Optional[Utilisateur]:
    
    statement = select(Utilisateur).where(Utilisateur.nom_utilisateur == nom_utilisateur)
    utilisateur = session.exec(statement).first()
    
    if not utilisateur:
        return None
    
    if not verifier_mot_de_passe(mot_de_passe, utilisateur.mot_de_passe_hash):
        return None
    
    return utilisateur


async def obtenir_utilisateur_courant(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(obtenir_session)
) -> Utilisateur:
   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Décoder le token
    token_data = decoder_token(token)
    
    # Récupérer l'utilisateur depuis la base de données
    statement = select(Utilisateur).where(Utilisateur.nom_utilisateur == token_data.nom_utilisateur)
    utilisateur = session.exec(statement).first()
    
    if utilisateur is None:
        raise credentials_exception
    
    # Vérifier que l'utilisateur est actif
    if not utilisateur.est_actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inactif"
        )
    
    return utilisateur


async def obtenir_utilisateur_courant_actif(
    utilisateur_courant: Utilisateur = Depends(obtenir_utilisateur_courant)
) -> Utilisateur:
   
    if not utilisateur_courant.est_actif:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif"
        )
    return utilisateur_courant
