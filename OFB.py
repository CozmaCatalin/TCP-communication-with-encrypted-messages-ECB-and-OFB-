from Crypto.Cipher import AES
from helpers import delete_empty_bytes,message_split_to_blocks,put_empty_bytes
import copy

class OFB:
    def __init__(self,encode_key,iv):
        self.encode_key = encode_key.encode('utf-8')
        self.aes_tool = AES.new(self.encode_key, AES.MODE_ECB)
        self.iv = iv

    def encrypt(self,message):
        blocks = message_split_to_blocks(put_empty_bytes(message.encode()))
        encrypted_blocks = []
        for block in blocks:
            self.iv = self.aes_tool.encrypt(self.iv)
            iv_byte_array = bytearray(copy.copy(self.iv))
            for i in range(16):
                iv_byte_array[i] = iv_byte_array[i]^block[i]
            encrypted_blocks.append(bytes(iv_byte_array))
        self.iv = b'0'*16
        return encrypted_blocks

    def decrypt(self,block):
        self.iv = self.aes_tool.encrypt(self.iv)
        iv_byte_array = bytearray(copy.copy(self.iv))
        for i in range(16):
            iv_byte_array[i] = iv_byte_array[i]^block[i]
        return delete_empty_bytes(bytes(iv_byte_array))
