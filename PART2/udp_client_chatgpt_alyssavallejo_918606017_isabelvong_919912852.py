import socket

# Define client parameters
SERVER_ADDRESS = ('localhost', 12345)
BUFFER_SIZE = 4096  # 4 KB per packet
TOTAL_DATA_SIZE = 100 * 1024 * 1024  # 100 MB

def udp_client():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Send 100 MB of data to the server
        data_chunk = b'x' * BUFFER_SIZE  # 4 KB chunk
        total_data_sent = 0
        
        while total_data_sent < TOTAL_DATA_SIZE:
            client_socket.sendto(data_chunk, SERVER_ADDRESS)
            total_data_sent += len(data_chunk)
        
        # Send an "END" message to indicate end of transmission
        client_socket.sendto(b"END", SERVER_ADDRESS)

        # Receive the throughput from the server
        throughput_data, _ = client_socket.recvfrom(BUFFER_SIZE)
        throughput_kbps = float(throughput_data.decode())
        print(f"Throughput: {throughput_kbps:.2f} KB/s")

if __name__ == "__main__":
    udp_client()
