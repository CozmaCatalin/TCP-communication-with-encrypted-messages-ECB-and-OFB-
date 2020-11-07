from interfaces.node import Node
from encryptions.ECB import ECB
from encryptions.OFB import OFB
import threading

k3 = "3333333333333333"
b = Node("B")
receive_number = 0
key_received = None
encryption_mode = None
encryption_class = None
decrypted_message = ""

def receive_counter(data):
    global receive_number
    receive_number+=1
    if not receive_number > 2:
        print(f'[RECEIVE->{receive_number}]{data}')

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
    global receive_number,encryption_mode,key_received
    if receive_number == 2:
        if encryption_mode == b'ECB':
            crypto = ECB(k3)
            key_received = crypto.decrypt(data).decode()
            print(f'Decrypted K1 with k3 {key_received} ECB mode from -> {str(data)}')
        else:
            crypto = OFB(k3,b'0'*16)
            key_received = crypto.decrypt(data).decode()
            print(f'Decrypted K2 with k3 {key_received} OFB mode from -> {str(data)}')
        b.socket.sendall(b'START')

def set_decrypt_class():
    global encryption_mode,encryption_class,key_received
    if encryption_mode == b'ECB':
        print("\n=============Setting decrypt class ECB and start decrypting the blocks with key " + key_received + "=============")
        encryption_class = ECB(key_received)
    else:
        print("\n=============Setting decrypt class ECB and start decrypting the blocks with key " + key_received + "=============")
        encryption_class = OFB(key_received,b'0'*16)

def decrypt_message(data):
    global encryption_mode,key_received,encryption_class,decrypted_message
    if receive_number == 3:
        set_decrypt_class()
    if receive_number > 2:
        if data != b'STOP':
            if encryption_mode == b'ECB':
                decrypt_block = encryption_class.decrypt(data).decode()
                decrypted_message += decrypt_block
                print(f'[ECB Block->{receive_number-2}]{str(data)} -> {str(decrypt_block)}')
            else:
                decrypt_block = encryption_class.decrypt(data).decode()
                decrypted_message += decrypt_block
                print(f'[OFB Block->{receive_number-2}]{str(data)} -> {str(decrypt_block)}')
        else:
            print('\n')
            print("============= Decryption DONE ! =============")
            print(decrypted_message)

def receive():
    while b.signal:
        try:
            data = b.socket.recv(1024)
            receive_counter(data)
            encryption_mode_receive(data)
            decrypt_key_wanted(data)
            decrypt_message(data)
        except Exception as e:
            print("You have been disconnected from the server " + str(e))
            b.signal = False

receive_thread = threading.Thread(target=receive)
receive_thread.start()