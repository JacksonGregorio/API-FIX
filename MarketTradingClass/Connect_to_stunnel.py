import socket
from datetime import datetime
import simplefix

class ConnectToStunnel:

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

    def connect_to_stunnel(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, self.port))
        return sock