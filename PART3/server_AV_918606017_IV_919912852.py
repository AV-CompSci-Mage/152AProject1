import socket

# HOW TO RUN THESE FILES: 
# 1. SPLIT INTO THREE TERMINALS
# 2. Run proxy file  in one terminal
# 3. Run server file in another
# 4. Lastly, run the client file on the last terminal

# Note: hard codes in the block list, and json message that the client server sends to the
# proxy server.

#  most of the code in this file is from the demo code the TA presented us:
#  source: https://github.com/klvijeth/ecs152a-fall-2024/blob/main/week3/code/tcp-server-v2.py

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 7000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen()

    while True:

        proxy_socket, (proxy_addr, proxy_port) = server_socket.accept()

        # receive data just once from proxy
        data = proxy_socket.recv(1024)

        # respond to proxy
        if data == b"ping":
            print(f"Received {data.decode()} from {proxy_addr}:{proxy_port}")
            proxy_socket.sendall(b"pong")
            exit(0)
        else:
            print(f"Unknown message received from {proxy_addr}:{proxy_port}")
            exit(1)