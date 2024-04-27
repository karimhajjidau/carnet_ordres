import time

class Order:
    def __init__(self, order_type, side, price, quantity):
        self.order_id = None  # ID de l'ordre, initialisé à None
        self.timestamp = time.time()  # Enregistre le moment de création de l'ordre
        self.order_type = order_type  # Type d'ordre (par exemple 'limit', 'market')
        self.side = side  # Côté de l'ordre ('buy' ou 'sell')
        self.price = price  # Prix à l'unité de l'ordre
        self.quantity = quantity  # Quantité à acheter ou vendre
