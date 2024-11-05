import dpkt
import datetime
import socket
from dpkt.compat import compat_ord


pcap_path="PART1APCAP/example.pcap"
f = open(pcap_path, 'rb')
print("Now reading pcap file: ", pcap_path)
pcap = dpkt.pcap.Reader(f)
http_reqcount = 0
http_rescount = 0
for timestamp, data in pcap:
    ts=datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
    #print(ts, len(data))
    eth = dpkt.ethernet.Ethernet(data)
    # # do not proceed if there is no network layer data
    if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
        continue
    # # extract network layer data
    ip = eth.data
    
    try:
        ip_src = socket.inet_ntop(socket.AF_INET, ip.src)
        ip_dst = socket.inet_ntop(socket.AF_INET, ip.dst)
        #print("Timestamp: ",ts, " IP dst: ", ip_dst)
    except ValueError:
        pass
    

    # # do not proceed if there is no transport layer data
    if not isinstance(ip.data, dpkt.tcp.TCP):
        continue

    # # extract transport layer data
    tcp = ip.data

    # # do not proceed if there is no application layer data
    # # here we check length because we don't know protocol yet

    if not len(tcp.data) > 0:
        continue

    # # extract application layer data
    # ## if destination port is 80, it is a http request
    if tcp.dport == 80:
        try:
            http = dpkt.http.Request(tcp.data)
            http_reqcount += 1
            #print("Timestamp: ",ts, " IP dst: ", ip_dst)
            #print(http.headers)
            print(http.headers['user-agent'])
        except:
            pass
            
    ## if source port is 80, it is a http response
    elif tcp.sport == 80:
        try:
            http = dpkt.http.Response(tcp.data)
            http_rescount += 1
            #print("Timestamp: ",ts, " IP src: ", ip_src)
            #print(http.headers)
            print(http.headers['user-agent'])
        except:
            pass
#print("http_rescount: ", http_rescount)
#print("http_reqcount: ", http_reqcount)
