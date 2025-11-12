# 💬 Gestion RBAC Chat - Projet FastAPI

Système complet de gestion des utilisateurs, rôles, permissions (RBAC) et chat en temps réel avec FastAPI, PostgreSQL et WebSocket.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue)

---

## 📋 Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement](#lancement)
- [Documentation API](#documentation-api)
- [Structure du projet](#structure-du-projet)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Sécurité](#sécurité)

---

## ✨ Fonctionnalités

### 🔐 Authentification & Autorisation
- Authentification JWT sécurisée
- Système RBAC (Role-Based Access Control)
- Gestion des rôles et permissions granulaires
- Middleware de vérification des permissions

### 👥 Gestion des utilisateurs
- CRUD complet des utilisateurs
- Activation/désactivation des comptes
- Vérification des emails
- Changement de mot de passe sécurisé

### 🎭 Gestion des rôles
- CRUD des rôles
- Attribution dynamique des permissions
- 4 rôles par défaut : Admin, Modérateur, Utilisateur, Invité
- 16 permissions prédéfinies

### 💬 Chat en temps réel
- WebSocket pour communication instantanée
- Support multi-canaux
- Notifications de connexion/déconnexion
- Historique des messages persistant
- Permissions RBAC sur le chat

### 📊 Fonctionnalités supplémentaires
- Documentation Swagger automatique
- Seed de données automatique au démarrage
- Support CORS pour intégration front-end
- Interface de test HTML incluse

---

## 🛠️ Technologies

- **Backend:** FastAPI 0.115.0
- **Base de données:** PostgreSQL 13+
- **ORM:** SQLModel 0.0.22
- **Authentification:** JWT (python-jose)
- **Hachage:** Bcrypt (passlib)
- **WebSocket:** Native FastAPI
- **Serveur:** Uvicorn

---

## 📦 Prérequis

- Python 3.10 ou supérieur
- PostgreSQL 13 ou supérieur
- pip (gestionnaire de paquets Python)
- Un navigateur moderne (pour l'interface de test)

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd gestion_rbac_chat
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer PostgreSQL

**Option A : Installation locale**

```sql
-- Se connecter à PostgreSQL
psql -U postgres

-- Créer la base de données
CREATE DATABASE gestion_rbac_chat;

-- Créer un utilisateur
CREATE USER rbac_user WITH PASSWORD 'motdepasse123';

-- Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE gestion_rbac_chat TO rbac_user;

-- Quitter
\q
```

**Option B : Docker**

```bash
docker run --name postgres_rbac \
  -e POSTGRES_DB=gestion_rbac_chat \
  -e POSTGRES_USER=rbac_user \
  -e POSTGRES_PASSWORD=motdepasse123 \
  -p 5432:5432 \
  -d postgres:16
```

---

## ⚙️ Configuration

### Variables d'environnement

Modifier le fichier `.env` selon votre configuration :

```env
# Base de données
DATABASE_URL=postgresql://rbac_user:motdepasse123@localhost:5432/gestion_rbac_chat

# JWT
SECRET_KEY=votre_cle_secrete_changez_moi_en_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
PROJECT_NAME=Gestion RBAC Chat
DEBUG=True
```

⚠️ **IMPORTANT** : Changez la `SECRET_KEY` en production !

Générer une clé sécurisée :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🎯 Lancement

### Démarrer l'application

```bash
python main.py
```

L'API sera disponible sur : **http://localhost:8000**

### URLs importantes

- **Documentation Swagger:** http://localhost:8000/docs
- **Documentation ReDoc:** http://localhost:8000/redoc
- **Interface de test:** Ouvrir `test_chat.html` dans un navigateur

### Compte administrateur par défaut

Le seed crée automatiquement un compte admin :
- **Username:** admin
- **Password:** admin123

⚠️ **Changez ce mot de passe en production !**

---

## 📚 Documentation API

### Endpoints principaux

#### 🔐 Authentification (`/auth`)
- `POST /auth/login` - Connexion et obtention du token JWT
- `GET /auth/moi` - Informations de l'utilisateur connecté
- `POST /auth/changer-mot-de-passe` - Changer son mot de passe

#### 👥 Utilisateurs (`/utilisateurs`)
- `POST /utilisateurs` - Créer un utilisateur (Permission: creer_utilisateurs)
- `GET /utilisateurs` - Lister les utilisateurs (Permission: lire_utilisateurs)
- `GET /utilisateurs/{id}` - Obtenir un utilisateur
- `PATCH /utilisateurs/{id}` - Modifier un utilisateur
- `DELETE /utilisateurs/{id}` - Supprimer un utilisateur

#### 🎭 Rôles (`/roles`)
- `POST /roles` - Créer un rôle (Permission: gerer_roles)
- `GET /roles` - Lister les rôles (Permission: lire_roles)
- `GET /roles/{id}` - Obtenir un rôle
- `PATCH /roles/{id}` - Modifier un rôle
- `DELETE /roles/{id}` - Supprimer un rôle

#### 🔑 Permissions (`/permissions`)
- `POST /permissions` - Créer une permission (Permission: gerer_permissions)
- `GET /permissions` - Lister les permissions (Permission: lire_permissions)
- `POST /permissions/attribuer` - Attribuer des permissions à un rôle

#### 📢 Canaux (`/canaux`)
- `POST /canaux` - Créer un canal (Permission: creer_canaux)
- `GET /canaux` - Lister les canaux (Permission: lire_canaux)
- `GET /canaux/{id}` - Obtenir un canal
- `PATCH /canaux/{id}` - Modifier un canal
- `DELETE /canaux/{id}` - Supprimer un canal

#### 💬 Messages (`/messages`)
- `POST /messages` - Envoyer un message (Permission: envoyer_messages)
- `GET /messages/canal/{canal_id}` - Historique d'un canal
- `GET /messages/{id}` - Obtenir un message
- `PATCH /messages/{id}` - Modifier un message
- `DELETE /messages/{id}` - Supprimer un message (soft delete)

#### 🔌 WebSocket (`/ws`)
- `WS /ws/chat/{canal_id}?token=JWT` - Connexion WebSocket pour chat temps réel
- `GET /ws/canaux/{canal_id}/utilisateurs` - Utilisateurs connectés

---

## 📁 Structure du projet

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

---

## 🧪 Tests

### Tester l'API avec curl

```bash
# 1. Se connecter
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 2. Copier le token et lister les utilisateurs
curl -X GET "http://localhost:8000/utilisateurs" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

### Tester le WebSocket

1. Ouvrir `test_chat.html` dans un navigateur
2. Se connecter avec admin/admin123
3. Sélectionner un canal
4. Envoyer des messages

### Tester avec Swagger

1. Aller sur http://localhost:8000/docs
2. Cliquer sur "Authorize"
3. Entrer : admin / admin123
4. Tester tous les endpoints

---

## 🚢 Déploiement

### Variables d'environnement en production

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=<clé_générée_aléatoirement>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PROJECT_NAME=Gestion RBAC Chat
DEBUG=False
```

### Avec Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Avec Gunicorn (production)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 🔒 Sécurité

### Bonnes pratiques implémentées

✅ Mots de passe hashés avec Bcrypt  
✅ Tokens JWT avec expiration  
✅ Vérification des permissions sur chaque endpoint  
✅ Protection CORS configurable  
✅ Validation des données avec Pydantic  
✅ Soft delete pour les messages  

### Recommandations pour la production

- [ ] Changer toutes les valeurs par défaut (.env, mots de passe)
- [ ] Configurer CORS avec des domaines spécifiques
- [ ] Activer HTTPS
- [ ] Utiliser des variables d'environnement sécurisées
- [ ] Mettre en place des rate limits
- [ ] Activer les logs de sécurité
- [ ] Sauvegardes régulières de la base de données

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des fonctionnalités
- Soumettre des pull requests

---

## 📄 Licence

Ce projet est sous licence MIT.

---

## 👨‍💻 Auteur

Développé avec ❤️ en Python & FastAPI

---

## 📞 Support

Pour toute question ou problème :
- Consulter la documentation : http://localhost:8000/docs
- Ouvrir une issue sur GitHub
- Consulter les fichiers de tests : `TESTS_PHASE_*.txt`

---

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !**
