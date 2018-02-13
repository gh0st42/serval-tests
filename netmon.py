 #!/usr/bin/python

# Simple network monitor - 1s interval csv stats dumper
# Copyright (c) 2016 Lars Baumgaertner
#
# requires dpkt and pcap python packages
#
# usage: sudo ./netmon.py <networkinterface>

import dpkt, pcap
import signal
import sys
import time
from thread import start_new_thread

def signal_handler(signum, frame):
        print('You pressed Ctrl+C!')
        # No total stats to be compatible to other logfiles
        # print_total_stats()
        sys.stdout.flush()
        sys.exit(0)

def log_handler(signum, frame):
    print("hello")
    # print_cur_stats()
    sys.stdout.flush()

    signal.alarm(1)

def logger():
    while True:
        print_cur_stats()
        sys.stdout.flush()
        time.sleep(1)

def print_header():
    print "timestamp_ms,cnt_pkt,cnt_ip,cnt_tcp,cnt_udp,cnt_iperf_tcp,cnt_iperf_udp,cnt_wget_tcp,cnt_wget_udp,size_pkt,size_ip,size_tcp,size_udp,size_iperf_tcp,size_iperf_udp,size_wget_tcp,size_wget_udp"

def print_total_stats_human():
    print "\n" , "="*40
    print "Packet counts total:"
    print "#Pkts: ", total_cnt['pkt']
    print "#IP: ", total_cnt['ip']
    print "#tcp: ", total_cnt['tcp']
    print "#udp: ", total_cnt['udp']
    print "#iperf_tcp: ", total_cnt['iperf_tcp']
    print "#iperf_udp: ", total_cnt['iperf_udp']
    print "#wget_tcp: ", total_cnt['wget_tcp']
    print "#wget_udp: ", total_cnt['wget_udp']
    print "\nPacket size counts total:"
    print "Pkts: ", total_size['pkt']
    print "IP: ", total_size['ip']
    print "tcp: ", total_size['tcp']
    print "udp: ", total_size['udp']
    print "iperf_tcp: ", total_size['iperf_tcp']
    print "iperf_udp: ", total_size['iperf_udp']
    print "wget_tcp: ", total_size['wget_tcp']
    print "wget_udp: ", total_size['wget_udp']

def print_total_stats():
    csv_line = "TOTAL,"
    csv_line += "%d,%d,%d,%d,%d,%d,%d,%d" % (total_cnt['pkt'],total_cnt['ip'],total_cnt['tcp'],total_cnt['udp'],total_cnt['iperf_tcp'],total_cnt['iperf_udp'],total_cnt['wget_tcp'],total_cnt['wget_udp'])
    csv_line += ",%d,%d,%d,%d,%d,%d,%d,%d" % (total_size['pkt'],total_size['ip'],total_size['tcp'],total_size['udp'],total_size['iperf_tcp'],total_size['iperf_udp'],total_size['wget_tcp'],total_size['wget_udp'])
    print csv_line

def print_cur_stats():
    cur_time = int(time.time() * 1000)
    csv_line = str(cur_time) + ','
    csv_line += "%d,%d,%d,%d,%d,%d,%d,%d" % (cur_cnt['pkt'],cur_cnt['ip'],cur_cnt['tcp'],cur_cnt['udp'],cur_cnt['iperf_tcp'],cur_cnt['iperf_udp'],cur_cnt['wget_tcp'],cur_cnt['wget_udp'])
    csv_line += ",%d,%d,%d,%d,%d,%d,%d,%d" % (cur_size['pkt'],cur_size['ip'],cur_size['tcp'],cur_size['udp'],cur_size['iperf_tcp'],cur_size['iperf_udp'],cur_size['wget_tcp'],cur_size['wget_udp'])
    print csv_line

    for i in cur_cnt.keys():
        cur_cnt[i] = 0
    for i in cur_size.keys():
        cur_size[i] = 0

    last_time = cur_time



if len(sys.argv) != 2:
    print "usage: %s <interface>" % sys.argv[0]
    sys.exit(1)

pc = pcap.pcap(name=sys.argv[1])

total_cnt = {'pkt':0, 'ip':0, 'tcp':0, 'udp':0, 'iperf_tcp':0, 'iperf_udp':0, 'wget_tcp':0, 'wget_udp':0}
total_size = {'pkt':0, 'ip':0, 'tcp':0, 'udp':0,'iperf_tcp':0, 'iperf_udp':0, 'wget_tcp':0, 'wget_udp':0}

cur_cnt = {'pkt':0, 'ip':0, 'tcp':0, 'udp':0, 'iperf_tcp':0, 'iperf_udp':0, 'wget_tcp':0, 'wget_udp':0}
cur_size = {'pkt':0, 'ip':0, 'tcp':0, 'udp':0, 'iperf_tcp':0, 'iperf_udp':0, 'wget_tcp':0, 'wget_udp':0}


# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGALRM, log_handler)

print_header()
last_time = time.time()
start_new_thread(logger,())
# signal.alarm(1)
while True:
    try:
        for timestamp, raw_buf in pc:
            output = {}

            # Unpack the Ethernet frame (mac src/dst, ethertype)
            eth = dpkt.ethernet.Ethernet(raw_buf)

            packet_size = len(raw_buf)

            cur_cnt['pkt'] += 1
            total_cnt['pkt'] += 1

            cur_size['pkt'] += packet_size
            total_size['pkt'] += packet_size

            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue

            ip = eth.data

            cur_cnt['ip'] += 1
            total_cnt['ip'] += 1

            cur_size['ip'] += packet_size
            total_size['ip'] += packet_size

            if ip.p==dpkt.ip.IP_PROTO_TCP:
               TCP=ip.data
               cur_cnt['tcp'] += 1
               total_cnt['tcp'] += 1
               cur_size['tcp'] += packet_size
               total_size['tcp'] += packet_size
               if (TCP.dport > 42420 and TCP.dport < 44430) or (TCP.sport > 42420 and TCP.sport < 44430):
                   cur_cnt['iperf_tcp'] += 1
                   total_cnt['iperf_tcp'] += 1
                   cur_size['iperf_tcp'] += packet_size
                   total_size['iperf_tcp'] += packet_size
               elif TCP.dport == 8000 or TCP.sport == 8000:
                   cur_cnt['wget_tcp'] += 1
                   total_cnt['wget_tcp'] += 1
                   cur_size['wget_tcp'] += packet_size
                   total_size['wget_tcp'] += packet_size


            elif ip.p==dpkt.ip.IP_PROTO_UDP:
               UDP=ip.data
               cur_cnt['udp'] += 1
               total_cnt['udp'] += 1
               cur_size['udp'] += packet_size
               total_size['udp'] += packet_size
               if (UDP.dport > 42420 and UDP.dport < 44430) or (UDP.sport > 42420 and UDP.sport < 44430):
                   cur_cnt['iperf_udp'] += 1
                   total_cnt['iperf_udp'] += 1
                   cur_size['iperf_udp'] += packet_size
                   total_size['iperf_udp'] += packet_size
               elif UDP.dport == 8000 or UDP.sport == 8000:
                   cur_cnt['wget_udp'] += 1
                   total_cnt['wget_udp'] += 1
                   cur_size['wget_udp'] += packet_size
                   total_size['wget_udp'] += packet_size
    except Exception as e:
        print "Netmon Error: ", e
