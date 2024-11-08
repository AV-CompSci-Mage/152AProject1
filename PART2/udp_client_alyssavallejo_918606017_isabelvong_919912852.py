import socket
import time

# specify server host and port to connect to
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500
BUFFER_SIZE = 8192  # size of each chunk to send
TOTAL_DATA_SIZE = 100 * 1024 * 1024

# open a new datagram socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

    data_chunk = b'a' * BUFFER_SIZE # make up data 
    total_sent = 0
    chunk_count = 0
    
    # send 100 MB of data in chunks
    while total_sent < TOTAL_DATA_SIZE:
        client_socket.sendto(data_chunk, (SERVER_HOST, SERVER_PORT))
        total_sent += BUFFER_SIZE
        chunk_count += 1
            
        # print status for each chunk sent
        print(f"Sent packet {chunk_count}, Total data sent: {total_sent / 1024:.2f} KB")

    # receive throughput from the server
    throughput_data, _ = client_socket.recvfrom(BUFFER_SIZE)
    throughput_kbps = float(throughput_data.decode())
    print(f"Throughput received from server: {throughput_kbps:.2f} KBps")

