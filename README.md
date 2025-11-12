# 💬 Gestion RBAC Chat - Projet FastAPI

Système complet de gestion des utilisateurs, rôles, permissions (RBAC) et chat en temps réel avec FastAPI, PostgreSQL et WebSocket.


##  Fonctionnalités

###  Authentification & Autorisation
- Authentification JWT sécurisée
- Système RBAC (Role-Based Access Control)
- Gestion des rôles et permissions granulaires
- Middleware de vérification des permissions

###  Gestion des utilisateurs
- CRUD complet des utilisateurs
- Activation/désactivation des comptes
- Vérification des emails
- Changement de mot de passe sécurisé

###  Gestion des rôles
- CRUD des rôles
- Attribution dynamique des permissions
- 4 rôles par défaut : Admin, Modérateur, Utilisateur, Invité
- 16 permissions prédéfinies

###  Chat en temps réel
- WebSocket pour communication instantanée
- Support multi-canaux
- Notifications de connexion/déconnexion
- Historique des messages persistant
- Permissions RBAC sur le chat

###  Fonctionnalités supplémentaires
- Documentation Swagger automatique
- Seed de données automatique au démarrage
- Support CORS pour intégration front-end
- Interface de test HTML incluse



##  Documentation API

### Endpoints principaux

####  Authentification (`/auth`)
- `POST /auth/login` - Connexion et obtention du token JWT
- `GET /auth/moi` - Informations de l'utilisateur connecté
- `POST /auth/changer-mot-de-passe` - Changer son mot de passe

####  Utilisateurs (`/utilisateurs`)
- `POST /utilisateurs` - Créer un utilisateur (Permission: creer_utilisateurs)
- `GET /utilisateurs` - Lister les utilisateurs (Permission: lire_utilisateurs)
- `GET /utilisateurs/{id}` - Obtenir un utilisateur
- `PATCH /utilisateurs/{id}` - Modifier un utilisateur
- `DELETE /utilisateurs/{id}` - Supprimer un utilisateur

####  Rôles (`/roles`)
- `POST /roles` - Créer un rôle (Permission: gerer_roles)
- `GET /roles` - Lister les rôles (Permission: lire_roles)
- `GET /roles/{id}` - Obtenir un rôle
- `PATCH /roles/{id}` - Modifier un rôle
- `DELETE /roles/{id}` - Supprimer un rôle

####  Permissions (`/permissions`)
- `POST /permissions` - Créer une permission (Permission: gerer_permissions)
- `GET /permissions` - Lister les permissions (Permission: lire_permissions)
- `POST /permissions/attribuer` - Attribuer des permissions à un rôle

####  Canaux (`/canaux`)
- `POST /canaux` - Créer un canal (Permission: creer_canaux)
- `GET /canaux` - Lister les canaux (Permission: lire_canaux)
- `GET /canaux/{id}` - Obtenir un canal
- `PATCH /canaux/{id}` - Modifier un canal
- `DELETE /canaux/{id}` - Supprimer un canal

####  Messages (`/messages`)
- `POST /messages` - Envoyer un message (Permission: envoyer_messages)
- `GET /messages/canal/{canal_id}` - Historique d'un canal
- `GET /messages/{id}` - Obtenir un message
- `PATCH /messages/{id}` - Modifier un message
- `DELETE /messages/{id}` - Supprimer un message (soft delete)

#### 🔌 WebSocket (`/ws`)
- `WS /ws/chat/{canal_id}?token=JWT` - Connexion WebSocket pour chat temps réel
- `GET /ws/canaux/{canal_id}/utilisateurs` - Utilisateurs connectés

---

##  Structure du projet

```
gestion_rbac_chat/
│
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration de l'application
│   ├── database.py            # Connexion PostgreSQL
│   │
│   ├── modeles/               # Modèles SQLModel (tables)
│   │   ├── utilisateur.py
│   │   ├── role.py
│   │   ├── permission.py
│   │   ├── role_permission.py
│   │   ├── canal.py
│   │   └── message.py
│   │
│   ├── schemas/               # Schémas Pydantic (validation)
│   │   ├── utilisateur.py
│   │   ├── role.py
│   │   ├── permission.py
│   │   ├── role_permission.py
│   │   ├── canal.py
│   │   ├── message.py
│   │   └── auth.py
│   │
│   ├── routes/                # Routes API
│   │   ├── auth.py
│   │   ├── utilisateurs.py
│   │   ├── roles.py
│   │   ├── permissions.py
│   │   ├── canaux.py
│   │   ├── messages.py
│   │   └── websocket.py
│   │
│   ├── services/              # Logique métier
│   │   ├── securite.py        # Hachage mots de passe
│   │   ├── auth.py            # Authentification JWT
│   │   ├── rbac.py            # Gestion permissions
│   │   └── websocket.py       # Gestionnaire WebSocket
│   │
│   └── utils/                 # Utilitaires
│       └── permissions.py     # Dépendances FastAPI
│
├── main.py                    # Point d'entrée
├── seed.py                    # Initialisation des données
├── test_chat.html             # Interface de test
├── requirements.txt           # Dépendances Python
├── .env                       # Variables d'environnement
├── .gitignore
└── README.md
```


### Tester le WebSocket

1. Ouvrir `chat.html` dans un navigateur
2. Se connecter avec admin/admin123
3. Sélectionner un canal
4. Envoyer des messages
