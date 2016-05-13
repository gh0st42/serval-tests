#!/usr/bin/env python

import hashlib, socket, time, argparse, signal, sys, random, os
from Helpers import *

parser = argparse.ArgumentParser(description='Periodically generate and add directed files into the serval rhizome store.')
parser.add_argument('-d', dest='min_delay_ms', default=0, help='set minimum insertion delay (ms)')
parser.add_argument('-j', dest='delay_jitter_ms', default=1000, help='set maximum jitter (ms) for insertion delay')
parser.add_argument('-s', dest='size_k', default=1024, help='size (KiB) of files to be inserted')
parser.add_argument('-t', dest='timeout', default=-1, type=int, help='stop after timout')
parser.add_argument('-l', dest='log', action='store_true', help='file, where proactive logging happens')
args = parser.parse_args()

# adding parsed /default values to global dict 
globals().update(vars(args))
random.seed(socket.gethostname())
my_sid = getSid()
neighbours = getNeightbourSids()

later = time.time() + timeout

all_subdirs = ['/tmp/serval-monitor/' + d for d in os.listdir('/tmp/serval-monitor/') if os.path.isdir('/tmp/serval-monitor/' + d) and d.startswith('20')]
monitor_path = max(all_subdirs, key=os.path.getctime)
outfile = monitor_path + '/active/rhizome-direceted-active-' + socket.gethostname() + '.csv'

f = open(outfile, 'w')
f.write('timestamp,sender,recipient,file\n')
f.close

if __name__ == "__main__":
    count = 0
    running = True
    def signal_handler(signal, frame): print("Received SIGINT, stopping..."); sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    basename = socket.gethostname()
    if len(neighbours) == 0: print("No neighbours found, exiting"); sys.exit(1)
    while running:
    	if timeout != -1 and later < time.time():
			running = False
			break
        their_sid = random.choice(neighbours)
        size_str = rhizomeRandomFile(basename+"-"+str(size_k)+"k-"+str(count)+".bin", size_k, mySid, their_sid=their_sid)
        if log:
                f = open(outfile, 'a')
		f.write(str(int(time.time())) + ',' + str(my_sid) + ',' + str(their_sid) + ',' + basename+"-"+str(size_str)+"k-"+str(count)+".bin" + '\n')
                f.close
        count += 1
        insertion_delay_ms = min_delay_ms + random.randint(0, delay_jitter_ms)
        print("Inserted files to "+their_sid+", sleeping for "+str(insertion_delay_ms)+"ms")
        time.sleep(float(insertion_delay_ms)/100)
