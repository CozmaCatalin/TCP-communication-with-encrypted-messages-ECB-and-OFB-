from Crypto.Cipher import AES

class ECB:
    def __init__(self,encode_key):
        self.encode_key = encode_key.encode('utf-8')
        self.tool = AES.new(self.encode_key, AES.MODE_ECB)

    def encrypt(self,message):
        message = message.encode('utf-8')
        return self.tool.encrypt(message)

    def decrypt(self,message):
        return self.tool.decrypt(message).decode()
