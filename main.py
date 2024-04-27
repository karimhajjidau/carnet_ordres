import requests

from class_Orderbook import Orderbook
from class_Order import Order



# Example usage 
orderbook = Orderbook()
orderbook.open_market()
orderbook.add_order(Order('limit', 'sell', 102, 200))
print(orderbook)
orderbook.add_order(Order('limit', 'buy', 102, 50))
print(orderbook)
orderbook.add_order(Order('market', 'buy', None, 25))

orderbook.modify_order(1,102,100) #Changement de l'ordre numéro 1
print(orderbook)


#Example usage with snapshot
orderbook = Orderbook()
orderbook.fetch_binance_snapshot()  # Récupération de l'état actuel du carnet d'ordres de Binance
orderbook.open_market()
print(orderbook)

orderbook.add_order(Order('market', 'buy', None, 0.58281)) #Ajout d'achat ordre au marché (éxecuté) au meilleur prix
print(orderbook)
