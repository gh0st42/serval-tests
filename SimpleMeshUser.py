#!/usr/bin/env python

import hashlib, socket, time, argparse, signal, sys, random
from Helpers import *

parser = argparse.ArgumentParser(description='Periodically generate and send messages to neighbourly serval peers')
parser.add_argument('-d', dest='min_delay_ms', default=0, help='set minimum insertion delay (ms)')
parser.add_argument('-j', dest='delay_jitter_ms', default=100, help='set maximum jitter (ms) for insertion delay')
parser.add_argument('-s', dest='size_b', default=64, help='size (Byte) of files to be inserted')
parser.add_argument('-t', dest='timeout', default=-1, type=int, help='stop after timout')
args = parser.parse_args()

# adding parsed /default values to global dict 
globals().update(vars(args))
random.seed(socket.gethostname())
my_sid = getSid()
neighbours = getNeightbourSids()

later = time.time() + timeout

if __name__ == "__main__":
	count = 0
	running = True
	def signal_handler(signal, frame): print("Received SIGINT, stopping..."); sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	if len(neighbours) == 0: print("No neighbours found, exiting"); sys.exit(1)
	while running:
		if timeout != -1 and later < time.time():
			running = False
			break
		their_sid = random.choice(neighbours)
		randomMeshMS(size_b, my_sid, their_sid)
		count += 1
		insertion_delay_ms = min_delay_ms + random.randint(0, delay_jitter_ms)
		print("Send message to "+their_sid+", sleeping for "+str(insertion_delay_ms)+"ms")
		time.sleep(float(insertion_delay_ms)/100)
