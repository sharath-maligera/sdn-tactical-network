#!/bin/sh
while true
do
	echo "---------------Monitoring qdiscs-------------------"
	echo "$(/sbin/tc -p -s -d -j qdisc show dev h1-eth0)" | tee -a qdisc_log.json
    sleep 1
done