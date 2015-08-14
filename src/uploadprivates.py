#!/usr/bin/env python
import sys, os, getopt

def main(argv):

  nodeslist = "/Users/adhoot/Documents/perf/nodes.txt"
  jar = 'hadoop-mapreduce-client-core-2.2.0-cdh5.0.0-beta-2-SNAPSHOT.jar'
  dir = '/opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/'
  privatesdir = "/Users/adhoot/privates/"
  user = "adhoot"

  try:
    opts, args = getopt.getopt(argv,"hn:j:d:p:u:",["nodelist=","jar=","dir=","privatesdir=","user="])
  except getopt.GetoptError as err:
    print(err)
    print 'uploadprivates.py -n <nodelist file> -j <jar file> -d <dir to place jar>  -p <dir containing privates> -u <user for ssh>'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'uploadprivates.py -n <nodelist file> -j <jar file> -d <dir to place jar> -p <dir containing privates> -u <user for ssh>'
      sys.exit()
    elif opt in ("-n", "--nodelist"):
      nodeslist = arg
    elif opt in ("-j", "--jar"):
      jar = arg
    elif opt in ("-d", "--dir"):
      dir = arg
    elif opt in ("-p", "--privatesdir"):
      privatesdir = arg
    elif opt in ("-u", "--user"):
      user = arg

  print "nodelist = {0}, jar = {1}, destination dir = {2}, privates dir = {3}".format(nodeslist, jar, dir, privatesdir)

  with open(nodeslist, 'rU') as f:
      for m in f.readlines():
          machineName = m.strip()
          print "Upload privates to " + machineName
          jarName = jar.strip()
          cmd = "rsync -ave ssh  {2}{1} {3}@{0}:~/jars/".format(machineName, jarName, privatesdir, user)
          print cmd
          os.system(cmd)

          base = os.path.splitext(jarName)[0]
          backupName = base + ".orig"

          print "Copy privates on " + machineName
          cmd = (
          'ssh  {4}@{0} "ls -l {2}{1}*'
                 + ' ;sudo mv -n  {2}{1}  {2}{3}'
                 + ' ;sudo cp -n ~/jars/{1} {2}/{1}'
                 + ' ;ls -l {2}{1}*'
                 +'"').format(machineName, jarName, dir, backupName, user)
          print cmd
          os.system(cmd)

if __name__ == "__main__":
  main(sys.argv[1:])
