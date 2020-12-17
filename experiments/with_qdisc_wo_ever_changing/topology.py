#!/usr/bin/python

import re
import os
from time import sleep
import json
from mininet.net import Mininet
from mininet.link import TCIntf
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.link import TCLink
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mn_wifi.cli import CLI
import pandas as pd
import paramiko
from mininet.term import cleanUpScreens, makeTerm


def myNet():

    ctl ='192.168.1.102'
    net = Mininet( topo=None, link=TCLink, build=False)

    # Create nodes
    h1 = net.addHost( 'h1', mac='01:00:00:00:01:00', ip='192.168.0.1/24' )
    h2 = net.addHost( 'h2', mac='01:00:00:00:02:00', ip='192.168.0.2/24' )
    h3 = net.addHost( 'h3', mac='01:00:00:00:03:00', ip='192.168.0.3/24')

    # Create switches
    s1 = net.addSwitch( 's1', listenPort=6634, dpid='0000000000000010' )
    s2 = net.addSwitch( 's2', listenPort=6634, dpid='0000000000000020' )
    s3 = net.addSwitch( 's3', listenPort=6634, dpid='0000000000000030')

    print "*** Creating links"
    net.addLink(h1, s1, )
    net.addLink(h2, s2, )
    net.addLink(h3, s3, )
    net.addLink(s1, s2, )
    net.addLink(s1, s3, )

    # Add Controllers
    ctrl = net.addController( 'c1', controller=RemoteController, ip=ctl, port=6633)

    net.build()

    # Connect each switch to a different controller
    s1.start([ctrl])
    s2.start([ctrl])
    s3.start([ctrl])

    print "Testing network connectivity\n"
    net.pingAll()
    print "Dumping host connections\n"
    dumpNodeConnections(net.hosts)

    h1, h2, h3, s1, s2, s3 = net.getNodeByName('h1', 'h2', 'h3', 's1', 's2', 's3')

    s1.cmdPrint('ovs-vsctl show')

    h1.cmd('/sbin/tc qdisc del dev h1-eth0 root')
    sleep(3)
    h1.cmd('ifconfig h1-eth0 txqueuelen 10000')
    sleep(2)
    # h1.cmd('/sbin/tc qdisc add dev h1-eth0 root handle 1:0 htb default 20 && '
    #        '/sbin/tc class add dev h1-eth0 parent 1:0 classid 1:1 htb rate 250kbps ceil 250kbps && '
    #        '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:10 htb rate 240kbps ceil 240kbps && '
    #        '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:20 htb rate 10kbps ceil 10kbps && '
    #        '/sbin/tc class add dev h1-eth0 parent 10:1 handle 2: prio bands 5 && '
    #        '/sbin/tc class add dev h1-eth0 parent 2:1 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 2:2 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 2:3 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 2:4 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 2:5 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 20:1 handle 3: prio bands 5 && '
    #        '/sbin/tc class add dev h1-eth0 parent 3:1 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 3:2 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 3:3 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 3:4 pfifo && '
    #        '/sbin/tc class add dev h1-eth0 parent 3:5 pfifo && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x78 0xff flowid 2:1 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x58 0xff flowid 2:2 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x40 0xff flowid 2:3 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x38 0xff flowid 2:4 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x00 0xff flowid 2:5 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.2 ip tos 0x78 0xff flowid 3:1 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x58 0xff flowid 3:2 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x40 0xff flowid 3:3 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x38 0xff flowid 3:4 && '
    #        '/sbin/tc filter add dev h1-eth0 protocol ip parent 2:0 prio 1 u32 match ip dst 192.168.0.3 ip tos 0x00 0xff flowid 3:5')

    # h1.cmd('/sbin/tc qdisc add dev h1-eth0 root handle 1: prio bands 5 && '
    #        '/sbin/tc qdisc add dev h1-eth0 parent 1:1 handle 10: htb rate 250kbps ceil 250kbps && '
    #        '/sbin/tc qdisc add dev h1-eth0 parent 1:2 handle 20: htb rate 250kbps ceil 250kbps && '
    #        '/sbin/tc qdisc add dev h1-eth0 parent 1:3 handle 30: htb rate 250kbps ceil 250kbps && '
    #        '/sbin/tc qdisc add dev h1-eth0 parent 1:4 handle 40: htb rate 250kbps ceil 250kbps && '
    #        '/sbin/tc qdisc add dev h1-eth0 parent 1:5 handle 50: htb rate 250kbps ceil 250kbps && '
    #        )

    # h1.cmd('/sbin/tc qdisc add dev h1-eth0 root handle 1: htb default 11 && '
    #        '/sbin/tc class add dev h1-eth0 parent 1: classid 1:1 htb rate 250kbps ceil 250kbps burst 250kb && '
    #        '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:11 htb rate 240kbps ceil 240kbps burst 240kb && '
    #        '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:12 htb rate 10kbps ceil 10kbps burst 10kb && '
    #        '/sbin/tc qdisc add dev h1-eth0 parent 1:11 handle 11: prio bands 5 priomap 4 4 4 4 3 3 3 3 2 2 1 1 0 0 0 0 && '
    #        '/sbin/tc qdisc add dev h1-eth0 parent 1:12 handle 12: prio bands 5 priomap 4 4 4 4 3 3 3 3 2 2 1 1 0 0 0 0 && '
    #        '/sbin/tc filter add dev h1-eth0 root 1: protocol ip prio 1 u32 match ip protocol 17 0xff flowid 1:1 && '
    #        '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.0.2 flowid 1:11 && '
    #        '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.0.3 flowid 1:12 && '
    #        '/sbin/tc filter add dev h1-eth0 parent 1:11 protocol ip prio 1 u32 match ip dst 192.168.0.2 flowid 11: && '
    #        '/sbin/tc filter add dev h1-eth0 parent 1:12 protocol ip prio 1 u32 match ip dst 192.168.0.3 flowid 12:'
    #        )
    """
    to shape data at    9.6kbps -> 76800bit -> 76.8kbit
                        4.8kbps -> 38400bit -> 38.4kbit
                        2.4kbps -> 19200bit -> 19.2kbit
                        1.2kbps -> 9600bit  -> 9.6kbit
                        0.6kbps -> 4800bit  -> 4.8kbit
                        240kbps -> 1920000bit -> 1920kbit
                        250kbps -> 2000000bit -> 2000kbit
    """
    h1.cmd('/sbin/tc qdisc add dev h1-eth0 root handle 1: htb default 11 && '
           '/sbin/tc class add dev h1-eth0 parent 1: classid 1:1 htb rate 2000kbit ceil 2000kbit burst 250kb && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:11 htb rate 76.8kbit ceil 76.8kbit burst 10kb && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:12 htb rate 1920kbit ceil 1920kbit burst 240kb && '
           '/sbin/tc qdisc add dev h1-eth0 parent 1:11 handle 11: prio bands 4 priomap 3 3 2 3 0 3 1 3 3 3 3 3 3 3 3 3 && '
           '/sbin/tc qdisc add dev h1-eth0 parent 1:12 handle 12: prio bands 4 priomap 3 3 2 3 0 3 1 3 3 3 3 3 3 3 3 3 && '
           '/sbin/tc qdisc add dev h1-eth0 parent 11:1 handle 111: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 11:2 handle 112: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 11:3 handle 113: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 11:4 handle 114: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 12:1 handle 121: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 12:2 handle 122: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 12:3 handle 123: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 12:4 handle 124: netem limit 1000 delay 5ms && '
           '/sbin/tc filter add dev h1-eth0 parent 1: protocol ip prio 1 u32 matchall flowid 1:1 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.0.2 flowid 1:11 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.0.3 flowid 1:12 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:11 protocol ip prio 1 u32 match ip dst 192.168.0.2 flowid 11: && '
           '/sbin/tc filter add dev h1-eth0 parent 1:12 protocol ip prio 1 u32 match ip dst 192.168.0.3 flowid 12: && '
           '/sbin/tc filter add dev h1-eth0 parent 11:1 protocol ip prio 1 u32 match ip dsfield 0x1e 0x1e flowid 111: && '
           '/sbin/tc filter add dev h1-eth0 parent 11:2 protocol ip prio 1 u32 match ip dsfield 0x16 0x1e flowid 112: && ' #match ip tos 0x58 0xff match ip protocol 0x11 0xff
           '/sbin/tc filter add dev h1-eth0 parent 11:3 protocol ip prio 1 u32 match ip dsfield 0x0e 0x1e flowid 113: && '
           '/sbin/tc filter add dev h1-eth0 parent 11:4 protocol ip prio 1 u32 match ip dsfield 0x04 0x1e match ip dsfield 0x00 0x1e flowid 114: && '
           '/sbin/tc filter add dev h1-eth0 parent 12:1 protocol ip prio 1 u32 match ip dsfield 0x1e 0x1e flowid 121: && '
           '/sbin/tc filter add dev h1-eth0 parent 12:2 protocol ip prio 1 u32 match ip dsfield 0x16 0x1e flowid 122: && '
           '/sbin/tc filter add dev h1-eth0 parent 12:3 protocol ip prio 1 u32 match ip dsfield 0x0e 0x1e flowid 123: && '
           '/sbin/tc filter add dev h1-eth0 parent 12:4 protocol ip prio 1 u32 match ip dsfield 0x04 0x1e match ip dsfield 0x00 0x1e flowid 124:'
           )

    sleep(3)
    makeTerm(h2, title='mgen receiver', cmd="mgen input receive.mgn output receive_log.txt")
    sleep(1)
    makeTerm(h1, title='class statistics', cmd="watch -dc tc -s -d -j class show dev h1-eth0")
    sleep(2)
    makeTerm(h1, title='mgen sender', cmd="mgen input send.mgn")

    # makeTerm(h2, title='mgen receiver', cmd='mgen input receive.mgn output receive_log.txt')
    # makeTerm(h2, title='packet sniffer receiver', cmd="sudo python packet_sniffer_receiver.py")
    # makeTerm(h1, title='packet sniffer sender', cmd="sudo python packet_sniffer_sender.py")
    # makeTerm(h1, title='qdisc statistics', cmd="sh log_qdisc.sh")
    # makeTerm(h1, title='class statistics', cmd="sh log_class.sh")
    # makeTerm(h1, title='mgen sender', cmd="mgen input send.mgn")
    sleep(1)

    CLI(net)
    net.stop()
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel('info')
    myNet()