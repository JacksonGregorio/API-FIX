import socket
import simplefix
from datetime import datetime
import time
from FixClientQuotes import FixClientQuotes
from Connect_to_stunnel import ConnectToStunnel;
from Calculate_checksum import CalculateCheck;
from Create_logon_msg import CreateLogonMessage;
from Send_Message import SendMessage;
from Create_heartbeat_msg import CreateHeartBeatMessage;
from Receive_Messages import ReceiveMessage;
from Create_order_cancel_msg import CreateOrderCancel;
from Create_new_order_single_msg_opposie import CreateOrderSingleOpposite;
from Create_new_order_single_msg import CreateOrderSingle;
from Create_order_status_request_msg import CreateOrderStatus;
from Market_data_multiple_depht import FixClientQuotesMarketMultiple;
from Market_data_unsubscribe import FixClientQuotesMarketUnsubscribe;
from Market_data_subscribe2 import FixClientQuotesMarketSubscribe;

print("Choose an option:")
print("Enter 1 to run Functions of Market Data")
print("Enter 2 to run Functions of Market Data Wrong Symbol")
print("Enter 3 to run Functions of Market Data send duplicate MDReqID")
print("Enter 4 to run Functions of Market Data subscribe one depth level")
print("Enter 5 to run Functions of Market Data subscribe multi level")
print("Enter 6 to run Functions of Market Data unsubscribe")
print("Enter 7 to run Functions of Market Data  Market Data Snapshot ")

print("Enter 10 to run Functions of Trading")

choice = input("Option: ")

if choice == '1':

    client = FixClientQuotes("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.logon()
    client.get_quote("EURUSD_MDReqID", "EURUSD.x")

    try:
        while True:
            #time.sleep(1)
            bid, ask = client.listen_for_quotes()
            print(f"Bid: {bid}, Ask: {ask}")

            if int(time.time()) % 30 == 0:
               CreateHeartBeatMessage.send_heartbeat()
    except KeyboardInterrupt:
        pass
    finally:
        client.close_connection()

elif choice == '2':
    client = FixClientQuotes("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.logon()
    client.get_quote("XXXXXX_MDReqID", "XXXXXX.x")

    try:
        while True:
            #time.sleep(1)
            bid, ask = client.listen_for_quotes()
            print(f"Bid: {bid}, Ask: {ask}")

            if int(time.time()) % 30 == 0:
               CreateHeartBeatMessage.send_heartbeat()
    except KeyboardInterrupt:
        pass
    finally:
        client.close_connection()

elif choice == '3':
    client = FixClientQuotes("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.logon()
    client.get_quote("EURUSD_MDReqID", "EURUSD_MDReqID")

    try:
        while True:
            #time.sleep(1)
            bid, ask = client.listen_for_quotes()
            print(f"Bid: {bid}, Ask: {ask}")

            if int(time.time()) % 30 == 0:
               CreateHeartBeatMessage.send_heartbeat()
    except KeyboardInterrupt:
        pass
    finally:
        client.close_connection()

elif choice == '4':

    client = FixClientQuotesMarketSubscribe("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.logon()
    client.get_quote_sub2("EURUSD_MDReqID", "EURUSD.x")

    try:
        while True:
            #time.sleep(1)
            bid, ask = client.listen_for_quotes_sub2()
            print(f"Bid: {bid}, Ask: {ask}")

            if int(time.time()) % 30 == 0:
               CreateHeartBeatMessage.send_heartbeat("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    except KeyboardInterrupt:
        pass
    finally:
        client.close_connection()

elif choice == '5':

    client = FixClientQuotesMarketMultiple("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.logon()
    client.get_quote_multi("EURUSD_MDReqID", "EURUSD.x")

    try:
        while True:
            #time.sleep(1)
            bid, ask = client.listen_for_quotes_multi()
            print(f"Bid: {bid}, Ask: {ask}")

            if int(time.time()) % 30 == 0:
               CreateHeartBeatMessage.send_heartbeat("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    except KeyboardInterrupt:
        pass
    finally:
        client.close_connection()

elif choice == '6':

    client = FixClientQuotesMarketUnsubscribe("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.logon()
    client.get_quote_unsubscribe("EURUSD_MDReqID", "EURUSD.x")

    try:
        while True:
            #time.sleep(1)
            bid, ask = client.listen_for_quotes_unsubscribe()
            print(f"Bid: {bid}, Ask: {ask}")

            if int(time.time()) % 30 == 0:
               CreateHeartBeatMessage.send_heartbeat("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    except KeyboardInterrupt:
        pass
    finally:
        client.close_connection()

elif choice == '7':

    client = FixClientQuotes("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client.logon()
    client.get_quote_Snapshot("EURUSD_MDReqID", "EURUSD.x")

    try:
        while True:
            #time.sleep(1)
            bid, ask = client.listen_for_quotes_Snapshot()
            print(f"Bid: {bid}, Ask: {ask}")

            if int(time.time()) % 30 == 0:
               CreateHeartBeatMessage.send_heartbeat("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    except KeyboardInterrupt:
        pass
    finally:
        client.close_connection()


elif choice == '10':
    logon_msg = CreateLogonMessage("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client2 = FixClientQuotes("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client2.logon()
    client2.get_quote("EURUSD_MDReqID", "EURUSD.x")

    # Aguardar alguns segundos para garantir que o logon seja bem-sucedido antes de enviar a ordem
    time.sleep(5)
    quotes = client2.listen_for_quotes()
    time.sleep(1)
    bid, ask = quotes
    print(f"Bid: {bid}, Ask: {ask}")
    # Enviar uma ordem de compra a mercado
    point = 0.00001
    SL = 0.00010
    TP = 0.00040
    new_order_msg, original_clordid = CreateOrderSingle.create_new_order_single_msg(
        self=logon_msg,
        symbol="EURUSD.x",
        side="1",
        order_qty="1000000",
        ord_type="1",
        price=ask + point
    )
    time.sleep(1)
    SendMessage(new_order_msg)
    price_used = ask + point
    cancel_msg = CreateOrderCancel.create_order_cancel_msg(
        clordid="unique_id_12343",
        account="100019",
        orig_clordid=1690376701735,
        side="1"
    )
    time.sleep(1)
    SendMessage(cancel_msg)
    ReceiveMessage("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    time.sleep(5)
    new_order_msg = CreateOrderSingleOpposite.create_new_order_single_msg_opposite(
        symbol="EURUSD.x",
        side="2",
        order_qty="1000000",
        ord_type="2",
        price=price_used + TP
    )
    time.sleep(1)
    SendMessage(new_order_msg)
    # Espere 30 segundos antes de enviar a requisição de alteração de ordem
    time.sleep(30)
    status_request_msg = CreateOrderStatus.create_order_status_request_msg(
        clordid=1690376701735,
        account="100019",
        order_id="order_id_67898"  # This is optional
    )
    SendMessage(status_request_msg)
    time.sleep(1)

    ReceiveMessage("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
else:
    print("Invalid option. Please enter 1 or 2.")