# ContactBook - Application de Gestion de Contacts Personnels

ContactBook est une application web moderne de gestion de contacts personnels développée avec Django. Elle permet à chaque utilisateur de gérer ses propres contacts de manière sécurisée, esthétique et fonctionnelle.

## Fonctionnalités

- **Gestion complète des contacts** : Ajout, modification, consultation et suppression de contacts
- **Informations détaillées** : Prénom, nom, téléphone, email, adresse, avatar, date de naissance et notes
- **Tableau de bord personnalisé** : Statistiques, anniversaires à venir, contacts récents
- **Recherche avancée** : Recherche par nom, prénom, email ou téléphone
- **Organisation** : Groupes de contacts et système de favoris
- **Corbeille** : Récupération des contacts supprimés
- **Thème clair/sombre** : Personnalisation de l'interface
- **Authentification sécurisée** : Chaque utilisateur n'a accès qu'à ses propres données
- **Suivi des sessions** : Visualisation des connexions actives

## Technologies utilisées

- **Backend** : Django 4.2
- **Frontend** : HTML, CSS, JavaScript, Bootstrap 5
- **Base de données** : SQLite 
- **Authentification** : Système personnalisé basé sur Django Auth
- **Stockage des médias** : Gestion des avatars avec Pillow

## Installation

1. Cloner le dépôt :
   \`\`\`
   git clone https://github.com/JoeDev-00/ContactsBook.git
   cd contactbook
   \`\`\`

2. Créer et activer un environnement virtuel :
   \`\`\`
   python -m venv venv
   venv\Scripts\activate #sur Mac source venv/bin/activate
   \`\`\`

3. Installer les dépendances :
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

4. Effectuer les migrations :
   \`\`\`
   python manage.py migrate
   \`\`\`

5. Créer un superutilisateur :
   \`\`\`
   python manage.py createsuperuser
   \`\`\`

6. Lancer le serveur de développement :
   \`\`\`
   python manage.py runserver
   \`\`\`

7. Accéder à l'application dans votre navigateur à l'adresse `http://127.0.0.1:8000`

## Captures d'écran

![Tableau de bord](screenshots/dashboard.png)
![Liste des contacts](screenshots/contact_list.png)
![Détail d'un contact](screenshots/contact_detail.png)

## Déploiement

L'application peut être déployée sur diverses plateformes comme Vercel, Render, PythonAnywhere, ou Heroku. Consultez la documentation de ces services pour les instructions spécifiques de déploiement.
Elle est actuellement accessible sur Vercel à l'addresse : https://repertoire.vercel.app

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.
Mais ne pas directement travailler avec la branche principale 😉

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
