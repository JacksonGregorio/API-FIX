import asyncio
import os

from FIXConnection import FIXConnection, pricing_session_credentials, trading_session_credentials
from fix_api_client import FixApiClient
from price_listener import PriceListener
from message_handler import MessageHandler

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    price_listener = PriceListener()
    message_handler = MessageHandler(price_listener=price_listener)

    pricing_connection = FIXConnection(credentials=pricing_session_credentials, message_handler=message_handler)
    trading_connection = FIXConnection(credentials=trading_session_credentials, message_handler=message_handler)

    await pricing_connection.connect()
    await trading_connection.connect()

    print("Start fix api client")
    fix_api_client = FixApiClient(pricing=pricing_connection, trading=trading_connection)

    await fix_api_client.logon()
    await fix_api_client.logon(trading_session=True)

    print("Start listening to messages...")
    asyncio.create_task(pricing_connection.listen())
    asyncio.create_task(trading_connection.listen())

    print("Starting heartbeat system")
    asyncio.create_task(fix_api_client.heartbeat())

    await fix_api_client.market_data_request(symbol="EURUSD.x")

    last_bid_price = 0
    change_times = 0

    while True:
        await asyncio.sleep(.5)
        bid_price = pricing_connection.message_handler.price_listener.bid
        ask_price = pricing_connection.message_handler.price_listener.ask
        #
        if bid_price != last_bid_price:
            print(f'Bid Price: {bid_price} ~ Ask Price: {ask_price} ~ changed {change_times} times ~ last bid: {last_bid_price}')
        
            last_bid_price = pricing_connection.message_handler.price_listener.bid
            change_times += 1
        
        if change_times == 5:
            print(f'Opening BUY order at Bid price: {bid_price} ~ Ask Price: {ask_price}')
        
            asyncio.create_task(fix_api_client.new_order(symbol="EURUSD.x", side=1, order_type=1, lot_size=1000))
        
            await asyncio.sleep(5)

            print(f'CLOSING BUY order at Bid price: {bid_price} ~ Ask Price: {ask_price}')
        
            asyncio.create_task(fix_api_client.new_order(symbol="EURUSD.x", side=2, order_type=1, lot_size=1000))

    # print("=========")
    #
    # print("Sending market order message")
    #
    # await fix_api_client.new_order(symbol="EURUSD.x", side=1, order_type=1, lot_size=1000)
    # await asyncio.sleep(10)
    #
    # print("=========")
    #
    #
    # print("Sending market order message")
    #
    # await fix_api_client.new_order(symbol="EURUSD.x", side=2, order_type=1, lot_size=1000)
    # await asyncio.sleep(2)
    #
    # print("=========")


    # print("Sending limit IOC order message")

    # limit_ioc_order = await fix_api_client.new_order(
    #     symbol="EURUSD.x",
    #     side=2,
    #     order_type=2,
    #     lot_size=1000,
    #     price=1.07950,
    #     time_in_force=4,
    # )

    # await asyncio.sleep(3)

    # print("=========")

    

    # print("Sending limit FOK order message")

    # limit_fok_order = await fix_api_client.new_order(
    #     symbol="EURUSD.x",
    #     side=1,
    #     order_type=2,
    #     lot_size=1000,
    #     price=1.08350,
    #     time_in_force=4
    # )

    # await asyncio.sleep(2)

    # print("=========")

    

    # print("Sending below limit order message")

    # below_limit = await fix_api_client.new_order(symbol="EURUSD.x", side=1, order_type=1, lot_size=100)

    # await asyncio.sleep(2)

    # print("=========")

    

    # print("Sending above limit order message")

    # below_limit = await fix_api_client.new_order(symbol="EURUSD.x", side=1, order_type=1, lot_size=1000000000)

    # await asyncio.sleep(4)

    # print("=========")


    # print("Sending cancel order IOC")
    # await fix_api_client.order_cancel(request_id='UmalJDvGSwQdO-ywvkB', side=2)

    # await asyncio.sleep(2)

    # print("=========")


    # print("Sending cancel order FOK")

    

    # await fix_api_client.order_cancel(request_id=limit_fok_order, side=1)

    # while True:
    #     await asyncio.sleep(1)


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
