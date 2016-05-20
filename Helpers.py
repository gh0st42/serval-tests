#!/usr/bin/env python
import hashlib, subprocess, os, binascii, sys, random

SERVALD_BIN = "servald"
RANDOM_FILES_FOLDER = "/root/tmp/"

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
	if not os.path.exists(RANDOM_FILES_FOLDER): os.mkdir(RANDOM_FILES_FOLDER, 0755)
	if size_k == 'f1':
		size_k = random.choice(F1)
		filepath = RANDOM_FILES_FOLDER+name.replace('f1', str(size_k))
	elif size_k == 'f2':
		size_k = random.choice(F2)
		filepath = RANDOM_FILES_FOLDER+name.replace('f2', str(size_k))
	elif size_k == 'f3':
		size_k = random.choice(F3)
		filepath = RANDOM_FILES_FOLDER+name.replace('f3', str(size_k))
	elif size_k == 'f4':
		size_k = random.choice(F4)
		filepath = RANDOM_FILES_FOLDER+name.replace('f4', str(size_k))
	else:
		filepath = RANDOM_FILES_FOLDER+name
	
	with open(filepath, 'wb') as f:
		# write 1k random data
		f.write(os.urandom(1024))
		#write missing bytes 
		f.write('\0' * 1024 * (int(size_k)-1))
		
	print sid, filepath, their_sid
	
	if their_sid:
		commmand = [SERVALD_BIN, "rhizome", "add", "file", sid, filepath, "/dev/null", "", "sender="+sid, "recipient="+their_sid]
	else:
		commmand = ["/serval-tests/rhizome-insert-curl", filepath]
	subprocess.call(commmand)
	os.remove(filepath)
	return size_k

def randomMeshMS(my_sid, their_sid, messsage):
    subprocess.call(["/serval-tests/meshms-send-curl", my_sid, their_sid, messsage])
