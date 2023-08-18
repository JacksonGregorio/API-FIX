import socket
from datetime import datetime
import simplefix

class CreateOrderCancel:


    def create_order_cancel_msg(self, clordid, account, orig_clordid, side, transact_time=None):
        message = simplefix.FixMessage()

        # Append Body tags
        message.append_pair(35, "F")  # MsgType for Order Cancel Request
        message.append_pair(49, self.sender_comp_id)  # SenderCompID
        message.append_pair(56, self.target_comp_id)  # TargetCompID
        message.append_pair(34, self.msg_seq_num)  # MsgSeqNum
        message.append_pair(52, datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # SendingTime

        message.append_pair(11, clordid)  # ClOrdID
        message.append_pair(1, account)  # Account
        message.append_pair(41, orig_clordid)  # OrigClOrdID
        message.append_pair(54, side)  # Side (1 - Buy, 2 - Sell)
        message.append_pair(60, transact_time or datetime.utcnow().strftime("%Y%m%d-%H:%M:%S"))  # TransactTime

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