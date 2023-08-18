import socket
import simplefix
from datetime import datetime
import time

class FixClientSequenciReset:

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
        

    def logon(self):
        logon_msg = self.create_logon_msg()
        self.send_fix_msg(logon_msg)

    def receive_messages(self):
        data = self.sock.recv(8192)
        if data:
            self.parser.append_buffer(data)
            while True:
                msg = self.parser.get_message()
                if msg is None:
                    break
                msg_type = msg.get(35)
                if msg_type:
                    msg_type = msg_type
                    print(f"Received FIX message Sequenci Reset: {msg}")
                    if msg_type == b"4":
                        gap_fill_flag = msg.get(123)
                        if gap_fill_flag and gap_fill_flag == b"Y":
                            new_seq_num = msg.get(36)
                            if new_seq_num:
                                self.msg_seq_num = int(new_seq_num)
                                print(f"Updated sequence number to {self.msg_seq_num}")
                break
        

    def close_connection(self):
        self.sock.close()

if __name__ == "__main__":
    pricing_client = FixClientSequenciReset("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    pricing_client.logon()

    trading_client = FixClientSequenciReset("fixapidcrd.squaredfinancial.com", 10211, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    trading_client.logon()

    try:
        while True:
            pricing_client.receive_messages()
            pricing_client.create_logon_msg()
            time.sleep(1)
    finally:
        pricing_client.close_connection()
        trading_client.close_connection()