from uuid import uuid4

import socket
import simplefix

default_credentials = {
    "username": 100019,
    "server": "fixapidcrd.squaredfinancial.com",
    "target_comp_id": "DCRD",
}

pricing_session_credentials = {
    "port": 10210,
    "sender_comp_id": "MD019",
    "password": "87MTgLw345dfb!",
    "ssl_enabled": "N",
    "reset_on_logon": "Y",
}

trading_session_credentials = {
    "port": 10211,
    "sender_comp_id": "TD019",
    "password": "87MTgLw23wfe!",
    "ssl_enabled": "Y",
    "reset_on_logon": "N",
}

class FixApiClient:

  def __init__(self):
    self.username = default_credentials["username"]
    self.server = default_credentials["server"]
    self.target_comp_id = default_credentials["target_comp_id"]
    self.pricing_session = self.get_pricing_session()
    self.trading_session = self.get_trading_session()
    self.sequence_number = 0

  @staticmethod
  def get_fix_message():
    return simplefix.FixMessage()

  def get_pricing_session(self):
    return self._get_session(pricing_session_credentials)
  
  def get_trading_session(self):
    return self._get_session(trading_session_credentials)
  
  def _get_session(self, credentials):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((self.server, credentials["port"]))

    return sock

  def send_message(self, session, parameters):
    fix_message = self.build_message(parameters)
    
    try:
      session.sendall(fix_message)
    except BrokenPipeError:
      print("BrokenPipeError: disconnected")
      return None

    print(f"Sending message: {fix_message}")

    self.sequence_number += 1

    return self.listen_to_response(session)

  def send_pricing_session(self, parameters):
    parameters += [f"49={pricing_session_credentials['sender_comp_id']}"]

    return self.send_message(self.pricing_session, parameters)

  def send_trading_session(self, parameters):
    parameters += [f"49={trading_session_credentials['sender_comp_id']}"]

    return self.send_message(self.trading_session, parameters)

  def listen_to_response(self, session):
    parser = simplefix.parser.FixParser()
    data = session.recv(8192)

    print(data)

    if data:
      parser.append_buffer(data)
      while True:
        msg = parser.get_message()
        if msg is None:
            break
        print(f"Received FIX message: {msg}")
        break
    # if not data:
    #   return None

    # parser.append_buffer(data)

    # return parser.get_message()

  def build_message(self, parameters):
    fix_message = self.get_fix_message()
    fix_message.append_pair(8, "FIX.4.4")
    fix_message.append_pair(56, self.target_comp_id)
    fix_message.append_pair(34, self.sequence_number)
    fix_message.append_time(52)

    fix_message.append_strings(parameters)

    return fix_message.encode()

  def heartbeat(self):
    parameters = ["35=0"]

    return self.send_pricing_session(parameters)

  def test_request(self):
    parameters = ["35=1", f"112={uuid4()}"]
    return self.send_pricing_session(parameters)

  def logon(self):
    parameters = [
      "35=A",
      "98=0",
      "108=60",
      "141=Y",
      f"553={self.username}",
      f"554={pricing_session_credentials['password']}",
    ]

    return self.send_pricing_session(parameters)

  def logout(self):
    parameters = ["35=5"]

    return self.send_pricing_session(parameters)

  def resend_request(self):
    parameters = ["35=2", "7=0", "16=0"]

    return self.send_pricing_session(parameters)

  def reject(self):
    parameters = ["35=3", "45=1"]

    return self.send_pricing_session(parameters)

  def business_reject(self):
    """Preciso entender melhor oq é isso e quando é usado"""
    parameters = ["35=j", "45=1"]

    return self.send_pricing_session(parameters)

  def sequence_reset(self):
    parameters = ["35=4", "36=0"]

    return self.send_pricing_session(parameters)