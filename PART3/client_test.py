import socket

# specify server host and port to connect to
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5500

message = '{"server_ip": "127.0.0.1", "server_port": 7000, "message": "ping"}'

# create a new TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # connect to the server
    s.connect((PROXY_HOST, PROXY_PORT))

    # send a single ping message
    # `b` before string converts string to bytes (alternatively, use "ping".encode())
    s.sendall(message.encode())
    while True:
        # receive response from proxy server
        data = s.recv(1024)

        # print server response
        if data == b"Error!":
            print(f"Received {data.decode()!r} from {PROXY_HOST}:{PROXY_PORT}")
            break
        elif data == b"pong":
            print(f"Received {data.decode()!r} from {PROXY_HOST}:{PROXY_PORT}")
            print("Successfully finished Part 3! :)")
            exit(0)

