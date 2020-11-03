from node import Node
from ECB import ECB
import threading

keys = {
    "K1":"1111111111111111",
    "K2":"2222222222222222",
    "K3":"3333333333333333",
}
key_wanted = None

km = Node("KM")
receive_number = 0

def set_key_wanted(data):
    global key_wanted
    if receive_number == 1:
        key_wanted = data.decode("utf-8")

def receive_counter(data):
    global receive_number
    receive_number+=1
    print(f'[receive->{receive_number}]{data}')

def send_encrypted_key():
    global receive_number,key_wanted
    if receive_number == 2:
        crypto = ECB(keys["K3"])
        km.socket.sendall(crypto.encrypt(keys[key_wanted]))

def receive():
    while km.signal:
        try:
            data = km.socket.recv(1024)
            receive_counter(data)
            set_key_wanted(data)
            send_encrypted_key()
        except Exception as e:
            print("You have been disconnected from the server " + str(e))
            km.signal = False

receive_thread = threading.Thread(target=receive)
receive_thread.start()
