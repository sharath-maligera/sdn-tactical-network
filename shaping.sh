#!/bin/bash

TC=/sbin/tc

# interface traffic will leave on
IF=h1-eth0

# host 2
DST_VHF=192.168.0.2/24
# host 3
DST_UHF=192.168.0.3/24

# filter command to filter packets based on destination host
U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"

create () {
  echo "== SHAPING STARTED =="

  # create the root qdisc
  $TC qdisc add dev $IF root handle 1:0 htb default 20

  # create the parent qdisc for both VHF and UHF qdisc
  $TC class add dev $IF parent 1:0 classid 1:1 htb rate 250kbps ceil 250kbps

  # create UHF qdisc with bandwidth 240kbps and reference it's parent
  $TC class add dev $IF parent 1:1 classid 1:10 htb rate 240kbps ceil 240kbps

  # create VHF qdisc with bandwidth 10kbps and reference it's parent
  $TC class add dev $IF parent 1:1 classid 1:20 htb rate 9.6kbps ceil 10kbps

  # filters to ensure packets are enqueued to the correct child qdisc based on the dst IP of the packet
  $U32 match ip dst $DST_UHF flowid 1:10
  $U32 match ip dst $DST_VHF flowid 1:20

  echo "== SHAPING DONE =="
}

# run clean to ensure existing tc is not configured
clean () {
  echo "== CLEAN INIT =="
  $TC qdisc del dev $IF root
  echo "== CLEAN DONE =="
}

clean
create