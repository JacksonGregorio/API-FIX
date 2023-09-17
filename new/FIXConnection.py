import asyncio
import socket

import simplefix

default_credentials = {
    "username": 100019,
    "account": 100019,
    "target_comp_id": "DCRD",
}

pricing_session_credentials = {
    **default_credentials,
    "server": "fixapidcrd.squaredfinancial.com",
    "port": 10210,
    "sender_comp_id": "MD019",
    "password": "87MTgLw345dfb!",
    "ssl_enabled": "N",
    "reset_on_logon": "Y",
    "session": "pricing",
}

trading_session_credentials = {
    **default_credentials,
    "port": 8080,
    "server": "127.0.0.1",
    "sender_comp_id": "TD019",
    "password": "87MTgLw23wfe!",
    "ssl_enabled": "Y",
    "reset_on_logon": "N",
    "session": "trading",
}


class FIXConnection:
    def __init__(self, credentials, message_handler):
        self.message_handler = message_handler

        self.credentials = credentials
        self.username = default_credentials["username"]
        self.target_comp_id = default_credentials["target_comp_id"]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parser = simplefix.parser.FixParser()
        self.loop = asyncio.get_event_loop()

        self.sequence_number = 1

    @staticmethod
    def get_fix_message():
        return simplefix.FixMessage()

    @staticmethod
    def get_message_details(**kwargs):
        headers = kwargs.get('headers') or []
        parameters = kwargs.get('parameters') or []

        return [headers, parameters]

    async def connect(self):
        print("Connecting...")
        self.sock.setblocking(False)
        await self.loop.sock_connect(self.sock, (self.credentials["server"], self.credentials["port"]))

    async def listen(self):
        while True:
            data = await self.loop.sock_recv(self.sock, 8192)
            self.parser.append_buffer(data)

            while True:
                msg = self.parser.get_message()

                if not msg:
                    break

                self.message_handler.on_receive_message(msg)

    def build_message(self, **kwargs):
        headers, parameters = self.get_message_details(**kwargs)

        fix_message = self.get_fix_message()
        fix_message.append_pair(8, "FIX.4.4")
        fix_message.append_pair(56, self.target_comp_id)
        fix_message.append_pair(34, self.sequence_number)
        fix_message.append_time(52)
        fix_message.append_strings(headers, header=True)

        fix_message.append_strings(parameters)

        print(f"Sending message: {fix_message}")

        return fix_message.encode()

    async def send_message(self, **kwargs):
        headers, parameters = self.get_message_details(**kwargs)

        new_headers = headers + [f"49={self.credentials['sender_comp_id']}"]

        message = self.build_message(headers=new_headers, parameters=parameters)

        print(f"Sending {self.credentials['session']} message: {message}")
        await self.loop.sock_sendall(self.sock, message)

        self.sequence_number += 1
