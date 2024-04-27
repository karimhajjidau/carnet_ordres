import time

class Order:
    def __init__(self, order_type, side, price, quantity):
        self.order_id = None
        self.timestamp = time.time()
        self.order_type = order_type
        self.side = side
        self.price = price
        self.quantity = quantity