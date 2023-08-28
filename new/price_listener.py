class PriceListener:

    def __init__(self):
        self.bid = 0
        self.ask = 0
    
    def update(self, bid_price: float, ask_price: float):
        self.bid = bid_price
        self.ask = ask_price
