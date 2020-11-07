from interfaces.node import Node
from encryptions.ECB import ECB
from encryptions.OFB import OFB

import time
import threading
sleep_time = 0.01
k3 = "3333333333333333"
a = Node("A")
receive_number = 0
encryption_mode = None
key_received = None
def receive_counter(data):
    global receive_number
    receive_number+=1
    print(f'[RECEIVE->{receive_number}]{data}')

def decrypt_key_wanted(data):
    global receive_number,key_received,encryption_mode
    if receive_number == 1:
        if encryption_mode == "ECB":
            crypto = ECB(k3)
            key_received = crypto.decrypt(data).decode()
            print(f'Decrypted K1 with K3 {key_received} ECB mode from -> {str(data)}')
        else:
            crypto = OFB(k3,b'0'*16)
            key_received = crypto.decrypt(data).decode()
            print(f'Decrypted K2 with K3 {key_received} OFB mode from -> {str(data)}')

def start_crypting_file_text_message(data):
    global encryption_mode,key_received
    if receive_number == 2:
        while 1:
            try:
                file = input("Please enter the file from tests that you want to send : ")
                f = open(f'tests/{file}.txt', 'r')
                break
            except Exception as e:
                print(e)
        i = 0
        if encryption_mode == "ECB":
            print('\n===Sending to server the blocks encrypted with EBC and key-> ' + str(key_received) + "===")
            e = ECB(key_received)
            encrypted_blocks = e.encrypt(f.read())
            for block in encrypted_blocks:
                i+=1
                time.sleep(sleep_time)
                print(f'[ECB Block->{i}] {str(block)}')
                a.socket.sendall(block)
        else:
            print('\n===Sending to server the blocks encrypted with OFB and key-> ' + str(key_received) + "===")
            e = OFB(key_received,b'0'*16)
            encrypted_blocks = e.encrypt(f.read())
            for block in encrypted_blocks:
                i+=1
                time.sleep(sleep_time)
                print(f'[OFB Block->{i}] {str(block)}')
                a.socket.sendall(block)
        a.socket.sendall(b'STOP')

def receive():
    while a.signal:
        try:
            data = a.socket.recv(1024)
            receive_counter(data)
            decrypt_key_wanted(data)
            start_crypting_file_text_message(data)
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

