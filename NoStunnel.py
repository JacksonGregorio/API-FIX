import socket
import simplefix
from datetime import datetime
import time
from TestRio import FixClientQuotes


class FixClient:

    def __init__(self, server, port, sender_comp_id, target_comp_id, username, password):
        self.server = server
        self.port = port
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self.username = username
        self.password = password
        self.parser = simplefix.FixParser()
        self.msg_seq_num = 1
        #self.unique_clordid = 0


    def calculate_checksum(self, message):
        return '{:03d}'.format(sum(message) % 256)

    def create_logon_msg(self):
        message = simplefix.FixMessage()

        # Append Body tags
        message.append_pair(35, "A")  # MsgType
        message.append_pair(49, self.sender_comp_id)  # SenderCompID
        message.append_pair(56, self.target_comp_id)  # TargetCompID
        message.append_pair(34, self.msg_seq_num)  # MsgSeqNum
        message.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # SendingTime
        message.append_pair(98, 0)  # EncryptMethod
        message.append_pair(108, "30")  # HeartBtInt
        message.append_pair(141, "Y")  # ResetSeqNumFlag
        message.append_pair(553, self.username)  # Username
        message.append_pair(554, self.password)  # Password

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

        return final_message.encode()
    
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
        # Incrementa o número de sequência para a próxima mensagem
        self.msg_seq_num += 1
        print(f"Send: {msg}")


    def receive_messages(self):
        last_heartbeat_time = time.time()
        fake_messages = [b'Message', b'Message', b'Message', b'Message', b'Message', b'Message']  # Substitua isso pelas mensagens que você deseja processar

        try:
            for data in fake_messages:
                self.parser.append_buffer(data)
                while True:
                    msg = self.parser.get_message()
                    if msg is None:
                    # Verifica se a mensagem é uma resposta de logon
                        msg_type = msg.get(35)
                    if msg_type and msg_type.decode() == "A":
                        print("Logon foi bem-sucedido!")
                        print(f"Received: {msg}")

                # Envia uma mensagem de heartbeat se já passaram mais de 30 segundos
                    current_time = time.time()
                    if current_time - last_heartbeat_time >= 30:
                        heartbeat_msg = self.create_heartbeat_msg()
                        self.send_message(heartbeat_msg)
                        last_heartbeat_time = current_time

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")

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
        message.append_pair(44, price)  # Price
        message.append_pair(60, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))

        # Include price if ord_type is Limit
        #if ord_type == "2" and price is not None:


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

    def create_new_order_single_msg_opposite(self, symbol, side, order_qty, ord_type, price=None):
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
        message.append_pair(44, price)  # Price
        message.append_pair(60, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))

        # Include price if ord_type is Limit
        #if ord_type == "2" and price is not None:


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

        return final_message.encode()

    def create_order_cancel_msg(self, clordid, account, orig_clordid, side, transact_time=None):
        message = simplefix.FixMessage()

        # Append Body tags
        message.append_pair(35, "F")  # MsgType for Order Cancel Request
        message.append_pair(49, self.sender_comp_id)  # SenderCompID
        message.append_pair(56, self.target_comp_id)  # TargetCompID
        message.append_pair(34, self.msg_seq_num)  # MsgSeqNum
        message.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # SendingTime

        message.append_pair(11, clordid)  # ClOrdID
        message.append_pair(1, account)  # Account
        message.append_pair(41, orig_clordid)  # OrigClOrdID
        message.append_pair(54, side)  # Side (1 - Buy, 2 - Sell)
        message.append_pair(60, transact_time or datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # TransactTime

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

        return final_message.encode()

    def create_order_status_request_msg(self, clordid, account, order_id=None):
        message = simplefix.FixMessage()

        # Append Body tags
        message.append_pair(35, "H")  # MsgType for Order Status Request
        message.append_pair(34, self.msg_seq_num)  # MsgSeqNum
        message.append_pair(49, self.sender_comp_id)  # SenderCompID


        message.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # SendingTime
        message.append_pair(56, self.target_comp_id)  # TargetCompID
        message.append_pair(54, 2)

        if order_id:
            message.append_pair(37, 6424)  # OrderID

        message.append_pair(11, clordid)  # ClOrdID
        message.append_pair(1, account)  # Account

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

        return final_message.encode()
    
    def process_market_data_snapshot(self, msg):
        symbol = msg.get(55)
        if symbol is not None:
            symbol = symbol.decode()

        bid_price = None
        ask_price = None

        no_md_entries = msg.get(268)
        if no_md_entries is not None:
            no_md_entries = int(no_md_entries.decode())

            for i in range(no_md_entries):
                md_entry_type = msg.get(269, i + 1)
                md_entry_px = msg.get(270, i + 1)

                if md_entry_type is not None and md_entry_px is not None:
                    md_entry_type = md_entry_type.decode()
                    md_entry_px = float(md_entry_px.decode())

                    if md_entry_type == '0':
                        bid_price = md_entry_px
                    elif md_entry_type == '1':
                        ask_price = md_entry_px

        if symbol is not None and bid_price is not None and ask_price is not None:
            print(f"Market Data Snapshot for {symbol}: Bid = {bid_price}, Ask = {ask_price}")
        else:
            bid_price = None
            ask_price = None

        return bid_price, ask_price


if __name__ == '__main__':
    client = FixClient("127.0.0.1", 8080, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    logon_msg = client.create_logon_msg()
    client.send_message(logon_msg)
    client2 = FixClientQuotes("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client2.logon()
    client2.get_quote("EURUSD_MDReqID", "EURUSD.x")

    # Aguardar alguns segundos para garantir que o logon seja bem-sucedido antes de enviar a ordem
    time.sleep(5)
    quotes = client2.listen_for_quotes()
    #time.sleep(5)
    bid, ask = quotes
    print(f"Bid: {bid}, Ask: {ask}")
    # Enviar uma ordem de compra a mercado
    point = 0.00001
    SL = 0.00010
    TP = 0.00040
    new_order_msg, original_clordid = client.create_new_order_single_msg(
        symbol="EURUSD.x",
        side="1",
        order_qty="1000000",
        ord_type="1",
        price=ask + point
    )
    client.send_message(new_order_msg)
    price_used = ask + point
    cancel_msg = client.create_order_cancel_msg(
        clordid="unique_id_12343",
        account="100019",
        orig_clordid=1690376701735,
        side="1"
    )
    client.send_message(cancel_msg)
    client.receive_messages()
    #time.sleep(30)
    new_order_msg = client.create_new_order_single_msg_opposite(
        symbol="EURUSD.x",
        side="2",
        order_qty="1000000",
        ord_type="2",
        price=price_used + TP
    )
    client.send_message(new_order_msg)
    # Espere 30 segundos antes de enviar a requisição de alteração de ordem
    time.sleep(30)
    status_request_msg = client.create_order_status_request_msg(
        clordid=1690376701735,
        account="100019",
        order_id="order_id_67898"  # This is optional
    )
    client.send_message(status_request_msg)

    client.receive_messages()
