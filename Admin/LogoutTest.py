import socket
import simplefix
from datetime import datetime
import time

class FixClientLogoutTest:

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
        self.fix_generator.append_pair(34, self.msg_seq_num)
        self.fix_generator.append_pair(49, self.sender_comp_id)
        self.fix_generator.append_pair(56, self.target_comp_id)
        self.fix_generator.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        self.fix_generator.append_pair(553, self.username)
        self.fix_generator.append_pair(554, self.password)
        return self.fix_generator.encode()

    def create_logout_msg(self):
        self.fix_generator = simplefix.FixMessage()
        self.fix_generator.append_pair(8, "FIX.4.4")
        self.fix_generator.append_pair(35, "5")  # Logout
        self.fix_generator.append_pair(34, self.msg_seq_num)
        self.fix_generator.append_pair(49, self.sender_comp_id)
        self.fix_generator.append_pair(56, self.target_comp_id)
        self.fix_generator.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        return self.fix_generator.encode()

    def logon(self):
        logon_msg = self.create_logon_msg()
        self.send_fix_msg(logon_msg)

    def send_logout(self):
        logout_msg = self.create_logout_msg()
        self.send_fix_msg(logout_msg)
        print("Sent Logout message.")

        response = self.sock.recv(8192)
        print(f"Received Logout response Logout Test{response.decode()}")

    def close_connection(self):
        self.sock.close()

if __name__ == "__main__":
    
    pricing_client = FixClientLogoutTest("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    pricing_client.logon()

    trading_client = FixClientLogoutTest("fixapidcrd.squaredfinancial.com", 10211, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    trading_client.logon()

    time.sleep(5)  
    
    pricing_client.send_logout()  

    pricing_client.close_connection()
    trading_client.close_connection()