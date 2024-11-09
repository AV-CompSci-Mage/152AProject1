import socket, json

# HOW TO RUN THESE FILES: 
# 1. SPLIT INTO THREE TERMINALS
# 2. Run proxy file  in one terminal
# 3. Run server file in another
# 4. Lastly, run the client file on the last terminal

# Note: hard codes in the block list, and json message that the client server sends to the
# proxy server.

#  most of the code in this file is from the demo code the TA presented us:
#  source 1: https://github.com/klvijeth/ecs152a-fall-2024/blob/main/week3/code/tcp-client-v1.py
#  source 2: https://github.com/klvijeth/ecs152a-fall-2024/blob/main/week3/code/tcp-server-v2.py

# block list of IPs
BLOCKED = ["127.0.0.1","1.1.1.1", "8.8.8.8", "208.67.222.222"]

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5500
message_2_client = ""
#ctp -> client to proxy
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ctp_socket:

    ctp_socket.bind((PROXY_HOST, PROXY_PORT))

    ctp_socket.listen()

    client_socket, (client_addr, client_port) = ctp_socket.accept()


    data = client_socket.recv(1024)
    data_decoded = data.decode()
    print(data_decoded)

    client_message = json.loads(data_decoded)

    SERVER_HOST = client_message["server_ip"]
    SERVER_PORT = client_message["server_port"]
    message_2_server = client_message["message"]
        
    # if server IP is in blocked list
    if SERVER_HOST in BLOCKED:
        print("Error: Server IP is blocked!")
        client_socket.sendall(b"Error!")
        client_socket.close()
        exit(1)

        # respond to client
    elif message_2_server == "ping":
        print(f"Received {message_2_server} from {client_addr}:{client_port}")
        #proxy->server = pts
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pts_socket:
            # connect to the server
            pts_socket.connect((SERVER_HOST, SERVER_PORT))

            pts_socket.sendall(b"ping")

            # receive response from server
            data = pts_socket.recv(1024)

            # put server response into message_2_client so it can be sent back to client
            message_2_client = data.decode()
            print(f"Received {data.decode()!r} from {SERVER_HOST}:{SERVER_PORT}")
            pts_socket.close()
        
        client_socket.sendall(message_2_client.encode())
