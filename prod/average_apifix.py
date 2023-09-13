import time

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

    time.sleep(.2)

    responses_execution_time = []

    for i in range(10):
        responses_execution_time.append(execute(lambda: fix_api_client.market_data_request('EURUSD.x')))
        time.sleep(.2)

    average = sum(responses_execution_time) / len(responses_execution_time)
    print(f"Average execution time: {average}ms")
