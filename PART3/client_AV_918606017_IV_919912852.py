import socket

# HOW TO RUN THESE FILES: 
# 1. SPLIT INTO THREE TERMINALS
# 2. Run proxy file  in one terminal
# 3. Run server file in another
# 4. Lastly, run the client file on the last terminal

# Note: hard codes in the block list, and json message that the client server sends to the
# proxy server.


# most of the code used here is from the TA's demo code:
# source: https://github.com/klvijeth/ecs152a-fall-2024/blob/main/week3/code/tcp-client-v1.py

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5500

message = '{"server_ip": "127.0.0.1", "server_port": 7000, "message": "ping"}'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # connect to the server
    s.connect((PROXY_HOST, PROXY_PORT))

    s.sendall(message.encode())
    while True:
        data = s.recv(1024)
        if data == b"Error!":
            print(f"Received {data.decode()!r} from {PROXY_HOST}:{PROXY_PORT}")
            break
        elif data == b"pong":
            print(f"Received {data.decode()!r} from {PROXY_HOST}:{PROXY_PORT}")
            print("Successfully finished Part 3! :)")
            exit(0)

