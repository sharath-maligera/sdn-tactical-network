#!/bin/sh
while true
do
	echo "---------------Monitoring classes-------------------"
	echo "$(date '+TIME:%H:%M:%S')" | tee -a class_log.txt
	echo "$(/sbin/tc -p -s -d -j class show dev h1-eth0)" | tee -a class_log.txt
    sleep 2
done