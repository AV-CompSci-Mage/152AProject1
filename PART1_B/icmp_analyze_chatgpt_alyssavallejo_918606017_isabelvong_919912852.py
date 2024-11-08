import dpkt
import socket
from scapy.all import IP, ICMP

def parse_icmp(pcap_file):
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for timestamp, buf in pcap:
            # Try to parse the packet as an IP packet using dpkt
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                
                # Check if the IP packet contains ICMP data
                if isinstance(ip.data, dpkt.icmp.ICMP):
                    icmp = ip.data
                    
                    # Extract the ICMP type, code, and checksum
                    icmp_type = icmp.type
                    icmp_code = icmp.code
                    icmp_checksum = icmp.sum
                    payload = icmp.data
                    print(f"Timestamp: {timestamp}")
                    print(f"ICMP Type: {icmp_type}, Code: {icmp_code}, Checksum: {icmp_checksum}")
                    print(f"Payload: {payload}")
                    
                    # Extract source and destination IP addresses
                    src_ip = socket.inet_ntoa(ip.src)
                    dst_ip = socket.inet_ntoa(ip.dst)
                    print(f"Source IP: {src_ip}, Destination IP: {dst_ip}")
                    print("-" * 40)

def parse_icmp_scapy(pcap_file):
    packets = rdpcap(pcap_file)
    for packet in packets:
        if packet.haslayer(ICMP):
            icmp_layer = packet.getlayer(ICMP)
            ip_layer = packet.getlayer(IP)
            
            # Extract and print details
            print(f"Timestamp: {packet.time}")
            print(f"ICMP Type: {icmp_layer.type}, Code: {icmp_layer.code}")
            print(f"Source IP: {ip_layer.src}, Destination IP: {ip_layer.dst}")
            print(f"Payload: {bytes(icmp_layer.payload)}")
            print("-" * 40)

# Example usage
pcap_file = 'path_to_your_pcap_file.pcap'
print("Analyzing ICMP packets using dpkt:")
parse_icmp(pcap_file)
print("\nAnalyzing ICMP packets using Scapy:")
parse_icmp_scapy(pcap_file)
