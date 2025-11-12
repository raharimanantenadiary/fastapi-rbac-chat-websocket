"""
Gestionnaire de connexions WebSocket
Gère les connexions actives et la diffusion des messages
"""
from typing import Dict, List
from fastapi import WebSocket


class GestionnaireConnexions:
  
    def __init__(self):
        # Dictionnaire : canal_id -> liste de WebSocket connectées
        self.connexions_actives: Dict[int, List[WebSocket]] = {}
        # Dictionnaire : WebSocket -> utilisateur info
        self.utilisateurs_connectes: Dict[WebSocket, dict] = {}
    
    async def connecter(self, websocket: WebSocket, canal_id: int, utilisateur: dict):
      
        await websocket.accept()
        
        # Ajouter la connexion au canal
        if canal_id not in self.connexions_actives:
            self.connexions_actives[canal_id] = []
        
        self.connexions_actives[canal_id].append(websocket)
        
        # Enregistrer l'utilisateur
        self.utilisateurs_connectes[websocket] = {
            **utilisateur,
            "canal_id": canal_id
        }
    
    def deconnecter(self, websocket: WebSocket, canal_id: int):
      
        if canal_id in self.connexions_actives:
            self.connexions_actives[canal_id].remove(websocket)
            
            # Supprimer le canal s'il est vide
            if not self.connexions_actives[canal_id]:
                del self.connexions_actives[canal_id]
        
        # Supprimer l'utilisateur
        if websocket in self.utilisateurs_connectes:
            del self.utilisateurs_connectes[websocket]
    
    async def diffuser_message(self, message: dict, canal_id: int):
       
        if canal_id not in self.connexions_actives:
            return
        
        # Copier la liste pour éviter les modifications pendant l'itération
        connexions = self.connexions_actives[canal_id].copy()
        
        for connexion in connexions:
            try:
                await connexion.send_json(message)
            except Exception as e:
                print(f"Erreur lors de l'envoi du message: {e}")
                # Retirer la connexion si elle est fermée
                self.deconnecter(connexion, canal_id)
    
    async def envoyer_message_personnel(self, websocket: WebSocket, message: dict):
      
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Erreur lors de l'envoi du message personnel: {e}")
    
    def obtenir_nombre_utilisateurs(self, canal_id: int) -> int:
        
        if canal_id not in self.connexions_actives:
            return 0
        return len(self.connexions_actives[canal_id])
    
    def obtenir_utilisateurs_canal(self, canal_id: int) -> List[dict]:
       
        if canal_id not in self.connexions_actives:
            return []
        
        utilisateurs = []
        for connexion in self.connexions_actives[canal_id]:
            if connexion in self.utilisateurs_connectes:
                utilisateurs.append(self.utilisateurs_connectes[connexion])
        
        return utilisateurs


# Instance globale du gestionnaire
gestionnaire = GestionnaireConnexions()
