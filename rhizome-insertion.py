#!/usr/bin/env python
import hashlib, subprocess, os, binascii, time, sys

SERVALD_BIN = "servald"

def printPublicRhizome(log_files_path):
	for log_file_path in os.listdir(log_files_path):
		if not(log_file_path.endswith('.log')):
			continue
		
		with open(log_files_path + log_file_path, 'r') as log_file:
			log_list = log_file.readlines()
			for line in log_list:
				if ('INSERT OR REPLACE INTO MANIFESTS' in line) and not ('MeshMS2' in line):
					line_list = line.split('VALUES')[1].replace('(', '').replace(')', '').replace('\n', '').replace(';', '').split(',')
					if line_list[-3] == 'NULL':
						print ','.join(line_list)
    
printPublicRhizome(sys.argv[1])
