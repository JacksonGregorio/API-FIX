import socket
from datetime import datetime
import simplefix

class SendMessage:

    def send_message(self, msg):
        # Incrementa o número de sequência para a próxima mensagem
        self.msg_seq_num += 1
        self.sock.sendall(msg)
        print(f"Cancel Order: {msg}")

    