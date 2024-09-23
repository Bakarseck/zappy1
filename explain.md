Lorsque le client se connecte au serveur dans **Zappy**, voici le rôle et les actions de chaque composant (le joueur humain, l'IA et le serveur) :

### 1. **Le Client (Humain)** :
- **Ce qu'il fait** : Le joueur humain **ne contrôle pas directement** son personnage (puisque c'est une IA), mais il peut configurer et observer les actions de son IA. Le client envoie des commandes au serveur, comme des instructions pour que l'IA bouge, cherche de la nourriture, collecte des ressources, ou participe à un rituel d’évolution.
- **Interactions avec le jeu** : Le client peut définir la stratégie de l'IA, surveiller l’état du joueur (nourriture, objets collectés, etc.) via des commandes comme `inventory`, ou observer l’environnement via la commande `see`.

### 2. **L'IA (le joueur dans le jeu)** :
- **Ce qu'elle fait** : L'IA est le personnage contrôlé par le client sur le terrain de jeu. Elle agit de manière autonome après avoir reçu les instructions. Elle peut :
  - Se déplacer sur la carte.
  - Chercher de la nourriture pour survivre.
  - Collecter des pierres précieuses nécessaires à l'évolution.
  - Participer à des rituels pour monter de niveau.
  - Coopérer avec d'autres joueurs pour évoluer.
  L'IA suit les ordres envoyés par le client et réagit en fonction des informations qu'elle reçoit du serveur.

### 3. **Le Serveur** :
- **Ce qu'il fait** : Le serveur gère toute la logique du jeu. Il :
  - Gère la carte du monde (génère les ressources aléatoirement, place les joueurs).
  - Reçoit les commandes des clients, les exécute, et renvoie les résultats (comme les objets visibles sur une case).
  - Gère la nourriture et la survie des joueurs : si un joueur ne mange pas assez, il meurt.
  - Vérifie les conditions d'évolution des joueurs et la gestion des rituels.
  - Maintient à jour l’état du jeu et informe chaque client des changements (comme la position des autres joueurs, les ressources disponibles, etc.).
  - Termine la partie quand une équipe atteint les conditions de victoire (six joueurs au niveau 8).

### En résumé :
- **Le client humain** envoie des commandes au serveur pour influencer les actions de son IA.
- **L'IA** exécute les actions demandées par le client, mais agit de manière autonome pour collecter des ressources et survivre.
- **Le serveur** gère l’état du monde, les ressources, les interactions entre joueurs, et renvoie au client les résultats des actions.