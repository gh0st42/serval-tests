#!/usr/bin/env python
import os, sys

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
        print extract_values(line)
