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
            self.fix_orders(True)

    def close_market(self):
        with self.lock:
            self.market_open = False
            print("Market is now closed.")
            self.fix_orders(False)

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
                self.add_limit_order(order)
            elif order.order_type == "market":
                self.execute_market_order(order)

    def add_limit_order(self, order):
        target_list = self.bids if order.side == 'buy' else self.asks
        target_list.append(order)
        target_list.sort(key=lambda x: (-x.price, x.timestamp) if order.side == 'buy' else (x.price, x.timestamp))

    def execute_limit_order(self, order):
        self.add_limit_order(order)
        executed_list = self.asks if order.side == 'sell' else self.bids
        opposite_list = self.asks if order.side == 'buy' else self.bids
        i = 0
        while order.quantity > 0 and i < len(opposite_list):
            best_match = opposite_list[i]
            if (order.side == 'buy' and order.price >= best_match.price) or (order.side == 'sell' and order.price <= best_match.price):
                trade_quantity = min(order.quantity, best_match.quantity)
                order.quantity -= trade_quantity
                best_match.quantity -= trade_quantity
                if best_match.quantity == 0:
                    opposite_list.pop(i)
                    i += 1
                else:
                    executed_list.pop(0)
                    

    def execute_market_order(self, order):
        executed_list = self.asks if order.side == 'sell' else self.bids
        opposite_list = self.asks if order.side == 'buy' else self.bids
        if not opposite_list:
            print(f"No orders available for matching.")
            return

        index = 0
        while order.quantity > 0 and index < len(opposite_list):
            best_match = opposite_list[index]
            trade_quantity = min(order.quantity, best_match.quantity)
            order.quantity -= trade_quantity
            best_match.quantity -= trade_quantity
            if best_match.quantity == 0:
                opposite_list.pop(index)
                index += 1
            else:
                executed_list.pop(0)



    def fix_orders(self, opening=True):
        if not self.bids or not self.asks:
            print("Not enough orders to fix.")
            return

        potential_trades = [(min(bid.quantity, ask.quantity), bid, ask) for bid in self.bids for ask in self.asks if bid.price >= ask.price]
        potential_trades.sort(key=lambda x: x[0], reverse=True)
        if potential_trades:
            max_volume_trade = potential_trades[0]
            fixing_price = (max_volume_trade[1].price + max_volume_trade[2].price) / 2
            print(f"Fixing price at {'opening' if opening else 'closing'}: {fixing_price}")

    def __str__(self):
        bids_str = '\n'.join([f"Bid: {order.order_id}, Price: {order.price}, Quantity: {order.quantity}" for order in self.bids if order.quantity > 0])
        asks_str = '\n'.join([f"Ask: {order.order_id}, Price: {order.price}, Quantity: {order.quantity}" for order in self.asks if order.quantity > 0])
        return f"Orderbook:\n\nBids:\n{bids_str}\n\nAsks:\n{asks_str}"

# Example usage
orderbook = Orderbook()
orderbook.open_market()
orderbook.add_order(Order('limit', 'sell', 102, 200))
orderbook.add_order(Order('limit', 'buy', 102, 200))
print(orderbook)
orderbook.open_market()
print(orderbook)
print(orderbook)
orderbook.add_order(Order('market', 'sell', None, 150))
print(orderbook)
orderbook.close_market()
print(orderbook)
