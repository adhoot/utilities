#!/bin/bash

let count=0
echo Running mvn -o -Dtest=$* surefire:test until it fails
while mvn -o -Dtest=$* surefire:test 2>&1 > target/lastbuild.log
do
    now=`date`
    echo "Test Run $count - $now" >> target/looptest.log
    let count=$count+1
done
