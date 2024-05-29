#!/bin/bash

# This script generates TCP traffic flows from host1 and host3 tp host2.
# Two servers are run as background daemons on host2. The servers listen to ports 5201. and 5202, respectively.
# The clients run on host1 and host2 have the following paramters:
# - Total transmission time is 10,000 seconds.
# - Time between reports is 10 seconds.
# - The number of simultaneous connections to the server is 8.
# - The target bandwidth for each connection is 100Kbps (total is 1.6Mpbs).
# - The TCP maximum segment size is 1460 octets (results in MTU=1500).
# - The traffic is bound to the interface facing the leaf router.

set -eu

startAll() {
    echo "starting traffic on all hosts"
    docker exec host2 iperf3 -s -p 5201 -D
    docker exec host2 iperf3 -s -p 5202 -D
    docker exec host1 iperf3 -c 192.168.2.11 -t 10000 -i 10 -p 5201 -B 192.168.1.11 -P 8 -b 200K -M 1460 &
    docker exec host3 iperf3 -c 192.168.2.11 -t 10000 -i 10 -p 5202 -B 192.168.3.11 -P 8 -b 200K -M 1460 &
}

stopAll() {
    echo "stopping all traffic"
    docker exec host1 pkill iperf3
    docker exec host2 pkill iperf3
    docker exec host3 pkill iperf3
}

if [ $1 == "start" ]; then
    startAll
fi

if [ $1 == "stop" ]; then
    stopAll
fi
