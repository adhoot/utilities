#!/usr/bin/env python
import sys, os
import urllib2

attemptid = str(sys.argv[1]).strip()
#taskid = str(sys.argv[2]).strip()
machinename = str(sys.argv[2]).strip()

tasktrackerlogurl = "http://{0}.halxg.cloudera.com:21101/logs/hadoop-cmf-MAPREDUCE-1-TASKTRACKER-{0}.halxg.cloudera.com.log.out".format(machinename)

#taskdetailsurl = "http://a1009.halxg.cloudera.com:21001/taskdetails.jsp?tipid=%s" % taskid

response = urllib2.urlopen(tasktrackerlogurl)
ttlog = response.read()

ttlines = ttlog.split('\n')
attemptlines = [line for line in ttlines if attemptid in line]
print "\n".join(attemptlines)
