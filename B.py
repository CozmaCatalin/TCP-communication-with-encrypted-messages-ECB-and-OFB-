from node import Node
from ECB import ECB
from OFB import OFB
import threading

k3 = "3333333333333333"
b = Node("B")
receive_number = 0
encryption_mode = None
def receive_counter(data):
    global receive_number
    receive_number+=1
    print(f'[receive->{receive_number}]{data}')

def encryption_mode_receive(message):
    global receive_number,encryption_mode
    if receive_number == 1:
        encryption_mode = message
        if message == b'ECB':
            key = b'K1'
            b.socket.sendall(key)
        if message == b'OFB':
            key = b'K2'
            b.socket.sendall(key)

def decrypt_key_wanted(data):
    global receive_number,encryption_mode
    if receive_number == 2:
        if encryption_mode == b'ECB':
            crypto = ECB(k3)
            print(f'Decrypted K1 with k3 {crypto.decrypt(data)} ECB mode from -> {str(data)}')
        else:
            crypto = OFB(k3,b'0'*16)
            print(f'Decrypted K2 with k3 {crypto.decrypt(data)} OFB mode from -> {str(data)}')
        b.socket.sendall(b'START')

def receive():
    while b.signal:
        try:
            data = b.socket.recv(1024)
            receive_counter(data)
            encryption_mode_receive(data)
            decrypt_key_wanted(data)
        except Exception as e:
            print("You have been disconnected from the serve " + str(e))
            b.signal = False

receive_thread = threading.Thread(target=receive)
receive_thread.start()