#!/bin/bash
die () {
    echo >&2 "$@"
    kill %%
    exit 1
}

set -ex

. /opt/toolchain/toolchain.sh

export JAVA_HOME=$JAVA7_HOME
export PATH=${JAVA_HOME}/bin:${PATH}:.

export THRIFT_HOME=/opt/toolchain/thrift-0.9.0
export PATH=${THRIFT_HOME}/bin:${PATH}

export THRIFT_VERSION=`thrift --version`
if [ "${THRIFT_VERSION}" != "Thrift version 0.9.0" ]; 
then
  echo "Incorrect ${THRIFT_VERSION}, it should be 0.9.0"
  exit 1
fi

echo version for build is  ${POM_VERSION}

rm -rf $WORKSPACE/logs
mkdir -p $WORKSPACE/logs

: ${clienthost:=localhost}
export llamahost=127.0.0.1
echo $NODECOUNT nodes for the cluster
echo using llama host $llamahost
echo testing $ROUNDS rounds for $ITERATIONS iterations

#clean
mvn clean package -Pdist -Dtar -Dmaven.javadoc.skip=true -DskipTests

echo Using hadoop $HADOOPVERSION
rm -rf $HADOOPVERSION

curl -O http://repos.jenkins.cloudera.com/cdh5-nightly/cdh/5/$HADOOPVERSION.tar.gz
tar -xzf $HADOOPVERSION.tar.gz
curl -O http://github.mtv.cloudera.com/raw/adhoot/mr2-pseudo-dist/anucopy/mr2-pseudo-conf/conf.tar.gz
mkdir -p  $HADOOPVERSION/etc/hadoop/
echo Copy down yarn site to the conf folder
tar -xf conf.tar.gz -C $HADOOPVERSION/etc/hadoop/
tar -xf conf.tar.gz -C mini-llama/target/mini-llama-1.0.0-cdh5.5.0-SNAPSHOT/mini-llama-1.0.0-cdh5.5.0-SNAPSHOT/conf/
export HADOOP_HOME=$(readlink -f $HADOOPVERSION)

echo ### Starting perf test
pushd mini-llama/target/mini-llama-1.0.0-cdh5.5.0-SNAPSHOT/mini-llama-1.0.0-cdh5.5.0-SNAPSHOT/bin


minillama minicluster -nodes $NODECOUNT > $WORKSPACE/logs/minillama.log&
n=0; until [ $n -ge 300 ]; do  curl http://$llamahost:15001/ && break; echo Iteration $n; n=$(($n+1)); sleep 2; done
echo "## Llama ready .... starting perf test ###"

sleep 10

export handle=`llamaclient register -callback $llamahost:16000 -clientid 1df87d05786d42cb:83d93b6ebc4e9b4f -llama $llamahost:15000`
[[ -z $handle ]] && die "Registeration was not successful"
echo Got handle $handle

llamaclient getnodes  -llama $llamahost:15000 -handle $handle > ./nodes.txt
export nodes=`paste -d, -s ./nodes.txt`
[[ -z $nodes ]] && die "Get nodes was not successful"
echo Got llama nodes $nodes

for CLIENTCOUNT in $CLIENTCOUNTS
do
    echo "### Using $CLIENTCOUNT number of client threads"
    echo "### Starting $ITERATIONS iterations of allocations on a $NODECOUNT sized allocations"
    n=0; until [ $n -ge $ITERATIONS ]; do
        echo "### Test iteration " $n
        testlog=$WORKSPACE/logs/clients${CLIENTCOUNT}_nodes${NODECOUNT}_expand${EXPANDHOLDTIME}_rounds${ROUNDS}_iteration${n}.log 
        llamaclient load  -llama $llamahost:15000 -callback $clienthost:20000 -clients $CLIENTCOUNT -rounds $ROUNDS -holdtime 0 -sleeptime 0 -expandtime $EXPANDHOLDTIME  -locations $nodes -cpus 1 -memory 128 -user adhoot > $testlog
	curl http://$llamahost:15001/jmx\?qry\=metrics:name\=llama.am.queue.*allocation-latency\* >> $testlog
	n=$((n+1))

    done
done
gzip $WORKSPACE/logs/*.log

echo "End of test killing minillama"
kill %%
