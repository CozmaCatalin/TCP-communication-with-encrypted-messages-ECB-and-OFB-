from node import Node
from ECB import ECB
import threading

k3 = "3333333333333333"
a = Node("A")
receive_number = 0

def receive_counter(data):
    global receive_number
    receive_number+=1
    print(f'[receive->{receive_number}]{data}')

def decrypt_key_wanted(data):
    global receive_number
    if receive_number == 1:
        crypto = ECB(k3)
        print(f'Decrypted key with k3 {crypto.decrypt(data)}')

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

encrypt_mode = input("Enter encrypt mode: ")
a.socket.sendall(encrypt_mode.encode())
