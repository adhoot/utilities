#!/usr/bin/env python
import sys, os

#cmdargs = str(sys.argv)
#nodeslist = str(sys.argv[1])
nodeslist = "/Users/adhoot/Documents/perf/nodes.txt"
mr2file = 'hadoop-mapreduce-client-core-2.2.0-cdh5.0.0-beta-2-SNAPSHOT.jar'
mr2home = '/opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/'
with open(nodeslist, 'rU') as f:
    for m in f.readlines():
        print "Upload privates to " + m.strip()
        cmd = "scp /Users/adhoot/Documents/perf/jars/{1} {0}:~/jars/".format(m.strip(), mr2file.strip())
        print cmd
        #os.system(cmd)
        
        print "Copy privates on " + m.strip()
        cmd = (
        'ssh {0} "ls -l {2}{1}*'
               #+ ' ;sudo mv {2}{1}  {2}{1}.orig'
               #+ ' ;sudo cp /home/adhoot/jars/{1} {2}/{1}'
               #+ ' ;ls -l {2}{1}*'
               +'"').format(m.strip(), mr2file.strip(), mr2home)
        print cmd
        os.system(cmd)