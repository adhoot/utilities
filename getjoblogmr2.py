#!/usr/bin/env python
import sys, os
import urllib2

attemptid = str(sys.argv[1]).strip()
containerid = str(sys.argv[2]).strip()
machinename = str(sys.argv[3]).strip()

nmlogurl = "http://{0}.halxg.cloudera.com:8042/logs/hadoop-cmf-YARN-1-NODEMANAGER-{0}.halxg.cloudera.com.log.out".format(machinename)

#taskdetailsurl = "http://a1009.halxg.cloudera.com:21001/taskdetails.jsp?tipid=%s" % taskid
print "Downloading logs for {0} from machine {1}".format(attemptid, machinename)

nmresponse = urllib2.urlopen(nmlogurl)
nmlog = nmresponse.read()

ttlines = nmlog.split('\n')
attemptlines = [line for line in ttlines if (attemptid in line or containerid in line)]
print "\n".join(attemptlines)
