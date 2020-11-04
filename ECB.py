from Crypto.Cipher import AES
from helpers import delete_empty_bytes,message_split_to_blocks,put_empty_bytes

class ECB:
    def __init__(self,encode_key):
        self.encode_key = encode_key.encode('utf-8')
        self.aes_tool = AES.new(self.encode_key, AES.MODE_ECB)

    def encrypt(self,message):
        blocks = message_split_to_blocks(put_empty_bytes(message.encode()))
        return b''.join([self.aes_tool.encrypt(block) for block in blocks])

    def decrypt(self,encrypted_message):
        blocks = message_split_to_blocks(encrypted_message)
        return delete_empty_bytes(b''.join([self.aes_tool.decrypt(block) for block in blocks]))

