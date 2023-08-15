import socket
import simplefix
from datetime import datetime
import time

class FixClient:

    def __init__(self, server, port, sender_comp_id, target_comp_id, username, password):
        self.server = server
        self.port = port
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self.username = username
        self.password = password
        self.parser = simplefix.FixParser()
        self.fix_generator = simplefix.FixMessage()
        self.msg_seq_num = 1
        self.login_successful = False
        self.sock = None

    def calculate_checksum(self, message):
        return '{:03d}'.format(sum(message) % 256)

    def create_logon_msg(self):
        self.fix_generator.append_pair(8, "FIX.4.4")
        self.fix_generator.append_pair(35, "A")
        self.fix_generator.append_pair(34, 1)
        self.fix_generator.append_pair(49, self.sender_comp_id)
        self.fix_generator.append_pair(56, self.target_comp_id)
        self.fix_generator.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        self.fix_generator.append_pair(98, 0)
        self.fix_generator.append_pair(108, 30)
        self.fix_generator.append_pair(141, "Y")
        self.fix_generator.append_pair(553, self.username)
        self.fix_generator.append_pair(554, self.password)
        return self.fix_generator.encode()
    
    def create_heartbeat_msg(self):
        self.fix_generator = simplefix.FixMessage()
        self.fix_generator.append_pair(8, "FIX.4.4")
        self.fix_generator.append_pair(35, "0")  # Heartbeat
        self.fix_generator.append_pair(34, 3)  # Sequence number
        self.fix_generator.append_pair(49, self.sender_comp_id)
        self.fix_generator.append_pair(56, self.target_comp_id)
        self.fix_generator.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        return self.fix_generator.encode()
        

    def send_message(self, msg):
        if self.sock is None:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.server, self.port))
            except Exception as e:
                print("Error connecting to the server:", e)
                return

        # Increment message sequence number for each sent message
        self.msg_seq_num += 1
        self.sock.sendall(msg)
        print(f"Sent: {msg}")

    def create_new_order_single_msg(self, symbol, side, order_qty, ord_type, price=None):
        message = simplefix.FixMessage()

    def create_new_order_single_msg(self, symbol, side, order_qty, ord_type, price=None):
        message = simplefix.FixMessage()

        # Append Body tags
        message.append_pair(35, "D")  # MsgType for New Order - Single
        message.append_pair(49, self.sender_comp_id)  # SenderCompID
        message.append_pair(56, self.target_comp_id)  # TargetCompID
        message.append_pair(34, self.msg_seq_num)  # MsgSeqNum
        message.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # SendingTime

        # Generate a unique ClOrdID based on the current timestamp
        unique_clordid = str(int(time.time() * 1000))
        message.append_pair(11, unique_clordid)  # ClOrdID (Client Order ID)

        message.append_pair(1, self.username)  # Account
        message.append_pair(55, symbol)  # Symbol
        message.append_pair(54, side)  # Side (1 - Buy, 2 - Sell)
        message.append_pair(38, order_qty)  # OrderQty
        message.append_pair(40, ord_type)  # OrdType (1 - Market, 2 - Limit)
        message.append_pair(59, "1")  # TimeInForce
        if price is not None:
            message.append_pair(44, price)  # Price
        message.append_pair(60, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))

        # Encode the body part
        encoded_body = b''.join([f"{tag}={value}\x01".encode() for tag, value in message.pairs])

        # Calculate BodyLength (tag 9)
        body_length = len(encoded_body)

        # Build the final message
        final_message = simplefix.FixMessage()
        final_message.append_pair(8, "FIX.4.4")  # BeginString
        final_message.append_pair(9, str(body_length))  # BodyLength
        # Append the body
        for tag, value in message.pairs:
            final_message.append_pair(tag, value)

        # Calculate the checksum manually
        encoded_msg_without_checksum = final_message.encode()[:-7]
        checksum = self.calculate_checksum(encoded_msg_without_checksum)
        final_message.append_pair(10, checksum)  # CheckSum

        return final_message.encode(), unique_clordid

    def receive_messages(self):
        last_heartbeat_time = time.time()
        try:
            while True:
                data = self.sock.recv(8192)
                if not data:
                    break
                self.parser.append_buffer(data)
                while True:
                    msg = self.parser.get_message()
                    if msg is None:
                        break

                    msg_type = msg.get(35)
                    if msg_type and msg_type.decode() == "A":
                        print("Logon successful!")
                    print(f"Received: {msg}")

                current_time = time.time()
                if current_time - last_heartbeat_time >= 30:
                    heartbeat_msg = self.create_heartbeat_msg()
                    self.send_message(heartbeat_msg)
                    last_heartbeat_time = current_time

        except KeyboardInterrupt:
            pass

    # ... (your existing methods for creating heartbeat, order cancel, etc.)

if __name__ == '__main__':
    client = FixClient("127.0.0.1", 8080, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    logon_msg = client.create_logon_msg()
    client.send_message(logon_msg)
    
    # Wait for a few seconds to ensure successful logon before sending an order
    time.sleep(5)
    
    # Create and send a new order message
    new_order_msg = client.create_new_order_single_msg(
        symbol="EURUSD.x",
        side="1",
        order_qty="1000000",
        ord_type="1",
        price=None  # Market order, no specific price
    )
    client.send_message(new_order_msg)

    # Receive messages, including heartbeats and responses
    client.receive_messages()