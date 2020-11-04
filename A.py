from node import Node
from ECB import ECB
from OFB import OFB
import threading

k3 = "3333333333333333"
a = Node("A")
receive_number = 0
encryption_mode = None

def receive_counter(data):
    global receive_number
    receive_number+=1
    print(f'[receive->{receive_number}]{data}')

def decrypt_key_wanted(data):
    global receive_number
    if receive_number == 1:
        if encryption_mode == "ECB":
            crypto = ECB(k3)
            print(f'Decrypted K1 with k3 {crypto.decrypt(data)} ECB mode from -> {str(data)}')
        else:
            crypto = OFB(k3,b'0'*16)
            print(f'Decrypted K1 with k3 {crypto.decrypt(data)} ECB mode from -> {str(data)}')

def receive():
    while a.signal:
        try:
            data = a.socket.recv(1024)
            receive_counter(data)
            decrypt_key_wanted(data)
        except Exception as e:
            print("You have been disconnected from the server " + str(e))
            a.signal = False

receive_thread = threading.Thread(target=receive)
receive_thread.start()

while 1:
    encryption_mode = input("Enter encrypt mode: ")
    if encryption_mode == "OFB" or encryption_mode == "ECB":
        break
    print("Invalid encryption mode!")
a.socket.sendall(encryption_mode.encode())
