import socket
import time

# Define server parameters
SERVER_ADDRESS = ('localhost', 12345)
BUFFER_SIZE = 4096  # 4 KB per packet

def udp_server():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Bind the socket to the address
        server_socket.bind(SERVER_ADDRESS)
        print("Server listening on", SERVER_ADDRESS)

        # Receive data from the client
        total_data_received = 0
        start_time = time.time()
        
        while True:
            data, client_address = server_socket.recvfrom(BUFFER_SIZE)
            total_data_received += len(data)
            
            # Check for end-of-transmission signal
            if data == b"END":
                break

        # Calculate throughput
        end_time = time.time()
        duration = end_time - start_time
        throughput_kbps = (total_data_received / 1024) / duration  # KB/s

        # Send the throughput back to the client
        server_socket.sendto(str(throughput_kbps).encode(), client_address)
        print(f"Total data received: {total_data_received / (1024 * 1024)} MB")
        print(f"Duration: {duration} seconds")
        print(f"Throughput: {throughput_kbps} KB/s")

if __name__ == "__main__":
    udp_server()
