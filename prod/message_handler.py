

class MessageHandler:

    def __init__(self, price_listener):
        self.price_listener = price_listener
        self.code_to_function = {
            'W': self.on_market_data_response,
        }
    
    def get_function(self, code: str):
        if code in self.code_to_function:
            return self.code_to_function.get(code)

        return None
    
    def on_receive_message(self, message):
        message_type = message.get(35)
        function = self.get_function(message_type.decode('utf-8'))

        if function:
            function(message)
        else:
            print(f"Received FIX message: {message}")
    

    def on_market_data_response(self, message):
        bid_price = float(message.get(270, 1).decode('utf-8'))
        ask_price = float(message.get(270, 2).decode('utf-8'))

        self.price_listener.update(bid_price=bid_price, ask_price=ask_price)
