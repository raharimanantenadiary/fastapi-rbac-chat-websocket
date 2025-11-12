"""
Package des services
Logique métier de l'application
"""
from app.services.securite import hacher_mot_de_passe, verifier_mot_de_passe
from app.services.auth import (
    creer_token_acces,
    decoder_token,
    authentifier_utilisateur,
    obtenir_utilisateur_courant,
    obtenir_utilisateur_courant_actif,
    oauth2_scheme
)
from app.services.rbac import (
    obtenir_permissions_utilisateur,
    utilisateur_a_permission,
    verifier_permission,
    utilisateur_a_role,
    verifier_role
)
from app.services.websocket import gestionnaire

__all__ = [
    # Sécurité
    "hacher_mot_de_passe",
    "verifier_mot_de_passe",
    # Authentification
    "creer_token_acces",
    "decoder_token",
    "authentifier_utilisateur",
    "obtenir_utilisateur_courant",
    "obtenir_utilisateur_courant_actif",
    "oauth2_scheme",
    # RBAC
    "obtenir_permissions_utilisateur",
    "utilisateur_a_permission",
    "verifier_permission",
    "utilisateur_a_role",
    "verifier_role",
    # WebSocket
    "gestionnaire"
]
