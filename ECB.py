from Crypto.Cipher import AES

class ECB:
    def __init__(self,encode_key):
        self.encode_key = encode_key.encode('utf-8')
        self.tool = AES.new(self.encode_key, AES.MODE_ECB)

    @staticmethod
    def put_empty_bytes(message):
        empty_byte_length = 16 - (len(message) % 16)
        if empty_byte_length == 16:
            return message
        else:
            return message + (empty_byte_length * b'\0')

    @staticmethod
    def delete_empty_bytes(message):
        index = 0
        for i in range(0,len(message)):
            if message[i] == 0x00:
                index = i
                break
        return message[0:index]

    @staticmethod
    def message_split_to_blocks(message):
        return [message[i:i+16] for i in range(0,len(message),16)]

    def encrypt(self,message):
        blocks = self.message_split_to_blocks(self.put_empty_bytes(message.encode()))
        return b''.join([self.tool.encrypt(block) for block in blocks])

    def decrypt(self,encrypted_message):
        blocks = self.message_split_to_blocks(encrypted_message)
        return self.delete_empty_bytes(b''.join([self.tool.decrypt(block) for block in blocks])).decode()

k = "salut!, ce faci man ?"
k3 = "3333333333333333"

e = ECB(k3)
encrypted = e.encrypt(k)
print(encrypted)
decrypted = e.decrypt(encrypted)
print(decrypted)
