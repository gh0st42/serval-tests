#!/usr/bin/env python

import os, sys, subprocess

SERVALD_BIN = "servald"

def getOwnSid():
    sid = subprocess.check_output(SERVALD_BIN+" id self", shell=True)
    return "'" + sid.split('\n')[2] + "'"

LINE_FILTERS = ['INSERT OR REPLACE INTO MANIFESTS', 'MeshMS2']
VALUES_START_STRING='VALUES('
VALUES_END_STRING=');'

def extract_values(string):
    try:
        startindex = string.index(VALUES_START_STRING) + len(VALUES_START_STRING)
        endindex = string.index(VALUES_END_STRING, startindex)
        return string[startindex:endindex]
    except ValueError:
        return ""

for filename in os.listdir(sys.argv[1]):
    file = open(sys.argv[1] + "/" + filename, 'r')
    lines = (line for line in file if all(filter in line for filter in LINE_FILTERS))
    for line in lines:
        line_list = line.split('VALUES')[1].replace('(', '').replace(')', '').replace('\n', '').replace(';', '').split(',')
	if (line_list[-4] == getOwnSid() or line_list[-3] == getOwnSid()):
	    print ','.join(line_list)
