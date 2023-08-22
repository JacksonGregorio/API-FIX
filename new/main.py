import time
# from uuid import uuid4

from fix_api_client import FixApiClient


def execute(func):
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000

    return elapsed_time


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
    responses_execution_time = []

    for i in range(10):
        responses_execution_time.append(execute(lambda: fix_api_client.market_data_request('EURUSD.x')))
        time.sleep(.2)

    average = sum(responses_execution_time) / len(responses_execution_time)
    print(f"Average execution time: {average}ms")

    # print(f"market_data_request: {fix_api_client.market_data_request('EURUSD.x')}")


    # time.sleep(.2)

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
