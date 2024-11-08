import dpkt
import re

def extract_secrets_from_pcap(file_path):
    secrets = []

    # Define a regex pattern to identify obvious secrets
    # This pattern can be adjusted based on known secret formats or keywords
    secret_patterns = [
        re.compile(rb'password\s*[:=]\s*\S+', re.IGNORECASE),
        re.compile(rb'token\s*[:=]\s*\S+', re.IGNORECASE),
        re.compile(rb'secret\s*[:=]\s*\S+', re.IGNORECASE),
        re.compile(rb'key\s*[:=]\s*\S+', re.IGNORECASE),
        re.compile(rb'API_KEY\s*[:=]\s*\S+', re.IGNORECASE),
        # Add other patterns if necessary
    ]

    # Open the pcap file
    with open(file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        # Process each packet in the pcap file
        for timestamp, buf in pcap:
            try:
                # Parse the Ethernet layer
                eth = dpkt.ethernet.Ethernet(buf)
                
                # Check if the packet is an IP packet (IPv4 or IPv6)
                if isinstance(eth.data, dpkt.ip.IP):
                    ip = eth.data
                    
                    # Check if it's a TCP packet
                    if isinstance(ip.data, dpkt.tcp.TCP):
                        tcp = ip.data
                        
                        # Look at the TCP data for potential secrets
                        payload = tcp.data

                        # Search for secrets using the defined patterns
                        for pattern in secret_patterns:
                            matches = pattern.findall(payload)
                            for match in matches:
                                secrets.append(match.decode(errors='ignore').strip())

            except Exception as e:
                # Catch any parsing errors and continue
                print(f"Error processing packet: {e}")
    
    # Output all found secrets, each on a new line
    for secret in secrets:
        print(secret)

# Run the function with the given pcap file path
extract_secrets_from_pcap("ass1_1.pcap")
