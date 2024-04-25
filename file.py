import threading
import time

class Order:
    def __init__(self, order_type, side, price, quantity):
        self.order_id = None
        self.timestamp = time.time()
        self.order_type = order_type
        self.side = side
        self.price = price
        self.quantity = quantity

class Orderbook:
    def __init__(self):
        self.current_order_id = 1
        self.bids = []
        self.asks = []
        self.market_open = False
        self.lock = threading.Lock()

    def open_market(self):
        with self.lock:
            self.market_open = True
            print("Market is now open.")
            self.fix_orders()

    def close_market(self):
        with self.lock:
            self.market_open = False
            print("Market is now closed.")
            self.fix_orders()

    def add_order(self, order):

        order.order_id = self.current_order_id
        self.current_order_id += 1

        if not self.market_open:
            if order.order_type == 'market':
                print("Market is closed. Market orders are not accepted.")
                return
            else:
                self.add_limit_order(order)
            return

        with self.lock:
            if order.order_type == "limit":
                self.execute_limit_order(order)
            elif order.order_type == "market":
                self.execute_market_order(order)

    def add_limit_order(self, order):
        target_list = self.bids if order.side == 'buy' else self.asks
        target_list.append(order)
        target_list.sort(key=lambda x: (-x.price, x.timestamp) if order.side == 'buy' else (x.price, x.timestamp))

    def execute_limit_order(self, order):
        self.add_limit_order(order)
        opposite_list = self.asks if order.side == 'buy' else self.bids
        i = 0
        while order.quantity > 0 and i < len(opposite_list):
            best_match = opposite_list[i]
            if (order.side == 'buy' and order.price >= best_match.price) or (order.side == 'sell' and order.price <= best_match.price):
                trade_quantity = min(order.quantity, best_match.quantity)
                order.quantity -= trade_quantity
                best_match.quantity -= trade_quantity
                if best_match.quantity == 0:
                    opposite_list.pop(i)  # Remove fully matched order
                else:
                    i += 1  # Increment only if not removing an item

    def execute_market_order(self, order):
        opposite_list = self.asks if order.side == 'buy' else self.bids
        if not opposite_list:
            print(f"No orders available for matching with Order {order.order_id}.")
            return

        i = 0
        while order.quantity > 0 and i < len(opposite_list):
            best_match = opposite_list[i]
            trade_quantity = min(order.quantity, best_match.quantity)
            order.quantity -= trade_quantity
            best_match.quantity -= trade_quantity
            if best_match.quantity == 0:
                opposite_list.pop(i)  # Remove fully matched order
            else:
                i += 1  # Increment only if not removing an item

        if order.quantity > 0:  # Check if some quantity remains unexecuted
            print(f"Order number {order.order_id} not fully executed. Remaining quantity: {order.quantity}")

    def fix_orders(self):
        if not self.bids or not self.asks:
            print("No sufficient bids or asks to fix prices.")
            return
        
        min_price = min(ask.price for ask in self.asks)
        max_price = max(bid.price for bid in self.bids)

        price_to_volume = {}
        for price in range(min_price, max_price + 1):
            bid_volume = sum(bid.quantity for bid in self.bids if bid.price >= price)
            ask_volume = sum(ask.quantity for ask in self.asks if ask.price <= price)
            transaction_volume = min(bid_volume, ask_volume)
            price_to_volume[price] = transaction_volume

        if price_to_volume:
            equilibrium_price = max(price_to_volume, key=price_to_volume.get)
            max_volume = price_to_volume[equilibrium_price]
            print(f"Fixing price at opening: {equilibrium_price}. Max volume of transactions: {max_volume}")
        else:
            print("No bids or asks to fix prices.")

    def __str__(self):
        bids_str = '\n'.join([f"Bid: {order.order_id}, Price: {order.price}, Quantity: {order.quantity}" for order in self.bids if order.quantity > 0])
        asks_str = '\n'.join([f"Ask: {order.order_id}, Price: {order.price}, Quantity: {order.quantity}" for order in self.asks if order.quantity > 0])
        return f"Orderbook:\n\nBids:\n{bids_str}\n\nAsks:\n{asks_str}"

# Example usage
orderbook = Orderbook()
orderbook.open_market()
orderbook.add_order(Order('limit', 'sell', 102, 200))
print(orderbook)
orderbook.add_order(Order('limit', 'buy', 101, 200))
print(orderbook)
orderbook.add_order(Order('limit', 'buy', 102, 50))
orderbook.add_order(Order('market', 'sell', None, 200))
print(orderbook)

print(orderbook)
