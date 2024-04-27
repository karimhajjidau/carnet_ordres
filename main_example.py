import requests

# Import des classes Orderbook et Order définies dans les fichiers séparés
from class_Orderbook import Orderbook
from class_Order import Order

# Initialisation d'un carnet d'ordres
orderbook = Orderbook()
orderbook.open_market()  # Ouvre le marché pour permettre l'ajout et l'exécution des ordres. C'est nécessaire pour commencer à interagir avec le carnet d'ordres.

# Ajout d'un ordre de vente à prix limité
orderbook.add_order(Order('limit', 'sell', 102, 200))
print(orderbook)  # Affichage de l'état du carnet après ajout de l'ordre de vente

# Ajout d'un ordre d'achat à prix limité
orderbook.add_order(Order('limit', 'buy', 102, 50))
print(orderbook)  # Affichage de l'état du carnet après ajout de l'ordre d'achat

# Ajout d'un ordre d'achat au marché
orderbook.add_order(Order('market', 'buy', None, 25))  # Ordre exécuté immédiatement au meilleur prix disponible

# Modification d'un ordre existant
orderbook.modify_order(1, 102, 100)  # Modification du prix et de la quantité de l'ordre numéro 1
print(orderbook)  # Affichage de l'état du carnet après modification de l'ordre

# Exemple d'utilisation avec récupération de l'état actuel du carnet d'ordres sur Binance
orderbook = Orderbook()
orderbook.fetch_binance_snapshot('BTCUSDT')  # Télécharge et intègre les données récentes de Binance dans le carnet
orderbook.open_market()  # Réouverture du marché pour permettre l'ajout et l'exécution des ordres
print(orderbook)  # Affichage de l'état initial du carnet après récupération des données

# Ajout d'un ordre d'achat au marché
orderbook.add_order(Order('market', 'buy', None, 0.58281))  # Cet ordre est exécuté immédiatement au meilleur prix disponible
print(orderbook)  # Affichage de l'état du carnet après ajout et exécution de l'ordre au marché
