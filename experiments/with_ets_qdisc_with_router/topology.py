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

    ctl ='192.168.1.101'
    net = Mininet( topo=None, link=TCLink, build=False)

    # Create nodes
    # h1 = net.addHost('h1', mac='01:00:00:00:01:00', ip='192.168.1.10/24')
    # h2 = net.addHost('h2', mac='01:00:00:00:02:00', ip='192.168.2.10/24')
    # h3 = net.addHost('h3', mac='01:00:00:00:03:00', ip='192.168.3.10/24')

    h1 = net.addHost('h1', ip='192.168.10.10/24')
    h2 = net.addHost('h2', ip='192.168.20.10/24')
    h3 = net.addHost('h3', ip='192.168.30.10/24')
    h4 = net.addHost('h3', ip='192.168.40.10/24')
    r1 = net.addHost('r1', ip='192.168.10.1/24', inNamespace=False) #, inNamespace=True

    # Create switches
    s1 = net.addSwitch('s1', listenPort=6634, dpid='0000000000000010')
    s2 = net.addSwitch('s2', listenPort=6634, dpid='0000000000000020')
    s3 = net.addSwitch('s3', listenPort=6634, dpid='0000000000000030')
    s4 = net.addSwitch('s4', listenPort=6634, dpid='0000000000000040')

    print "*** Creating links"
    net.addLink(h1, s1, )
    net.addLink(h2, s2, )
    net.addLink(h3, s3, )
    net.addLink(h4, s4, )
    net.addLink(s1, r1, )
    net.addLink(s2, r1, )
    net.addLink(s3, r1, )
    net.addLink(s4, r1, )

    h1.intf('h1-eth0').setMAC('01:00:00:00:01:00')
    h2.intf('h2-eth0').setMAC('01:00:00:00:02:00')
    h3.intf('h3-eth0').setMAC('01:00:00:00:03:00')
    h4.intf('h4-eth0').setMAC('01:00:00:00:04:00')
    r1.intf('r1-eth0').setMAC('00:00:00:00:01:01')

    r1.intf('r1-eth1').setIP('192.168.20.1/24')
    r1.intf('r1-eth1').setMAC('00:00:00:00:01:02')

    r1.intf('r1-eth2').setIP('192.168.30.1/24')
    r1.intf('r1-eth2').setMAC('00:00:00:00:01:03')

    r1.intf('r1-eth3').setIP('192.168.40.1/24')
    r1.intf('r1-eth3').setMAC('00:00:00:00:01:04')

    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")


    # Add Controllers
    ctrl = net.addController( 'c1', controller=RemoteController, ip=ctl, port=6633)

    net.build()

    # Connect each switch to a different controller
    s1.start([ctrl])
    s2.start([ctrl])
    s3.start([ctrl])
    s4.start([ctrl])

    h1, h2, h3, h4, s1, s2, s3, s4 = net.getNodeByName('h1', 'h2', 'h3', 'h4', 's1', 's2', 's3', 's4')

    print "Testing network connectivity\n"
    net.pingAll()
    print "Dumping host connections\n"
    dumpNodeConnections(net.hosts)

    h1.cmd("ip route add default via 192.168.10.1")
    h2.cmd("ip route add default via 192.168.20.1")
    h3.cmd("ip route add default via 192.168.30.1")
    h4.cmd("ip route add default via 192.168.40.1")

    s1.cmdPrint('ovs-vsctl show')

    h1.cmd('/sbin/tc qdisc del dev h1-eth0 root')
    sleep(3)
    h1.cmd('ifconfig h1-eth0 txqueuelen 5000')
    r1.cmd('ifconfig r1-eth1 txqueuelen 5000')
    r1.cmd('ifconfig r1-eth2 txqueuelen 5000')
    r1.cmd('ifconfig r1-eth3 txqueuelen 5000')
    sleep(2)

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
           '/sbin/tc class add dev h1-eth0 parent 1: classid 1:1 htb rate 762kbit ceil 762kbit burst 762kb && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:11 htb rate 9.6kbit ceil 9.6kbit burst 10kb && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:12 htb rate 240kbit ceil 240kbit burst 240kb && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:13 htb rate 512kbit ceil 512kbit burst 512kb && '
           '/sbin/tc qdisc add dev h1-eth0 parent 1:11 handle 11: ets strict 2 quanta 900 600 priomap 3 3 2 1 0 1 1 1 1 1 1 1 1 1 1 1 && '
           '/sbin/tc qdisc add dev h1-eth0 parent 1:12 handle 12: ets strict 2 quanta 900 600 priomap 3 3 2 1 0 1 1 1 1 1 1 1 1 1 1 1 && '
           '/sbin/tc qdisc add dev h1-eth0 parent 1:13 handle 13: ets strict 2 quanta 900 600 priomap 3 3 2 1 0 1 1 1 1 1 1 1 1 1 1 1 && '
           '/sbin/tc qdisc add dev h1-eth0 parent 11:1 handle 111: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 11:2 handle 112: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 11:3 handle 113: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 11:4 handle 114: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 12:1 handle 121: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 12:2 handle 122: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 12:3 handle 123: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 12:4 handle 124: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 13:1 handle 131: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 13:2 handle 132: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 13:3 handle 133: netem limit 1000 delay 5ms && '
           '/sbin/tc qdisc add dev h1-eth0 parent 13:4 handle 134: netem limit 1000 delay 5ms && '
           '/sbin/tc filter add dev h1-eth0 parent 1:0 protocol ip prio 1 u32 match ip src 192.168.10.10 match ip protocol 17 0xff flowid 1:1 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.20.10 match ip protocol 17 0xff flowid 1:11 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.30.10 match ip protocol 17 0xff flowid 1:12 && '
           '/sbin/tc filter add dev h1-eth0 parent 1:1 protocol ip prio 1 u32 match ip dst 192.168.40.10 match ip protocol 17 0xff flowid 1:13'
           )


    ssh_to_ctrl_1 = paramiko.SSHClient()
    ssh_to_ctrl_1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_to_ctrl_1.connect(hostname=ctl, username='vagrant', password='vagrant', allow_agent=False, look_for_keys=False)
    stdin, stdout, stderr = ssh_to_ctrl_1.exec_command('python ~/sdn-tactical-network/rest_app/qos_app/qos_rest.py')
    print "STDOUT:\n%s\n\nSTDERR:\n%s\n" % (stdout.read(), stderr.read())
    CLI(net)
    sleep(3)
    makeTerm(h2, title='mgen receiver h2', cmd="mgen input receive_h2.mgn output receive_log_h2.txt")
    makeTerm(h3, title='mgen receiver h3', cmd="mgen input receive_h3.mgn output receive_log_h3.txt")
    makeTerm(h1, title='class statistics', cmd="watch -dc tc -s -d -j class show dev h1-eth0")
    makeTerm(h1, title='qdisc statistics', cmd="watch -dc tc -s -d qdisc show dev h1-eth0")
    makeTerm(h2, title='packet sniffer receiver h2', cmd="sudo python packet_sniffer_receiver_h2.py")
    makeTerm(h3, title='packet sniffer receiver h3', cmd="sudo python packet_sniffer_receiver_h3.py")
    makeTerm(h1, title='packet sniffer sender', cmd="sudo python packet_sniffer_sender.py")
    makeTerm(h1, title='queue stats server', cmd="python host_queue_socket_server.py")
    #makeTerm(h1, title='qdisc logger', cmd="python query_qdisc_log.py")

    sleep(1)

    r1.cmd('/sbin/tc qdisc add dev r1-eth1 root handle 1: htb default 1 && '
           '/sbin/tc class add dev r1-eth1 parent 1: classid 1:1 htb rate 9.6kbit ceil 9.6kbit burst 10kb && '
           '/sbin/tc filter add dev r1-eth1 parent 1: protocol ip prio 1 u32 match ip dst 192.168.20.10 match ip protocol 17 0xff flowid 1:1'
           )

    r1.cmd('/sbin/tc qdisc add dev r1-eth2 root handle 1: htb default 1 && '
           '/sbin/tc class add dev r1-eth2 parent 1: classid 1:1 htb rate 240kbit ceil 240kbit burst 240kb && '
           '/sbin/tc filter add dev r1-eth2 parent 1: protocol ip prio 1 u32 match ip dst 192.168.30.10 match ip protocol 17 0xff flowid 1:1'
           )

    #r1_s2_interface = r1.intf(intf='r1-eth1')
    #r1_s3_interface = r1.intf(intf='r1-eth2')

    # target_bw_r1_to_s2 = 0.0006  # 0.6 kbps => 0.0006 Mbit/s
    # target_bw_r1_to_s2 = 0.0012  # 1.2 kbps => 0.0012 Mbit/s
    # target_bw_r1_to_s2 = 0.0024  # 2.4 kbps => 0.0024 Mbit/s
    # target_bw_r1_to_s2 = 0.0048  # 4.8 kbps => 0.0048 Mbit/s
    # target_bw_r1_to_s2 = 0.0096  # 9.6 kbps => 0.0096 Mbit/s
    # target_bw_r1_to_s3 = 0.015  # 15 kbps => 0.015 Mbit/s
    # target_bw_r1_to_s3 = 0.03  # 30 kbps => 0.03 Mbit/s
    # target_bw_r1_to_s3 = 0.06  # 60 kbps => 0.06 Mbit/s
    # target_bw_r1_to_s3 = 0.12  # 120 kbps => 0.12 Mbit/s
    # target_bw_r1_to_s3 = 0.24  # 240 kbps => 0.24 Mbit/s
    # info("Setting BW Limit for Interface " + str(r1_s2_interface) + " to " + str(target_bw_r1_to_s2) + "\n")
    # info("Setting BW Limit for Interface " + str(r1_s3_interface) + " to " + str(target_bw_r1_to_s3) + "\n")
    # change the bandwidth of link to target bandwidth
    # s1_s2_interface.config(bw=target_bw_s1_to_s2, smooth_change=True)
    # sleep(1)
    # s1_s3_interface.config(bw=target_bw_s1_to_s3, smooth_change=True)
    sleep(5)
    makeTerm(h1, title='mgen sender to h2', cmd="mgen input send.mgn")
    #makeTerm(h1, title='mgen sender to h3', cmd="mgen input send_h3.mgn")
    sleep(1)

    CLI(net)
    net.stop()
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel('info')
    myNet()