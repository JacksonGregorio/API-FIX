import socket
from datetime import datetime
import simplefix

class SendMessage:

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

    def send_message(self, msg):
        # Incrementa o número de sequência para a próxima mensagem
        self.msg_seq_num += 1
        self.sock.sendall(msg)
        print(f"Cancel Order: {msg}")

    