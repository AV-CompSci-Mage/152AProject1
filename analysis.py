import dpkt
import datetime
import socket

# insert pcap file path here
pcap_path="PART1APCAP/tmz.pcap"
f = open(pcap_path, 'rb')
print("Now reading pcap file: ", pcap_path)
pcap = dpkt.pcap.Reader(f)
http_count = 0
https_count = 0
dns_count = 0
ftp_count = 0
ip_TCP = 0
ip_UDP = 0

for timestamp, data in pcap:
    ts=datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
    eth = dpkt.ethernet.Ethernet(data)
    if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
        continue
    
    ip = eth.data 
    # this part of the code is used by demo code from the dpkt library: 
    # https://dpkt.readthedocs.io/en/latest/_modules/examples/print_packets.html?highlight=socket.inet_ntop
    try:
        ip_dst = socket.inet_ntop(socket.AF_INET, ip.dst)
        print("Timestamp: ",ts, " IP dst: ", ip_dst)
    except ValueError:
        pass

    # checks to see if TCP data is present (HTTP, HTTPS, FTP)
    if isinstance(ip.data, dpkt.tcp.TCP):
        tcp = ip.data
    # # extract transport layer data
        if not len(tcp.data) > 0:
                continue

        if tcp.dport == 80:
            try:
                http = dpkt.http.Request(tcp.data)
                http_count += 1
                #print("HTTP Request user-agent ",http.headers['user-agent'])
            except:
                pass
            
    ## if source port is 80, it is a http response
        elif tcp.sport == 80:
            try:
                http = dpkt.http.Response(tcp.data)
                http_count += 1
                #print("HTTP Response user-agent ",http.headers['user-agent'])
            except:
                pass
            
    # ## if source or destination port is 443, it is a https packet
        elif tcp.dport == 443 or tcp.sport == 443:
            try:
             ## HTTPS packets are encrypted so we cannot extract headers or user-agents
             https_count += 1
            except:
                pass
    # ## if source or destination port is 20, it is a ftp packet
        elif tcp.dport == 21 or tcp.sport == 21:
            try:
             ## HTTPS packets are encrypted so we cannot extract headers or user-agents
                ftp_count += 1
            except:
                pass
# checking for UDP packets (DNS)
    elif isinstance(ip.data, dpkt.udp.UDP):
        udp = ip.data
        if not len(udp.data) > 0:
            continue

        if udp.dport == 53 or udp.sport == 53:
            try:
                dns_count += 1
            except:
                pass
    # if neither TCP nor UDP, ignore

print("Analysis complete. Results:")
print("ftp count: ", ftp_count)
print("dns count: ", dns_count)
print("http count: ", http_count)
print("https count: ", https_count)
