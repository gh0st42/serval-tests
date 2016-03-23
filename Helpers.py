#!/usr/bin/env python
import hashlib, subprocess, os, binascii, sys, random

SERVALD_BIN = "servald"

F1 = [64, 256, 512]
F2 = [1000, 5000, 10000]
F3 = [25000, 50000, 100000]
F4 = F1 + F2 + F3
   
def getSid():
    sid = subprocess.check_output(SERVALD_BIN+" id self", shell=True)
    return sid.split('\n')[2]
    
def getNeightbourSids():
	with open("/tmp/serval-all-sids", 'r') as sid_file:
		return filter(lambda x: x != getSid(), map(lambda x: x.replace('\n', ''), sid_file.readlines()))

def rhizomeRandomFile(name, size_k, sid, their_sid=None):
	if size_k == 'f1':
		size_k = random.choice(F1)
		filepath = "/tmp/"+name.replace('f1', str(size_k))
	elif size_k == 'f2':
		size_k = random.choice(F2)
		filepath = "/tmp/"+name.replace('f2', str(size_k))
	elif size_k == 'f3':
		size_k = random.choice(F3)
		filepath = "/tmp/"+name.replace('f3', str(size_k))
	elif size_k == 'f4':
		size_k = random.choice(F4)
		filepath = "/tmp/"+name.replace('f4', str(size_k))
	else:
		filepath = "/tmp/"+name
	
	with open(filepath, 'wb') as f:
		# write 1k random data
		f.write(os.urandom(1024))
		#write missing bytes 
		f.write('\0' * 1024 * (int(size_k)-1))
		
	print sid, filepath, their_sid
    
	commmand = [SERVALD_BIN, "rhizome", "add", "file", sid, filepath, "/dev/null", "", "sender="+sid]
	if their_sid: commmand.append("recipient="+their_sid)
	subprocess.call(commmand)
	os.remove(filepath)

def randomMeshMS(size, my_sid, their_sid):
    subprocess.call([SERVALD_BIN, "meshms", "send", "message", my_sid, their_sid, binascii.b2a_hex(os.urandom(size/2))])
