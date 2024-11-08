import dpkt
import socket

def analyze_icmp(pcap_file):
    # Open the pcap file
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        # Loop over each packet in the pcap file
        for timestamp, buf in pcap:
            # Unpack the Ethernet frame
            eth = dpkt.ethernet.Ethernet(buf)
            
            # Ensure the packet is an IP packet (skip ARP, etc)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data

                # Check if the IP packet is ICMP
                if isinstance(ip.data, dpkt.icmp.ICMP):
                    icmp = ip.data
                    
                    # Extract source and destination IPs
                    src_ip = socket.inet_ntoa(ip.src)
                    dst_ip = socket.inet_ntoa(ip.dst)
                    
                    # ICMP type and code
                    icmp_type = icmp.type
                    icmp_code = icmp.code

                    # Display ICMP packet information
                    print(f"Timestamp: {timestamp}")
                    print(f"Source IP: {src_ip}, Destination IP: {dst_ip}")
                    print(f"ICMP Type: {icmp_type}, Code: {icmp_code}")
                    
                    # Parse Echo request and reply (type 8 and 0)
                    if icmp_type == 8:
                        print("ICMP Echo Request")
                    elif icmp_type == 0:
                        print("ICMP Echo Reply")
                    print("="*40)

# Call the function with your ICMP pcap file path
analyze_icmp("ass1_3.pcap")
