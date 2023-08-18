import socket
from datetime import datetime
import simplefix
import time

class CreateOrderSingleOpposite:


    def create_new_order_single_msg_opposite(self, symbol, side, order_qty, ord_type, price=None):
        message = simplefix.FixMessage()

        # Append Body tags
        message.append_pair(35, "D")  # MsgType for New Order - Single
        message.append_pair(49, self.sender_comp_id)  # SenderCompID
        message.append_pair(56, self.target_comp_id)  # TargetCompID
        message.append_pair(34, self.msg_seq_num)  # MsgSeqNum
        message.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # SendingTime

        # Generate a unique ClOrdID based on the current timestamp
        unique_clordid = str(int(time.time() * 1000))
        message.append_pair(11, unique_clordid)  # ClOrdID (Client Order ID)

        message.append_pair(1, self.username)  # Account
        message.append_pair(55, symbol)  # Symbol
        message.append_pair(54, side)  # Side (1 - Buy, 2 - Sell)
        message.append_pair(38, order_qty)  # OrderQty
        message.append_pair(40, ord_type)  # OrdType (1 - Market, 2 - Limit)
        message.append_pair(59, "1")  # TimeInForce
        message.append_pair(44, price)  # Price
        message.append_pair(60, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))

        # Include price if ord_type is Limit
        #if ord_type == "2" and price is not None:


        # Encode the body part
        encoded_body = b''.join([f"{tag}={value}\x01".encode() for tag, value in message.pairs])

        # Calculate BodyLength (tag 9)
        body_length = len(encoded_body)

        # Build the final message
        final_message = simplefix.FixMessage()
        final_message.append_pair(8, "FIX.4.4")  # BeginString
        final_message.append_pair(9, str(body_length))  # BodyLength
        # Append the body
        for tag, value in message.pairs:
            final_message.append_pair(tag, value)

        # Calculate the checksum manually
        encoded_msg_without_checksum = final_message.encode()[:-7]
        checksum = self.calculate_checksum(encoded_msg_without_checksum)
        final_message.append_pair(10, checksum)  # CheckSum

        return final_message.encode()