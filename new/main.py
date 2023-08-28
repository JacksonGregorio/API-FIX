import asyncio
import time
import os

from FIXConnection import FIXConnection, pricing_session_credentials, trading_session_credentials
from fix_api_client import FixApiClient

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    pricing_connection = FIXConnection(credentials=pricing_session_credentials)
    trading_connection = FIXConnection(credentials=trading_session_credentials)

    await pricing_connection.connect()
    await trading_connection.connect()

    print("Start fix api client")
    fix_api_client = FixApiClient(pricing=pricing_connection, trading=trading_connection)

    await fix_api_client.logon()
    await fix_api_client.logon(trading_session=True)

    print("Start listening to messages...")
    asyncio.create_task(pricing_connection.listen())
    asyncio.create_task(trading_connection.listen())

    print("Sending heartbeat")
    await fix_api_client.heartbeat()

    await asyncio.sleep(2)

    print("=========")

    print("Sending market order message")

    market_order = await fix_api_client.new_order(symbol="EURUSD.x", side=1, order_type=1, lot_size=1000)
    await asyncio.sleep(2)

    print("=========")


    print("Sending limit IOC order message")

    limit_ioc_order = await fix_api_client.new_order(
        symbol="EURUSD.x",
        side=1,
        order_type=2,
        lot_size=1000,
        price=1.08320,
        time_in_force=3
    )

    await asyncio.sleep(2)

    print("=========")

    

    print("Sending limit FOK order message")

    limit_fok_order = await fix_api_client.new_order(
        symbol="EURUSD.x",
        side=1,
        order_type=2,
        lot_size=1000,
        price=1.08350,
        time_in_force=4
    )

    await asyncio.sleep(2)

    print("=========")

    

    print("Sending below limit order message")

    below_limit = await fix_api_client.new_order(symbol="EURUSD.x", side=1, order_type=1, lot_size=100)

    await asyncio.sleep(2)

    print("=========")

    

    print("Sending above limit order message")

    below_limit = await fix_api_client.new_order(symbol="EURUSD.x", side=1, order_type=1, lot_size=1000000000)

    await asyncio.sleep(4)

    print("=========")


    print("Sending cancel order IOC")
    await fix_api_client.order_cancel(request_id=limit_ioc_order, side=1)

    await asyncio.sleep(2)

    print("=========")


    print("Sending cancel order FOK")

    

    await fix_api_client.order_cancel(request_id=limit_fok_order, side=1)

    await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())

#
#     print(f"Logon {fix_api_client.logon(trading_session=True)}")
#     #
#     time.sleep(.2)
#     #
#     # print(f"heartbeat: {fix_api_client.heartbeat()}")
#     #
#     # time.sleep(.2)
#     #
#     print(f"test_request: {fix_api_client.test_request()}")
#     #
#     # time.sleep(.2)
#     #
#     # print(f"resend_request: {fix_api_client.resend_request()}")
#     #
#     # time.sleep(.2)
#     #
#     # print(f"reject: {fix_api_client.reject()}")
#     #
#     # time.sleep(.2)
#     #
#     # print(f"sequence_reset: {fix_api_client.sequence_reset()}")
#     #
#     # time.sleep(.2)
#     #
    # print(f"logout: {fix_api_client.logout()}")
#
#     # Market Data Requests
#
#     # print(f"market_data_request: {fix_api_client.market_data_request('EURUSD.x')}")
#
#     # fix_api_client.listen_to_response(fix_api_client.pricing_session)
#
#     # time.sleep(.2)
#
#     # print(f"market_data_request: {fix_api_client.market_data_request('WRONG_SYMBOL')}")
#     # time.sleep(.2)
#
#     # Duplicated id
#     request_id = str(uuid4())
#     #
#     # print(f"market_data_request: {fix_api_client.market_data_request(request_id=request_id, symbol='EURUSD.x')}")
#     # time.sleep(.2)
#     #
#     # print(f"market_data_request: {fix_api_client.market_data_request(request_id=request_id, symbol='EURUSD.x')}")
#     # time.sleep(.2)
#
#     # Market order
#     print(f"new_order: {fix_api_client.new_order(request_id='test', symbol='EURUSD.x')}")
#     time.sleep(5)
#
#     # Limit IOC
#
#     # Limit FOK
#
#     # < Min qty
#
#     # > Max qty
#
#     # Order cancel request
#
#     # Order cancel reject
#
#     print(f"order_status: {fix_api_client.order_status(request_id='test')}")
#
#     time.sleep(1)
#     fix_api_client.listen_to_response(fix_api_client.trading_session)
