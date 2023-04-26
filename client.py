import socket

server_address = ('localhost', 5000)

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(server_address)
tcp_socket.send(b"Hello World")
data = tcp_socket.recv(32)
print("server response", data)