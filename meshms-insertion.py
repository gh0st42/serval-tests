#!/usr/bin/env python
import hashlib, subprocess, os, binascii, time

SERVALD_BIN = "servald"

def getOwnSid():
    sid = subprocess.check_output(SERVALD_BIN+" id self", shell=True)
    return sid.split('\n')[2]
    
def getConversationsSids():
    sids = subprocess.check_output(SERVALD_BIN + " meshms list conversations " + getOwnSid(), shell=True)
    return [x.split(':')[1] for x in sids.split('\n')[2:-1]]
    
def printAllConversations():
	now = int(time.time())
	own_sid = getOwnSid()
	other_sids = getConversationsSids()
	for other_sid in other_sids:
		conversation = (subprocess.check_output(SERVALD_BIN + " meshms list messages " + own_sid + " " + other_sid, shell=True)).split('\n')
		for conversation_message in conversation[2:-1]:
			print str(now-int(conversation_message.split(':')[2])) + ',' + own_sid + ',' + other_sid + ',' + conversation_message.split(':')[4]
    
printAllConversations()
