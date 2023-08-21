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
    self.sequence_number = 1

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

  def send_message(self, session, **kwargs):
    fix_message = self.build_message(**kwargs)
    
    try:
      session.sendall(fix_message)
    except BrokenPipeError:
      print("BrokenPipeError: disconnected")
      return None

    print(f"Sending message: {fix_message}")

    self.sequence_number += 1

    return self.listen_to_response(session)

  def send_pricing_session(self, **kwargs):
    headers = kwargs.get('headers') or []
    parameters = kwargs.get('parameters') or []
    headers += [f"49={pricing_session_credentials['sender_comp_id']}"]

    return self.send_message(session=self.pricing_session, headers=headers, parameters=parameters)

  # def send_trading_session(self, parameters):
  #   parameters += [f"49={trading_session_credentials['sender_comp_id']}"]

  #   return self.send_message(self.trading_session, parameters)

  def listen_to_response(self, session):
    parser = simplefix.parser.FixParser()

    data = session.recv(8192)

    parser.append_buffer(data)

    return parser.get_message()

  def build_message(self, **kwargs):
    headers = kwargs.get('headers')
    parameters = kwargs.get('parameters')

    fix_message = self.get_fix_message()
    fix_message.append_pair(8, "FIX.4.4")
    fix_message.append_pair(56, self.target_comp_id)
    fix_message.append_pair(34, self.sequence_number)
    fix_message.append_time(52)
    fix_message.append_strings(headers, header=True)

    fix_message.append_strings(parameters)

    return fix_message.encode()

  def heartbeat(self):
    headers = ["35=0"]

    return self.send_pricing_session(headers=headers)

  def test_request(self):
    headers = ["35=1"]
    parameters = [f"112={uuid4()}"]
    return self.send_pricing_session(headers=headers, parameters=parameters)

  def logon(self):
    headers = [
      "35=A",
    ]

    parameters = [
      "98=0",
      "108=30",
      "141=Y",
      f"553={self.username}",
      f"554={pricing_session_credentials['password']}",
    ]

    return self.send_pricing_session(headers=headers, parameters=parameters)

  def logout(self):
    headers = ["35=5"]

    return self.send_pricing_session(headers=headers)

  def resend_request(self):
    headers = ["35=2"]
    parameters = ["7=0", "16=0"]

    return self.send_pricing_session(headers=headers, parameters=parameters)

  def reject(self):
    headers = ["35=3"]
    parameters = ["45=1"]

    return self.send_pricing_session(headers=headers, parameters=parameters)

  def business_reject(self):
    headers = ["35=j"]
    """Preciso entender melhor oq é isso e quando é usado"""
    parameters = ["45=1"]

    return self.send_pricing_session(headers=headers, parameters=parameters)

  def sequence_reset(self):
    headers = ["35=4"]
    parameters = ["36=1"]

    return self.send_pricing_session(headers=headers, parameters=parameters)