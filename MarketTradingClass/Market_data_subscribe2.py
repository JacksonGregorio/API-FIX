import socket
import simplefix
from datetime import datetime
import time
from Create_heartbeat_msg import CreateHeartBeatMessage

class FixClientQuotesMarketSubscribe:

    def __init__(self, server, port, sender_comp_id, target_comp_id, username, password):
        self.server = server
        self.port = port
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self.username = username
        self.password = password
        self.parser = simplefix.FixParser()
        self.fix_generator = simplefix.FixMessage()
        self.sock = self.connect_to_fix_server()
        self.msg_seq_num = 1  # Initialize message sequence number

    def connect_to_fix_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, self.port))
        return sock

    def send_fix_msg(self, msg):
        print(f"Sending FIX message: {msg}")
        self.sock.sendall(msg)

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
    
    def create_market_data_request_msg_sub2(self, md_req_id, symbol):
        self.fix_generator = simplefix.FixMessage()
        self.fix_generator.append_pair(8, "FIX.4.4")
        self.fix_generator.append_pair(35, "V")  # Market Data Request
        self.fix_generator.append_pair(34, self.msg_seq_num)  # Use the current sequence number
        self.fix_generator.append_pair(49, self.sender_comp_id)
        self.fix_generator.append_pair(56, self.target_comp_id)
        self.fix_generator.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])

        self.fix_generator.append_pair(262, md_req_id)  # MDReqID
        self.fix_generator.append_pair(263, "1")  # SubscriptionRequestType (Snapshot + Updates)
        self.fix_generator.append_pair(264, "0")  # MarketDepth
        self.fix_generator.append_pair(265, "0")  # MDUpdateType (Full Refresh)

        # Bid and Ask entries
        self.fix_generator.append_pair(267, "2")  # NoMDEntryTypes
        self.fix_generator.append_pair(269, "0")  # MDEntryType (Bid)
        self.fix_generator.append_pair(269, "1")  # MDEntryType (Offer)

        self.fix_generator.append_pair(146, "1")  # NoRelatedSym
        self.fix_generator.append_pair(55, symbol)  # Symbol (e.g., "EURUSD.x")
        return self.fix_generator.encode()
    
    
    def logon(self):
        logon_msg = self.create_logon_msg()
        self.send_fix_msg(logon_msg)


    def get_quote_sub2(self, md_req_id_base, symbol):
        self.msg_seq_num += 1  # Increment the sequence number for each new message
        md_req_id = f"{md_req_id_base}_{self.msg_seq_num}"  # Append unique sequence number to base md_req_id
        md_request_msg = self.create_market_data_request_msg_sub2(md_req_id, symbol)
        self.send_fix_msg(md_request_msg)

    def listen_for_quotes_sub2(self):
        while True:
            data = self.sock.recv(8192)
            if data:
                self.parser.append_buffer(data)
                while True:
                    msg = self.parser.get_message()
                    if msg is None:
                        break
                    print(f"Received FIX message: {msg}")

                    msg_type = msg.get(35)
                    if msg_type and msg_type.decode() == "W":  # Market Data Snapshot / Full Refresh
                        return self.process_market_data_snapshot(msg)
            else:
                break

    def get_quote_Snapshot(self, md_req_id_base, symbol):
        self.msg_seq_num += 1  # Increment the sequence number for each new message
        md_req_id = f"{md_req_id_base}_{self.msg_seq_num}"  # Append unique sequence number to base md_req_id
        md_request_msg = self.create_market_data_request_msg_sub2(md_req_id, symbol)
        self.send_fix_msg(md_request_msg)

    def listen_for_quotes_Snapshot(self):
        while True:
            data = self.sock.recv(8192)
            if data:
                self.parser.append_buffer(data)
                while True:
                    msg = self.parser.get_message()
                    if msg is None:
                        break
                    print(f"Received FIX message: {msg}")

                    msg_type = msg.get(35)
                    if msg_type and msg_type.decode() == "W":  # Market Data Snapshot / Full Refresh
                        return self.process_market_data_snapshot(msg)
            else:
                break


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