#!/usr/bin/env python

import sys, os
from datetime import datetime

try:
    if not os.path.isfile(sys.argv[1]):
        sys.stderr.write("[Error]: %s is not a file\n" % sys.argv[1])
        sys.exit(1)
except IndexError:
    sys.stderr.write("Usage: converttimestamps.py <logfile.log>\n")
    sys.exit(1)

with open(sys.argv[1]) as log:
    lines = log.readlines()
    first = lines[0].split(' ')
    start = datetime.strptime(str(first[0]) + ' ' + str(first[1]), "%Y-%m-%d %H:%M:%S,%f")
    for lineitem in lines:
        conv = None
        line = lineitem.split(' ')
        if (len(line) > 2):
            try:
                diff = datetime.strptime(str(line[0]) + ' ' + str(line[1]), "%Y-%m-%d %H:%M:%S,%f") - start
                line[1]=str(diff.total_seconds())
                conv = 1
                print ' '.join(line[1:]).strip()
            except ValueError:
                pass
        if not conv:
            if (lineitem.strip()):
                print lineitem.strip()

