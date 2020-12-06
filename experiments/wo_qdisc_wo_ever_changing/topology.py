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