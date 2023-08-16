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
from Create_new_order_single_msg import CreateOrderSingle;
from Create_new_order_single_msg_opposie import CreateOrderSingleOpposite;
from Create_new_order_single_msg import CreateOrderSingle;
from Create_order_status_request_msg import CreateOrderStatus;

if __name__ == '__main__':
    stunnel_connector = ConnectToStunnel("127.0.0.1", 8080)
    checksum_calculator = CalculateCheck()
    logon_message_creator = CreateLogonMessage("TD019", "DCRD", "100019", "87MTgLw23wfe!")

    client2 = FixClientQuotes("fixapidcrd.squaredfinancial.com", 10210, "MD019", "DCRD", "100019", "87MTgLw345dfb!")
    client2.logon()
    client2.get_quote("EURUSD_MDReqID", "EURUSD.x")

    logon_msg = logon_message_creator.create()
    SendMessage(logon_msg)
    print(logon_msg)
