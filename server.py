import socket
import threading
import time

nodes = []
total_nodes = 0


def send_msg(message, node_type):
    global nodes
    for node in nodes:
        if node.node_type == node_type:
            node.socket_node.send(message)

def a_handler(message, request_number):
    print(f'[A->{request_number}]{message}')
    if request_number == 1:
        send_msg(message, b'B')
        if message == b'ECB':
            send_msg(b'K1', b'KM')
        else:
            send_msg(b'K2', b'KM')
    if request_number > 1:
        send_msg(message,b'B')


def b_handler(message,request_number):
    print(f'[B->{request_number}]{message}')
    if request_number == 1:
        send_msg(message,b'KM')
    if request_number == 2:
        send_msg(b'B-SEND-START',b'A')
    pass


def km_handler(message,request_number):
    print(f'[KM->{request_number}]{message}')
    if request_number == 1:
        send_msg(message, b'A')
        send_msg(message, b'B')
    pass


class Node(threading.Thread):
    def __init__(self, socket_node, address_node, id_node, is_running):
        threading.Thread.__init__(self)
        self.node_type = ""
        self.socket_node = socket_node
        self.address_node = address_node
        self.id_node = id_node
        self.is_running = is_running
        self.number_of_request = -1

    def __str__(self):
        return str(self.id_node) + " " + str(self.address_node)

    def run(self):
        while self.is_running:
            try:
                data = self.socket_node.recv(1024)
                self.number_of_request += 1
                if self.number_of_request == 0:
                    print(f'Node {data} connected!')
                    self.node_type = data
                else:
                    if self.node_type == b'A':
                        a_handler(data,self.number_of_request)
                    if self.node_type == b'B':
                        b_handler(data,self.number_of_request)
                    if self.node_type == b'KM':
                        km_handler(data,self.number_of_request)

            except Exception as e:
                print(f'Node {str(self.node_type)} has disconnected {e}')
                self.is_running = False
                nodes.remove(self)
                break



def start_server():
    host = "127.0.0.1"
    port = 12345
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    socket_server.listen(3)

    while True:
        sock, address = socket_server.accept()
        global total_nodes
        nodes.append(Node(sock, address, total_nodes,True))
        nodes[len(nodes) - 1].start()
        total_nodes += 1

start_server()