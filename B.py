from node import Node
from ECB import ECB
import threading

k3 = "3333333333333333"
b = Node("B")
receive_number = 0

def receive_counter(data):
    global receive_number
    receive_number+=1
    print(f'[receive->{receive_number}]{data}')

def encryption_mode_receive(message):
    if message == b'ECB':
        key = b'K1'
        b.socket.sendall(key)
        return
    if message == b'OFB':
        key = b'K2'
        b.socket.sendall(key)
        return

def decrypt_key_wanted(data):
    global receive_number
    if receive_number == 2:
        crypto = ECB(k3)
        b.socket.sendall(b'START')
        print(f'Decrypted key with k3 {crypto.decrypt(data)}')

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