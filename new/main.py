import time
from uuid import uuid4

from fix_api_client import FixApiClient

if __name__ == '__main__':
    fix_api_client = FixApiClient()

    print(f"Logon {fix_api_client.logon()}")
    #
    time.sleep(.2)
    #
    # print(f"heartbeat: {fix_api_client.heartbeat()}")
    #
    # time.sleep(.2)
    #
    # print(f"test_request: {fix_api_client.test_request()}")
    #
    # time.sleep(.2)
    #
    # print(f"resend_request: {fix_api_client.resend_request()}")
    #
    # time.sleep(.2)
    #
    # print(f"reject: {fix_api_client.reject()}")
    #
    # time.sleep(.2)
    #
    # print(f"sequence_reset: {fix_api_client.sequence_reset()}")
    #
    # time.sleep(.2)
    #
    # print(f"logout: {fix_api_client.logout()}")

    # Market Data Requests
    start_time = time.perf_counter()
    print(f"market_data_request: {fix_api_client.market_data_request('EURUSD.x')}")
    end_time = time.perf_counter()
    execution_time_milliseconds = (end_time - start_time) * 1000

    whole_milliseconds = int(execution_time_milliseconds)

    print(f"{whole_milliseconds:02}ms")

    time.sleep(.2)

    # print(f"market_data_request: {fix_api_client.market_data_request('WRONG_SYMBOL')}")
    # time.sleep(.2)

    # Duplicated id
    # request_id = str(uuid4())
    #
    # print(f"market_data_request: {fix_api_client.market_data_request(request_id=request_id, symbol='EURUSD.x')}")
    # time.sleep(.2)
    #
    # print(f"market_data_request: {fix_api_client.market_data_request(request_id=request_id, symbol='EURUSD.x')}")
    # time.sleep(.2)
