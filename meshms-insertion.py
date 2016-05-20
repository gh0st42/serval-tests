#!/usr/bin/env python
import hashlib, subprocess, os, binascii, time, sys, json

def getOwnSid():
    sid = subprocess.check_output("servald id self", shell=True)
    return sid.split('\n')[2]
    
def getConversationsSids():
    conv_json = subprocess.check_output('/serval-tests/meshms-list-conv-curl ' + getOwnSid(), shell=True)
    parsed_conv_json = json.loads(conv_json)
    other_sid_list = [parsed_conv_json['rows'][i][2] for i in range(len(parsed_conv_json['rows']))]
    return other_sid_list
    
def printAllConversations():
    now = int(time.time())
    own_sid = getOwnSid()
    other_sids = getConversationsSids()
    for other_sid in other_sids:
        conversation_json = subprocess.check_output("/serval-tests/meshms-list-mess-curl " + own_sid + " " + other_sid, shell=True)
        parsed_conversation_json = json.loads(conversation_json)
        for conversation_message in parsed_conversation_json['rows']:
        	send_time = conversation_message[-2]
        	message = conversation_message[5]
        	direction = conversation_message[0]
        	
        	if direction == '>':
        		print str(send_time) + ',' + own_sid + ',' + other_sid + ',' + message
        	elif direction == '<':
        		print str(send_time) + ',' + other_sid + ',' + own_sid + ',' + message

printAllConversations()
