#!/usr/bin/env python
import hashlib, subprocess, os, binascii, time

SERVALD_BIN = "servald"

def getOwnSid():
    sid = subprocess.check_output(SERVALD_BIN+" id self", shell=True)
    return sid.split('\n')[2]

def printPublicRhizome():
	rhizome_list = (subprocess.check_output(SERVALD_BIN + " rhizome list", shell=True)).split('\n')
	for rhizome_file in rhizome_list[2:-1]:
		rhizome_file_splitted = rhizome_file.split(':')
		if (rhizome_file_splitted[1] == 'MeshMS2') or (rhizome_file_splitted[1] == 'file' and len(rhizome_file_splitted[-2]) == 0):
			pass
		else:
			if rhizome_file_splitted[-3] != getOwnSid() and rhizome_file_splitted[-2] != getOwnSid():
				pass
			else:
				print ','.join(rhizome_file_splitted)
    
printPublicRhizome()
