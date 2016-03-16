#!/usr/bin/env python
import hashlib, subprocess, os, binascii

SERVALD_BIN = "servald"
   
def getSid():
    sid = subprocess.check_output(SERVALD_BIN+" id self", shell=True)
    return sid.split('\n')[2]
    
def getNeightbourSids():
    sids = subprocess.check_output(SERVALD_BIN+" id allpeers", shell=True)
    return sids.split('\n')[2:-1]

def rhizomeRandomFile(name, size_k, sid, their_sid=None):
    filepath = "/tmp/"+name
    with open(filepath, 'wb') as f:
        # write 1k random data
        f.write(os.urandom(1024))
        # write missing bytes 
        f.write('\0'*1024*(size_k-1))
    
    commmand = [SERVALD_BIN, "rhizome", "add", "file", sid, filepath, "/dev/null", "", "sender="+sid]
    if their_sid: commmand.append("recipient="+their_sid)
    subprocess.call(commmand)
    os.remove(filepath)

def randomMeshMS(size, my_sid, their_sid):
    subprocess.call([SERVALD_BIN, "meshms", "send", "message", my_sid, their_sid, binascii.b2a_hex(os.urandom(size/2))])
