#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument for nodecount required, $# provided"
echo $1 | grep -E -q '^[0-9]+$' || die "Numeric argument required, $1 provided"

nodecount=$1
rounds=1
export llamahost=127.0.0.1
echo $nodecount nodes for the cluster used
echo using llama host $llamahost

minillama minicluster -nodes $nodecount > minillama.log&
n=0; until [ $n -ge 10 ]; do  curl http://$llamahost:15001/ && break; echo Iteration $n; n=$(($n+1)); sleep 2; done
echo "## Llama ready .... starting perf test ###"

export handle=`llamaclient register -callback 127.0.0.1:16000 -clientid 1df87d05786d42cb:83d93b6ebc4e9b4f -llama $llamahost:15000`
llamaclient getnodes  -llama $llamahost:15000 -handle $handle > ./nodes.txt
export nodes=`paste -d, -s ./nodes.txt`
echo "### Starting 5 iterations of allocations on a $nodecount sized allocations"
n = 0
until [ $n -ge 5 ]; do 
	llamaclient load  -llama $llamahost:15000 -callback localhost:20000 -clients 1 -rounds $rounds -holdtime 0 -sleeptime 0 -expandtime 0  -locations $nodes -cpus 1 -memory 128 -user adhoot
	curl http://$llamahost:15001/jmx\?qry\=metrics:name\=llama.am.queue.*allocation-latency\*
done
kill %%
