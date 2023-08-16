import socket
import simplefix
from datetime import datetime
import time

class FixClientHeartbeat:

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

    def connect_to_fix_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, self.port))
        return sock

    def send_fix_msg(self, msg):
        print(f"Sending FIX heartBeat message: {msg}")
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

    def create_heartbeat_msg(self):
        self.fix_generator = simplefix.FixMessage()
        self.fix_generator.append_pair(8, "FIX.4.4")
        self.fix_generator.append_pair(35, "0")  # Heartbeat
        self.fix_generator.append_pair(34, 3)  # Sequence number
        self.fix_generator.append_pair(49, self.sender_comp_id)
        self.fix_generator.append_pair(56, self.target_comp_id)
        self.fix_generator.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        return self.fix_generator.encode()

    def send_heartbeat(self):
        heartbeat_msg = self.create_heartbeat_msg()
        self.send_fix_msg(heartbeat_msg)

    def close_connection(self):
        self.sock.close()
    def receive_heartbeat_response(self):
        data = self.sock.recv(8192)
        if data:
            self.parser.append_buffer(data)
            while True:
                msg = self.parser.get_message()
                if msg is None:
                    break
                print(f"Received FIX HeartBeat: {msg}")
                break
        else:
            print("No data received.")

    def send_heartbeat_and_receive_response(self):
        self.logon()
        try:
            while True:
                self.send_heartbeat()
                self.receive_heartbeat_response()
                time.sleep(1)
                break
        except KeyboardInterrupt:
            pass
        finally:
            self.close_connection()

if __name__ == "__main__":
    client = FixClientHeartbeat("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.send_heartbeat_and_receive_response()