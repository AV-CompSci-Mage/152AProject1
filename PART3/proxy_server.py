import socket, selectors, types, json

# block list of IPs
BLOCKED = ["127.0.0.1","1.1.1.1", "8.8.8.8", "208.67.222.222"]

CLIENT_HOST = '127.0.0.1'
CLIENT_PORT = 5500

selector = selectors.DefaultSelector()

def accept_connection(sock: socket.socket):
    # accept connection from server_socket
    conn, (addr, port) = sock.accept()

    # data -> any data associated with this socket, can contain anything
    ## addr -> client IP, port -> client port
    ## recv -> array for data received, send -> array for data to send
    data = types.SimpleNamespace(addr=addr, port=port, recv=[], send=[])

    # specify events to listen for
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    # register client socket with selector with events and data
    selector.register(conn, events, data)

# method for handling client communication
def handle_message(key, mask):
    # extract socket and data from key
    sock = key.fileobj
    data = key.data

    # bitwise AND to check if READ event
    if mask & selectors.EVENT_READ:

        # receive data from client
        recv_data = sock.recv(1024)

        # client sent some data, save response
        if recv_data == b"ping":
            # print out data received
            print(f"Received {recv_data.decode()} from {data.addr}:{data.port}")

            # save data to recv array inside selector.data
            data.recv.append(recv_data)
            # uncomment the line below to simulate long-response time from server
            # and how it stalls other clients
            # sleep(10)

            # append response to selector send object, response will be sent later in WRITE event
            data.send.append(b"pong")
        elif not recv_data:
            selector.unregister(sock)
            sock.close()
        
    # bitwise AND to check if WRITE event
    elif mask & selectors.EVENT_WRITE:
        # check if some response is pending
        if len(data.send) > 0:
            # send out the first response in selector send object and remove it
            sock.sendall(data.send.pop(0))

# create a new TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # bind this socket to OS
    server_socket.bind((CLIENT_HOST, CLIENT_PORT))

    # set listening mode on for this socket
    server_socket.listen()

    # set socket to non-blocking mode so it doesn't stall
    server_socket.setblocking(False)

    # register server_socket inside selector
    # here data=None is important for identifying socket later
    selector.register(server_socket, selectors.EVENT_READ, data=None)

    # run indefinitely
    while True:

        # get pending events
        events = selector.select(timeout=None)

        # iterate over events
        for key, mask in events:
            # check if server socket (data is None)
            if key.data is None:
                # accept a new connection
                accept_connection(key.fileobj)
            # client socket event
            else:
                # handle client
                handle_message(key, mask)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ctp_socket:
#     # bind this socket to OS
#     ctp_socket.bind((CLIENT_HOST, CLIENT_PORT))

#     # set listening mode on for this socket
#     ctp_socket.listen()

#     # wait for and accept a new connection
#     # client_socket -> socket to communicate with client
#     # client_addr -> client's IP address, client_port -> client's port number
#     client_socket, (client_addr, client_port) = ctp_socket.accept()

#     # receive data just once from client
#     data = client_socket.recv(1024)
#     data_decoded = data.decode()
#     print(data_decoded)

#     client_message = json.loads(data_decoded)

#     SERVER_HOST = client_message["server_ip"]
#     SERVER_PORT = client_message["server_port"]
#     message_2_server = client_message["message"]
        
#     # if server IP is in blocked list
#     if SERVER_HOST in BLOCKED:
#         print("Error: Server IP is blocked!")
#         client_socket.sendall(b"Error!")
#         client_socket.close()

#         # respond to client
#     elif message_2_server == "ping":
#         print(f"Received {message_2_server} from {client_addr}:{client_port}")
        


#proxy->server = pts
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pts_socket:
#     # connect to the server
#     pts_socket.connect((SERVER_HOST, SERVER_PORT))

#     # send a single ping message
#     # `b` before string converts string to bytes (alternatively, use "ping".encode())
#     pts_socket.sendall(b"ping")

#     # receive response from server
#     data = pts_socket.recv(1024)

#     # print server response
#     message_2_client = data.decode()
#     pts_socket.close()
#     #print(f"Received {data.decode()!r} from {SERVER_HOST}:{SERVER_PORT}")