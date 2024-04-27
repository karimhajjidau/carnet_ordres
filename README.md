# carnet_ordres
Ce projet est un simulateur de carnet d’ordres, utile pour comprendre et analyser le fonctionnement des marchés financiers. Il permet de simuler les interactions entre acheteurs et vendeurs à travers des ordres limites et des ordres au marché, et intègre un mécanisme de fixing qui est exécuté à l'ouverture et à la fermeture du marché.

Deux classes : 
- Order : Représente un ordre individuel dans le carnet. Chaque ordre est caractérisé par un type (limite ou marché), un côté (achat ou vente), un prix, et une quantité.
- OrderBook : Gère l'ensemble du carnet d'ordres, incluant l'ajout, la modification, et la suppression des ordres, ainsi que la gestion de l'ouverture et de la fermeture du marché.

Deux types d'ordres :
- Ordre limite : L'utilisateur spécifie un prix précis. L'ordre n'est exécuté que si le marché atteint ce prix.
- Ordre au marché : L'ordre est passé à la meilleure offre ou à la meilleure demande. Nous n'éxectuons pas et ne stockons pas les ordres au marché s'ils ne conviennent pas.
  
Mécanisme de fixing :
- Nous réalisons un fixing au moment de l'ouverture et de la cloture du marché. Le cours de fixing correspond au cours qui permet de maximiser le nombre de transactions

Gestion des ordres :
- Ajout d'ordres : Ajouter des ordres au carnet, que ce soit des ordres limite ou au marché.
- Modification d'ordres : Permet de modifier le prix ou la quantité d'un ordre existant.
- Suppression d'ordres : Permet de retirer un ordre du carnet.

Intégration des données réelles :
- Fetch Binance snapshot : Récupère un instantané du carnet d'ordres de la plateforme Binance pour initialiser le simulateur avec des données de marché réelles.

Utilisation du simulateur :
Pour utiliser ce simulateur, vous devez d'abord configurer votre environnement Python et installer les dépendances nécessaires. Ensuite, vous pouvez exécuter le script pour interagir avec le simulateur via un terminal.
