import socket
from datetime import datetime
import simplefix

class CreateOrderStatus:


    def create_order_status_request_msg(self, clordid, account, order_id=None):
        message = simplefix.FixMessage()

        # Append Body tags
        message.append_pair(35, "H")  # MsgType for Order Status Request
        message.append_pair(34, self.msg_seq_num)  # MsgSeqNum
        message.append_pair(49, self.sender_comp_id)  # SenderCompID


        message.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # SendingTime
        message.append_pair(56, self.target_comp_id)  # TargetCompID
        message.append_pair(54, 2)

        if order_id:
            message.append_pair(37, 6424)  # OrderID

        message.append_pair(11, clordid)  # ClOrdID
        message.append_pair(1, account)  # Account

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