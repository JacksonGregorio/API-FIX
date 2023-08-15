from HeartBeat import FixClientHeartbeat;
from SequenciReset import FixClientSequenciReset;
from ReactTeste import FixClientReactTeste;
from SequenciReset import FixClientSequenciReset;
from RequestTest import FixClientRequestTest;
from NewLogout import FixClientLogoutTestNew;
from Login import  FixClientLogin;
import time


def run_fix_clients():
    pricing_client = FixClientLogin("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    pricing_client.logon()

    trading_client = FixClientLogin("fixapidcrd.squaredfinancial.com", 10211, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    trading_client.logon()

    try:
        while True:
            pricing_client.receive_messages()
            pricing_client.create_logon_msg()
            time.sleep(1)
            break
    except KeyboardInterrupt:
        pass
    finally:
        pricing_client.close_connection()
        trading_client.close_connection()

if __name__ == "__main__":
    run_fix_clients()

print("End Login Test")
time.sleep(1)

heartbeat_instance = FixClientHeartbeat("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")


heartbeat_instance.send_heartbeat_and_receive_response()
time.sleep(1)
print("End HeartBeat Test")
time.sleep(1)

def run_logout_clients():
    pricing_client = FixClientLogoutTestNew("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    pricing_client.logon()

    trading_client = FixClientLogoutTestNew("fixapidcrd.squaredfinancial.com", 10211, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    trading_client.logon()

    try:
        while True:
            pricing_client.receive_messages()
            pricing_client.create_logon_msg()
            time.sleep(1)
            break
    except KeyboardInterrupt:
        pricing_client.send_logout()  # Send Logout message when KeyboardInterrupt is detected
        trading_client.send_logout()  # Send Logout message for the trading client
    finally:
        pricing_client.close_connection()
        trading_client.close_connection()

if __name__ == "__main__":
    run_logout_clients()

print("End Logout Test")
time.sleep(1)

def run_request_clients():
    pricing_client = FixClientRequestTest("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    pricing_client.logon()

    trading_client = FixClientRequestTest("fixapidcrd.squaredfinancial.com", 10211, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    trading_client.logon()

    try:
        while True:
            pricing_client.receive_messages()
            pricing_client.create_logon_msg()
            time.sleep(1)
            break
    except KeyboardInterrupt:
        pricing_client.send_logout()  
        trading_client.send_logout()  
    finally:
        pricing_client.close_connection()
        trading_client.close_connection()

if __name__ == "__main__":
    run_request_clients()
print("End Request Test")
time.sleep(1)


def run_sequenci_reset_clients():
    pricing_client = FixClientSequenciReset("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    pricing_client.logon()

    trading_client = FixClientSequenciReset("fixapidcrd.squaredfinancial.com", 10211, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    trading_client.logon()

    try:
        while True:
            pricing_client.receive_messages()
            pricing_client.create_logon_msg()
            time.sleep(1)
            break
    finally:
        pricing_client.close_connection()
        trading_client.close_connection()

if __name__ == "__main__":
    run_sequenci_reset_clients()
print("End Sequenci Test")

time.sleep(1)

def run_react_test_clients():
    pricing_client = FixClientReactTeste("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    pricing_client.logon()

    trading_client = FixClientReactTeste("fixapidcrd.squaredfinancial.com", 10211, "TD019", "DCRD", "100019", "87MTgLw23wfe!")
    trading_client.logon()

    try:
        while True:
            pricing_client.receive_messages()
            pricing_client.create_logon_msg()
            time.sleep(1)
            break
    except KeyboardInterrupt:
        pricing_client.close_connection()
        trading_client.close_connection()

if __name__ == "__main__":
    run_react_test_clients()
time.sleep(1)
print("End React Test")
time.sleep(1)
print("End Test")





