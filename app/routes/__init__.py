"""
Package des routes
Exporte tous les routers de l'application
"""
from app.routes.auth import router as router_auth
from app.routes.utilisateurs import router as router_utilisateurs
from app.routes.roles import router as router_roles
from app.routes.permissions import router as router_permissions
from app.routes.canaux import router as router_canaux
from app.routes.messages import router as router_messages
from app.routes.websocket import router as router_websocket

__all__ = [
    "router_auth",
    "router_utilisateurs",
    "router_roles",
    "router_permissions",
    "router_canaux",
    "router_messages",
    "router_websocket"
]
