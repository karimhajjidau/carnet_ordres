from class_Order import Order

import threading
import time
import requests


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
            self.fix_orders() # fixing effectué à l'ouverture

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
        for price in range(int(min_price), int(max_price) + 1):
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

    def modify_order(self, order_id, new_price=None, new_quantity=None):
        with self.lock:
            # Search in both bids and asks
            for order_list in [self.bids, self.asks]:
                for order in order_list:
                    if order.order_id == order_id:
                        if new_price is not None:
                            order.price = new_price
                        if new_quantity is not None:
                            order.quantity = new_quantity
                        print(f"Order {order_id} modified to new price: {new_price}, new quantity: {new_quantity}")
                        return
            print(f"No order found with ID {order_id}.")
            
    def remove_order(self, order_id):
        with self.lock:
            # Search and remove from both bids and asks
            for order_list in [self.bids, self.asks]:
                for i, order in enumerate(order_list):
                    if order.order_id == order_id:
                        order_list.pop(i)
                        print(f"Order {order_id} removed.")
                        return
            print(f"No order found with ID {order_id}.")
    
    
    def __str__(self):
        bids_str = '\n'.join([f"Bid: {order.order_id}, Price: {order.price}, Quantity: {order.quantity}" for order in self.bids if order.quantity > 0])
        asks_str = '\n'.join([f"Ask: {order.order_id}, Price: {order.price}, Quantity: {order.quantity}" for order in self.asks if order.quantity > 0])
        return f"Orderbook:\n\nBids:\n{bids_str}\n\nAsks:\n{asks_str}"

    def fetch_binance_snapshot(self, symbol='BTCUSDT'):
        url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=50"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            
            with self.lock:
                self.bids.clear()  # Clear existing data
                self.asks.clear()
                
                for bid in data['bids']:
                    price, quantity = float(bid[0]), float(bid[1])
                    order = Order('limit', 'buy', price, quantity)
                    self.add_order(order)  # Managed addition
                    
                for ask in data['asks']:
                    price, quantity = float(ask[0]), float(ask[1])
                    order = Order('limit', 'sell', price, quantity)
                    self.add_order(order)  # Managed addition
                
        except requests.RequestException as e:
            print(f"Failed to fetch data: {e}")
        except ValueError:
            print("Failed to parse JSON data")