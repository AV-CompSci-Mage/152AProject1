import socket

# specify host and port to listen on
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5500


# create a new TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # bind this socket to OS
    server_socket.bind((PROXY_HOST, PROXY_PORT))

    # set listening mode on for this socket
    server_socket.listen()

    # run indefinitely
    while True:
        # wait for and accept a new connection
        # client_socket -> socket to communicate with client
        # client_addr -> client's IP address, client_port -> client's port number
        proxy_socket, (proxy_addr, proxy_port) = server_socket.accept()

        # receive data just once from client
        data = proxy_socket.recv(1024)

        # respond to client
        if data == b"ping":
            print(f"Received {data.decode()} from {proxy_addr}:{proxy_port}")
            proxy_socket.sendall(b"pong")
        else:
            print(f"Unknown message received from {proxy_addr}:{proxy_port}")
            exit(1)