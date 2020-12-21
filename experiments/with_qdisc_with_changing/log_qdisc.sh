#!/bin/sh
while true
do
	echo "---------------Monitoring qdiscs-------------------"
	echo "$(date '+TIME:%H:%M:%S')" | tee -a qdisc_log.txt
	echo "$(/sbin/tc -p -s -d -j qdisc show dev h1-eth0)" | tee -a qdisc_log.txt
    sleep 2
done