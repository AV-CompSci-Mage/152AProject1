import dpkt
import sys
import datetime
from dpkt.utils import inet_to_str


def parse_icmp(pcap_file):

    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    # iterate over packets
    for timestamp, data in pcap:

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip.IP):
            continue

        ip = eth.data

        # do not proceed if there is no ICMP data
        if not isinstance(ip.data, dpkt.icmp.ICMP):
            continue

        # extract ICMP data
        icmp = ip.data

        # if no data, don't continue
        if not len(ip.data) > 0:
            continue


        print("\n")
        print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
        print("IP:", inet_to_str(ip.src), "->", inet_to_str(ip.dst))
        print(f"Type: {icmp.type}")
        print(f"Code: {icmp.code}")
        print(f"Checksum: {icmp.sum}")
        print("Data:", repr(icmp.data)) 


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_icmp(sys.argv[1])
