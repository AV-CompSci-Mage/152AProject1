import socket
import time

# specify host and port to receive messages on
HOST = '127.0.0.1'
PORT = 5500
BUFFER_SIZE = 8192  # size of each chunk to send
TOTAL_DATA_SIZE = 100 * 1024 * 1024

# open a new datagram socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:

    # bind this socket to OS
    server_socket.bind((HOST, PORT))
    print(f"Server is set up on {HOST}:{PORT}")

    total_data_received = 0
    start_time = time.time()

    # receive messages until we get to 100 MB
    while total_data_received < TOTAL_DATA_SIZE:
            
        # data -> message, addr -> (client_addr, client_port)
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        total_data_received += len(data)
        
    end_time = time.time()
    elapsed_time = end_time - start_time  

    throughput_kbps = (total_data_received / 1024) / elapsed_time

    # send the throughput back to the client
    server_socket.sendto(str(throughput_kbps).encode(), client_address)
        
    print(f"Throughput sent to client: {throughput_kbps:.2f}KBps")
    print(f"Time taken: {elapsed_time:.2f} seconds") 

