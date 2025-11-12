"""
Point d'entrée principal de l'application FastAPI
Gestion RBAC et Chat en temps réel
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import parametres
from app.database import creer_tables
from app.routes import (
    router_auth,
    router_utilisateurs,
    router_roles,
    router_permissions,
    router_canaux,
    router_messages,
    router_websocket
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire du cycle de vie de l'application
    Exécuté au démarrage et à l'arrêt
    """
    # Démarrage : création des tables
    print(" Démarrage de l'application...")
    creer_tables()
    print(f" Base de données : {parametres.DATABASE_URL.split('@')[1]}")
    
    # Exécuter le seed automatiquement au premier démarrage
    try:
        from seed import executer_seed
        executer_seed()
    except Exception as e:
        print(f"⚠  Seed déjà exécuté ou erreur: {e}")
    
    yield
    
    # Arrêt : nettoyage si nécessaire
    print(" Arrêt de l'application...")


# Création de l'application FastAPI
app = FastAPI(
    title=parametres.PROJECT_NAME,
    description="API de gestion des utilisateurs, rôles, permissions et chat en temps réel",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS (pour permettre les requêtes depuis un front-end)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(router_auth)
app.include_router(router_utilisateurs)
app.include_router(router_roles)
app.include_router(router_permissions)
app.include_router(router_canaux)
app.include_router(router_messages)
app.include_router(router_websocket)


@app.get("/", tags=["Racine"])
async def racine():
    """
    Endpoint racine de l'API
    """
    return {
        "message": "Bienvenue sur l'API Gestion RBAC Chat",
        "version": "1.0.0",
        "docs": "/docs",
        "status": " Opérationnel",
        "endpoints": {
            "auth": "/auth",
            "utilisateurs": "/utilisateurs",
            "roles": "/roles",
            "permissions": "/permissions",
            "canaux": "/canaux",
            "messages": "/messages",
            "websocket": "ws://localhost:8000/ws/chat/{canal_id}?token=YOUR_TOKEN"
        }
    }


@app.get("/sante", tags=["Santé"])
async def verification_sante():
    """
    Endpoint pour vérifier l'état de l'API
    """
    return {
        "status": "healthy",
        "database": "connected",
        "message": "L'API fonctionne correctement"
    }


# Point d'entrée pour lancer l'application
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=parametres.DEBUG
    )
