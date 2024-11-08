import dpkt
import sys

def parse_pcap(pcap_file):

    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    # iterate over packets
    for timestamp, data in pcap:

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
            continue
        
        ip = eth.data

        # do not proceed if there is no transport layer data
        if not isinstance(ip.data, dpkt.tcp.TCP):
            continue

        # extract transport layer data
        tcp = ip.data

        # do not proceed if there is no application layer data
        # here we check length because we don't know protocol yet
        if not len(tcp.data) > 0:
            continue

        # extract application layer data
        # dest port = 80 -> http request 
        if tcp.dport == 80:
            try:
                http = dpkt.http.Request(tcp.data)
                for header, value in http.headers.items():
                    print(f"{header.capitalize()}: {value}")
                print(tcp.data)
                print("\n")
            except:
                pass
                
        # source port = 80 -> http response 
        elif tcp.sport == 80:
            try:
                http = dpkt.http.Response(tcp.data)
                for header, value in http.headers.items():
                    print(f"{header.capitalize()}: {value}")
                print(tcp.data)
                print("\n")
            except:
                pass

# run 
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_pcap(sys.argv[1])
