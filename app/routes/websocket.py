"""
Routes WebSocket pour le chat en temps réel
Gestion des connexions et diffusion des messages
"""
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, status
from sqlmodel import Session, select
from jose import jwt, JWTError

from app.database import obtenir_session
from app.modeles.utilisateur import Utilisateur
from app.modeles.canal import Canal
from app.modeles.message import Message
from app.services.websocket import gestionnaire
from app.services.rbac import utilisateur_a_permission
from app.config import parametres

router = APIRouter(prefix="/ws", tags=["WebSocket Chat"])


async def obtenir_utilisateur_depuis_token(token: str, session: Session) -> Utilisateur:
  
    try:
        payload = jwt.decode(token, parametres.SECRET_KEY, algorithms=[parametres.ALGORITHM])
        nom_utilisateur: str = payload.get("sub")
        
        if nom_utilisateur is None:
            raise Exception("Token invalide")
        
        statement = select(Utilisateur).where(Utilisateur.nom_utilisateur == nom_utilisateur)
        utilisateur = session.exec(statement).first()
        
        if utilisateur is None:
            raise Exception("Utilisateur introuvable")
        
        if not utilisateur.est_actif:
            raise Exception("Utilisateur inactif")
        
        return utilisateur
        
    except JWTError:
        raise Exception("Token invalide")


@router.websocket("/chat/{canal_id}")
async def websocket_chat(
    websocket: WebSocket,
    canal_id: int,
    token: str = Query(...),
    session: Session = Depends(obtenir_session)
):
   
    
    try:
        # Authentifier l'utilisateur via le token
        utilisateur = await obtenir_utilisateur_depuis_token(token, session)
        
        # Vérifier que l'utilisateur a la permission de lire les messages
        if not utilisateur_a_permission(session, utilisateur, "lire_messages"):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        # Vérifier que le canal existe
        canal = session.get(Canal, canal_id)
        if not canal:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        # Connecter l'utilisateur au canal
        await gestionnaire.connecter(
            websocket, 
            canal_id, 
            {
                "id": utilisateur.id,
                "nom_utilisateur": utilisateur.nom_utilisateur,
                "prenom": utilisateur.prenom,
                "nom": utilisateur.nom
            }
        )
        
        # Envoyer un message de bienvenue
        await gestionnaire.envoyer_message_personnel(
            websocket,
            {
                "type": "connexion",
                "message": f"Bienvenue dans le canal #{canal.nom}",
                "canal_id": canal_id,
                "utilisateurs_connectes": gestionnaire.obtenir_nombre_utilisateurs(canal_id)
            }
        )
        
        # Notifier les autres utilisateurs
        await gestionnaire.diffuser_message(
            {
                "type": "notification",
                "message": f"{utilisateur.nom_utilisateur} a rejoint le canal",
                "canal_id": canal_id,
                "utilisateurs_connectes": gestionnaire.obtenir_nombre_utilisateurs(canal_id)
            },
            canal_id
        )
        
        # Boucle de réception des messages
        while True:
            # Recevoir un message du client
            data = await websocket.receive_json()
            
            # Vérifier que l'utilisateur a la permission d'envoyer des messages
            if not utilisateur_a_permission(session, utilisateur, "envoyer_messages"):
                await gestionnaire.envoyer_message_personnel(
                    websocket,
                    {
                        "type": "erreur",
                        "message": "Permission refusée pour envoyer des messages"
                    }
                )
                continue
            
            # Extraire le contenu du message
            contenu = data.get("contenu", "")
            if not contenu or not contenu.strip():
                continue
            
            # Sauvegarder le message dans la base de données
            nouveau_message = Message(
                contenu=contenu.strip(),
                auteur_id=utilisateur.id,
                canal_id=canal_id,
                type_message=data.get("type_message", "texte"),
                url_fichier=data.get("url_fichier")
            )
            
            session.add(nouveau_message)
            session.commit()
            session.refresh(nouveau_message)
            
            # Diffuser le message à tous les utilisateurs du canal
            await gestionnaire.diffuser_message(
                {
                    "type": "message",
                    "id": nouveau_message.id,
                    "contenu": nouveau_message.contenu,
                    "canal_id": canal_id,
                    "auteur": {
                        "id": utilisateur.id,
                        "nom_utilisateur": utilisateur.nom_utilisateur,
                        "prenom": utilisateur.prenom,
                        "nom": utilisateur.nom
                    },
                    "date_creation": nouveau_message.date_creation.isoformat(),
                    "est_modifie": nouveau_message.est_modifie
                },
                canal_id
            )
    
    except WebSocketDisconnect:
        # L'utilisateur s'est déconnecté
        gestionnaire.deconnecter(websocket, canal_id)
        
        # Notifier les autres utilisateurs
        await gestionnaire.diffuser_message(
            {
                "type": "notification",
                "message": f"{utilisateur.nom_utilisateur} a quitté le canal",
                "canal_id": canal_id,
                "utilisateurs_connectes": gestionnaire.obtenir_nombre_utilisateurs(canal_id)
            },
            canal_id
        )
    
    except Exception as e:
        print(f"Erreur WebSocket: {e}")
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except:
            pass


@router.get("/canaux/{canal_id}/utilisateurs")
async def obtenir_utilisateurs_connectes(
    canal_id: int
):
    
    utilisateurs = gestionnaire.obtenir_utilisateurs_canal(canal_id)
    return {
        "canal_id": canal_id,
        "nombre_utilisateurs": len(utilisateurs),
        "utilisateurs": utilisateurs
    }
