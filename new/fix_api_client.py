from datetime import datetime
from uuid import uuid4

from FIXConnection import trading_session_credentials, pricing_session_credentials


class FixApiClient:
    def __init__(self, pricing, trading):
        self.pricing = pricing
        self.trading = trading

    async def heartbeat(self):
        headers = ["35=0"]

        await self.pricing.send_message(headers=headers)

    def test_request(self):
        headers = ["35=1"]
        parameters = [f"112={uuid4()}"]
        return self.pricing.send_message(headers=headers, parameters=parameters)

    async def logon(self, trading_session=False):
        headers = [
            "35=A",
        ]

        parameters = [
            "98=0",
            "108=30",
            "141=Y",
        ]

        if trading_session:
            parameters += [
                f"553={self.trading.username}",
                f"554={self.trading.credentials['password']}",
            ]

            await self.trading.send_message(headers=headers, parameters=parameters)
        else:
            parameters += [
                f"553={self.pricing.username}",
                f"554={self.pricing.credentials['password']}",
            ]

            await self.pricing.send_message(headers=headers, parameters=parameters)

    async def logout(self):
        headers = ["35=5"]

        await self.pricing.send_message(headers=headers)

    def resend_request(self):
        headers = ["35=2"]
        parameters = ["7=0", "16=0"]

        return self.pricing.send_message(headers=headers, parameters=parameters)

    def reject(self):
        headers = ["35=3"]
        parameters = ["45=3"]

        return self.pricing.send_message(headers=headers, parameters=parameters)

    def business_reject(self):
        headers = ["35=j"]
        """Preciso entender melhor oq é isso e quando é usado"""
        parameters = ["45=1"]

        return self.pricing.send_message(headers=headers, parameters=parameters)

    def sequence_reset(self):
        headers = ["35=4"]
        parameters = ["36=1"]

        return self.pricing.send_message(headers=headers, parameters=parameters)

    # Market data requests
    async def market_data_request(self, symbol: str, request_id: str = None):
        if not request_id:
            request_id = uuid4()

        headers = ["35=V"]
        parameters = [
            f"262={request_id}",
            "263=1",
            "264=0",
            "267=1",
            "269=1",
            "146=1",
            f"55={symbol}",
        ]

        await self.pricing.send_message(headers=headers, parameters=parameters)

    async def new_order(self, symbol: str, request_id: str = None):
        if not request_id:
            request_id = uuid4()

        headers = ["35=D"]

        parameters = [
            f"11={request_id}",
            f"1={self.trading.credentials['account']}",
            f"55={symbol}",
            "54=1",
            "38=1",
            "40=1",
            "59=1",
            f"60={datetime.utcnow().strftime('%Y%m%d-%H:%M:%S')}",
        ]

        await self.trading.send_message(headers=headers, parameters=parameters)

    async def order_cancel(self, request_id: str, side: int):
        headers = ["35=F"]

        parameters = [
            f"11={request_id}",
            f"1={self.trading.credentials['account']}",
            f"41={request_id}",
            f"54={side}",
            f"60={datetime.utcnow().strftime('%Y%m%d-%H:%M:%S')}",
        ]

        await self.trading.send_message(headers=headers, parameters=parameters)

    def order_status(self, request_id: str = None):
        headers = ["35=H"]
        parameters = [
            f"37=1",
            f"11={request_id}",
            f"1={trading_session_credentials['account']}",
        ]

        return self.trading.send_message(headers=headers, parameters=parameters)

