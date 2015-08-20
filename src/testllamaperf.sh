#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument for nodecount required, $# provided"
echo $1 | grep -E -q '^[0-9]+$' || die "Numeric argument required, $1 provided"

nodecount=$1
: ${rounds:=1}
: ${iterations:=2}
export llamahost=127.0.0.1
echo $nodecount nodes for the cluster
echo using llama host $llamahost
echo testing $rounds rounds for $iterations iterations

minillama minicluster -nodes $nodecount > minillama.log&
n=0; until [ $n -ge 10 ]; do  curl http://$llamahost:15001/ && break; echo Iteration $n; n=$(($n+1)); sleep 2; done
echo "## Llama ready .... starting perf test ###"

export handle=`llamaclient register -callback $llamahost:16000 -clientid 1df87d05786d42cb:83d93b6ebc4e9b4f -llama $llamahost:15000`
[[ -z $handle ]] && die "Registeration was not successful"
echo Got handle $handle

llamaclient getnodes  -llama $llamahost:15000 -handle $handle > ./nodes.txt
export nodes=`paste -d, -s ./nodes.txt`
[[ -z $nodes ]] && die "Get nodes was not successful"
echo Got llama nodes $nodes

echo "### Starting $iterations iterations of allocations on a $nodecount sized allocations"
n=0; until [ $n -ge $iterations ]; do 
    echo "### Test iteration " $n
    llamaclient load  -llama $llamahost:15000 -callback localhost:20000 -clients 1 -rounds $rounds -holdtime 0 -sleeptime 0 -expandtime 0  -locations $nodes -cpus 1 -memory 128 -user adhoot
	curl http://$llamahost:15001/jmx\?qry\=metrics:name\=llama.am.queue.*allocation-latency\*
	n=$((n+1))

	read -p "Press a key to continue"
done

echo "End of test killing minillama"
kill %%
