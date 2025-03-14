
# 🏢 BACOREX-SARL

**Application de gestion des activités pour BACOREX-SARL.**

---

## 📝 Description

Ce projet Django vise à développer une application de gestion des activités pour BACOREX-SARL. L'application offre des fonctionnalités pour la gestion de projets, le suivi des dossiers d'appel d'offres et la collaboration entre les membres de l'équipe.

---

## 🚀 Fonctionnalités

- **📂 Gestion des projets** : Création, modification et suppression de projets. Suivi de l'avancement des projets avec des tâches, des échéances et des responsables.
- **📑 Dossiers d'appel d'offres** : Gestion des dossiers d'appel d'offres, y compris la création, la modification et la visualisation des dossiers. Suivi des offres soumises et des résultats.
- **👥 Collaboration d'équipe** : Fonctionnalités de collaboration pour les membres de l'équipe, notamment la gestion des utilisateurs, la gestion des autorisations d'accès aux projets et aux dossiers, et la communication interne.

---

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **🐍 Python 3.11** (ou une version compatible)
- **📦 Poetry** (gestionnaire de dépendances)
- **🐘 PostgreSQL** (base de données)

---

## 🚀 Installation

### 1. Cloner le dépôt

Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/votre-utilisateur/BACOREX-SARL.git
cd BACOREX-SARL
```

### 2. Configurer l'environnement virtuel avec Poetry

Poetry est utilisé pour gérer les dépendances du projet. Pour installer les dépendances, exécutez :

```bash
poetry install
```

Cela installera toutes les dépendances listées dans `pyproject.toml`.

### 3. Activer l'environnement virtuel

Activez l'environnement virtuel créé par Poetry :

```bash
poetry shell
```

### 4. Configurer la base de données

Le projet utilise PostgreSQL comme base de données. Assurez-vous que PostgreSQL est installé et en cours d'exécution.

#### a. Créer la base de données

Créez une base de données PostgreSQL nommée `bacorex_db` :

```sql
CREATE DATABASE bacorex_db;
```

#### b. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet et ajoutez les informations de connexion à la base de données :

```env
POSTGRES_DB=bacorex_db
POSTGRES_USER=bacorex_user
POSTGRES_PASSWORD=bac0rex
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Appliquer les migrations

Appliquez les migrations Django pour configurer la base de données :

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur

Créez un superutilisateur pour accéder à l'interface d'administration :

```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur de développement

Démarrez le serveur de développement Django :

```bash
python manage.py runserver
```

Accédez à l'application dans votre navigateur à l'adresse : [http://localhost:8000](http://localhost:8000).

---

## 👥 Configuration des groupes et utilisateurs

1. Accédez à l'interface d'administration : [http://localhost:8000/admin](http://localhost:8000/admin).
2. Connectez-vous avec les identifiants du superutilisateur créé précédemment.
3. Créez les groupes suivants :
   - **DAO_TEAM**
   - **PROJET_TEAM**
4. Créez des utilisateurs et assignez-les aux groupes appropriés.

---

## 🧪 Exécution des tests

Pour exécuter les tests du projet, utilisez la commande suivante :

```bash
python manage.py test
```

---

## 🤝 Contribuer

Les contributions à ce projet sont les bienvenues ! Voici comment vous pouvez contribuer :

1. **🐛 Ouvrir une issue** : Signalez des bogues ou proposez des améliorations.
2. **🔀 Soumettre une pull request** : Apportez des modifications directement au projet.

### Bonnes pratiques

- Suivez les conventions de code du projet.
- Assurez-vous que les tests passent avant de soumettre une pull request.
- Documentez vos modifications.

---

## 👨‍💻 Auteurs

Ce projet a été développé par l'équipe de développement de BACOREX-SARL.

---

## 📜 Licence

Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier [LICENSE](LICENSE).

---

## 🔍 Remarques supplémentaires

- **🔒 Variables d'environnement** : Assurez-vous de ne pas exposer les informations sensibles (comme les mots de passe) dans le code source. Utilisez un fichier `.env` pour stocker ces informations.
- **📚 Documentation** : Si vous ajoutez de nouvelles fonctionnalités, mettez à jour la documentation en conséquence.

---

## 🎨 Icônes utilisées

Les icônes utilisées dans ce fichier proviennent de [Shields.io](https://shields.io/) et [Emoji Cheat Sheet](https://www.webfx.com/tools/emoji-cheat-sheet/).

