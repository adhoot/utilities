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
    for lineitem in lines:
        conv = None
        line = lineitem.split(' ')
        if (len(line) > 2):
            try:
                print ' '.join(line[4:]).strip()
                conv = 1
            except ValueError:
                pass
        if not conv:
            if (lineitem.strip()):
                print lineitem.strip()

