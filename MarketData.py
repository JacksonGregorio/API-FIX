import socket
import simplefix
from datetime import datetime

class FixClientMarketDataRequest:


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
        self.msg_seq_num = 1
        self.login_successful = False

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

    def create_market_data_request_msg(self, md_req_id, symbol):
        self.fix_generator.append_pair(8, "FIX.4.4")
        self.fix_generator.append_pair(35, "V")
        self.fix_generator.append_pair(34, self.msg_seq_num)
        self.fix_generator.append_pair(49, self.sender_comp_id)
        self.fix_generator.append_pair(56, self.target_comp_id)
        self.fix_generator.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        self.fix_generator.append_pair(262, md_req_id)
        self.fix_generator.append_pair(263, 1)
        self.fix_generator.append_pair(264, 0)
        self.fix_generator.append_pair(267, 2)
        self.fix_generator.append_pair(269, "0")
        self.fix_generator.append_pair(269, "1")
        self.fix_generator.append_pair(146, 1)
        self.fix_generator.append_pair(55, symbol)
        return self.fix_generator.encode()

    def logon(self):
        logon_msg = self.create_logon_msg()
        self.send_fix_msg(logon_msg)

    def get_quote(self, md_req_id_base, symbol):
        self.msg_seq_num += 1
        md_req_id = f"{md_req_id_base}_{self.msg_seq_num}"
        md_request_msg = self.create_market_data_request_msg(md_req_id, symbol)
        self.send_fix_msg(md_request_msg)

    def listen_for_quotes(self):

        
        while True:
            data = self.sock.recv(8192)
            if data:
                self.parser.append_buffer(data)
                while True:
                    msg = self.parser.get_message()
                    if msg is None:
                        break
                    print(f"Received FIX message: {msg}")

    def close_connection(self):
        self.sock.close()

if __name__ == "__main__":
    client = FixClientMarketDataRequest("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.logon()
    client.get_quote("EURUSD_MDReqID", "EURUSD.x")

    try:
        while True:
            bid, ask = client.listen_for_quotes()
    except KeyboardInterrupt:
        pass
    finally:
        client.close_connection()