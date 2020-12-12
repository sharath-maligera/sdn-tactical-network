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
    h1.cmd('/sbin/tc qdisc add dev h1-eth0 root handle 1: htb default 11 && '
           '/sbin/tc class add dev h1-eth0 parent 1: classid 1:1 htb rate 250kbps ceil 250kbps burst 250kb && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:11 htb rate 240kbps ceil 240kbps burst 240kb && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:12 htb rate 10kbps ceil 10kbps burst 10kb && '
           '/sbin/tc qdisc add dev h1-eth0 parent 1:11 handle 11: prio bands 5 priomap 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 && '
           '/sbin/tc qdisc add dev h1-eth0 parent 1:12 handle 12: prio bands 5 priomap 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 && '
           '/sbin/tc class add dev h1-eth0 parent 11:1 handle 111: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 11:2 handle 112: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 11:3 handle 113: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 11:4 handle 114: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 11:5 handle 115: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 12:1 handle 121: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 12:2 handle 122: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 12:3 handle 123: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 12:4 handle 124: pfifo && '
           '/sbin/tc class add dev h1-eth0 parent 12:5 handle 125: pfifo && '
           '/sbin/tc filter add dev h1-eth0 root 1: protocol ip prio 1 u32 match ip protocol 17 0xff flowid 1:1 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.0.2 flowid 1:11 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.0.3 flowid 1:12 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:11 protocol ip prio 1 u32 match ip dst 192.168.0.2 flowid 11: && '
           '/sbin/tc filter add dev h1-eth0 parent 1:12 protocol ip prio 1 u32 match ip dst 192.168.0.3 flowid 12: && '
           '/sbin/tc filter add dev h1-eth0 parent 11: protocol ip prio 1 u32 match ip dsfield 0x1e 0x1e flowid 11:1 && '
           '/sbin/tc filter add dev h1-eth0 parent 11: protocol ip prio 1 u32 match ip dsfield 0x16 0x1e flowid 11:2 && ' #match ip tos 0x58 0xff match ip protocol 0x11 0xff
           '/sbin/tc filter add dev h1-eth0 parent 11: protocol ip prio 1 u32 match ip dsfield 0x10 0x1e flowid 11:3 && '
           '/sbin/tc filter add dev h1-eth0 parent 11: protocol ip prio 1 u32 match ip dsfield 0x0e 0x1e flowid 11:4 && '
           '/sbin/tc filter add dev h1-eth0 parent 11: protocol ip prio 1 u32 match ip dsfield 0x00 0x1e flowid 11:5 && '
           '/sbin/tc filter add dev h1-eth0 parent 12: protocol ip prio 1 u32 match ip dsfield 0x1e 0x1e flowid 12:1 && '
           '/sbin/tc filter add dev h1-eth0 parent 12: protocol ip prio 1 u32 match ip dsfield 0x16 0x1e flowid 12:2 && '
           '/sbin/tc filter add dev h1-eth0 parent 12: protocol ip prio 1 u32 match ip dsfield 0x10 0x1e flowid 12:3 && '
           '/sbin/tc filter add dev h1-eth0 parent 12: protocol ip prio 1 u32 match ip dsfield 0x0e 0x1e flowid 12:4 && '
           '/sbin/tc filter add dev h1-eth0 parent 12: protocol ip prio 1 u32 match ip dsfield 0x00 0x1e flowid 12:5'
           )

    sleep(3)
    h1.cmdPrint('/sbin/tc -s -d qdisc show dev h1-eth0')
    sleep(3)
    h1.cmdPrint('/sbin/tc -s -d class show dev h1-eth0')
    sleep(3)
    h1.cmdPrint('/sbin/tc -s class ls dev h1-eth0')
    sleep(3)

    CLI(net)
    sleep(3)
    h2.cmd('/usr/bin/mgen event "listen udp 5001-5005" > mgenlog_output.txt &')
    sleep(5)
    h1.cmd('/usr/bin/mgen input send.mgn > mgenlog_input.txt &')

    sleep(300)
    net.stop()
    sleep(5)
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel('info')
    myNet()