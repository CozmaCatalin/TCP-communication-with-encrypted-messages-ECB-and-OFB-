import socket
import sys

host = "127.0.0.1"
port = 12345

class Node:
    def __init__(self,node_type):
        self.node_type = node_type
        self.signal = True
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.socket.send(self.node_type.encode())
        except Exception as e:
            print("Could not make a connection to the server " + str(e))
            input("Press any key to quit")
            sys.exit(0)

    def close_node(self):
        close = "CLOSE"
        self.socket.sendall(close.encode())



