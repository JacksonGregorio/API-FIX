import time

import MetaTrader2 as Mt2

oanda = dict(
    login=4033529,
    password="2104asdf",
    server="OANDA-Live-1",
    path="C:/Program Files/Oanda/terminal64.exe",
)


def execute(func):
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000

    return elapsed_time


if __name__ == '__main__':

    connection = Mt2.initialize(
        login=oanda["login"],
        password=oanda["password"],
        server=oanda["server"],
        path=oanda["path"]
    )

    responses_execution_time = []

    for i in range(10):
        responses_execution_time.append(execute(lambda: Mt2.symbol_info_tick("EURUSD.sml")))
        time.sleep(.2)

    average = sum(responses_execution_time) / len(responses_execution_time)
    print(f"Average execution time: {average}ms")
