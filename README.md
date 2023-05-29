# BACOREX-SARL

Application de gestion des activités pour BACOREX-SARL.

## Description

Ce projet Django vise à développer une application de gestion des activités pour BACOREX-SARL. L'application offrira des fonctionnalités pour la gestion de projets, le suivi des dossiers d'appel d'offres et la collaboration entre les membres de l'équipe.

## Fonctionnalités

- Gestion des projets : Création, modification et suppression de projets. Suivi de l'avancement des projets avec des tâches, des échéances et des responsables.
- Dossiers d'appel d'offres : Gestion des dossiers d'appel d'offres, y compris la création, la modification et la visualisation des dossiers. Suivi des offres soumises et des résultats.
- Collaboration d'équipe : Fonctionnalités de collaboration pour les membres de l'équipe, notamment la gestion des utilisateurs, la gestion des autorisations d'accès aux projets et aux dossiers, et la communication interne.

## Installation

1. Clonez ce dépôt vers votre machine locale.
2. Assurez-vous d'avoir Python et Django installés sur votre machine.
3. Créez un environnement virtuel et activez-le.
4. Installez les dépendances en exécutant la commande suivante :
```
pip install -r requirements.txt
```

5. Configurez la base de données en exécutant les migrations Django :
```
python manage.py migrate
```

6. Lancez le serveur de développement avec la commande suivante :
```
python manage.py runserver
```

7. Accédez à l'application dans votre navigateur à l'adresse : http://localhost:8000/  

Aller http://localhost:8000/admin et creer les groupe **DAO_TEAM** et **PROJET_TEAM**.  
Creer vous utiisateur  

## Contribuer

Les contributions à ce projet sont les bienvenues. Vous pouvez ouvrir des issues pour signaler des bogues, proposer des améliorations ou soumettre des demandes de fusion (pull requests) pour apporter des modifications directement.

Assurez-vous de suivre les bonnes pratiques de développement et de respecter le code de conduite du projet.

## Auteurs

Ce projet a été développé par l'équipe de développement de BACOREX-SARL.

## Licence

Ce projet est sous licence MIT. Vous pouvez consulter le fichier [LICENSE](LICENSE) pour plus de détails.

---
N'oubliez pas de mettre à jour les sections manquantes ou spécifiques à votre projet, telles que les fonctionnalités, l'installation, les auteurs et la licence, en fonction de vos besoins.
