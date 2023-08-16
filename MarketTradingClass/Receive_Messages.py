import socket
from datetime import datetime
import simplefix
import time

class ReceiveMessage:

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