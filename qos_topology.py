#!/usr/bin/python

import re
import os
from time import sleep
import json
from mininet.net import Mininet
from mininet.link import TCIntf
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from link import TCLink
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mn_wifi.cli import CLI
import pandas as pd
import paramiko


def myNet():

    ctl1='192.168.1.101'
    ctl2='192.168.1.102'
    bandwidth_9_6_kbps = 0.0768  # Mbit/s
    bandwidth_4_8_kbps = 0.0384  # Mbit/s
    bandwidth_2_4_kbps = 0.0192  # Mbit/s
    bandwidth_0_6_kbps = 0.0048  # Mbit/s
    bandwidth_240_kbps = 1.92    # Mbit/s
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
    net.addLink(s1, s2, bw=bandwidth_9_6_kbps)
    #net.addLink(s2, s3, )
    net.addLink(s1, s3, bw=bandwidth_240_kbps)

    # Add Controllers
    #ctrl_1 = net.addController( 'c0', controller=RemoteController, ip=ctl1, port=6633)

    ctrl_2 = net.addController( 'c1', controller=RemoteController, ip=ctl2, port=6633)

    net.build()

    # Connect each switch to a different controller
    s1.start([ctrl_2])
    s2.start([ctrl_2])
    s3.start([ctrl_2])

    #set the version of OpenFlow to be used in each router to version 1.3 and set to listen on port 6632 to access OVSDB
    s1.cmdPrint('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    s1.cmdPrint('ovs-vsctl set-manager "ptcp:6633"')
    s1.cmdPrint('ovs-vsctl --db=tcp:127.0.0.1:6633 set-controller s1 tcp:192.168.1.102:6633')

    s2.cmdPrint('ovs-vsctl set Bridge s2 protocols=OpenFlow13')
    s2.cmdPrint('ovs-vsctl set-manager "ptcp:6633"')

    s3.cmdPrint('ovs-vsctl set Bridge s3 protocols=OpenFlow13')
    s3.cmdPrint('ovs-vsctl set-manager "ptcp:6633"')
    #

    print "Testing network connectivity\n"
    net.pingAll()
    print "Dumping host connections\n"
    dumpNodeConnections(net.hosts)

    h1, h2, h3, s1, s2, s3 = net.getNodeByName('h1', 'h2', 'h3', 's1', 's2', 's3')

    s1.cmdPrint('ovs-vsctl show')

    h1.cmd('/sbin/tc qdisc del dev h1-eth0 root')
    sleep(3)
    h1.cmd('/sbin/tc qdisc add dev h1-eth0 root handle 1:0 htb default 20 && '
           '/sbin/tc class add dev h1-eth0 parent 1:0 classid 1:1 htb rate 250kbps ceil 250kbps && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:10 htb rate 240kbps ceil 240kbps && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:20 htb rate 10kbps ceil 10kbps && '
           '/sbin/tc filter add dev h1-eth0 protocol ip parent 1:0 prio 1 u32 match ip dst 192.168.0.3 flowid 1:10 && '
           '/sbin/tc filter add dev h1-eth0 protocol ip parent 1:0 prio 1 u32 match ip dst 192.168.0.2 flowid 1:20')
    sleep(3)
    h1.cmdPrint('/sbin/tc -s -d qdisc show dev h1-eth0')
    sleep(3)
    h1.cmdPrint('/sbin/tc -s -d class show dev h1-eth0')
    sleep(3)
    h2.cmd('/usr/bin/iperf3 -s -p 5001 -J > VHF_priority_1.json &')
    h2.cmd('/usr/bin/iperf3 -s -p 5002 -J > VHF_priority_2.json &')
    h2.cmd('/usr/bin/iperf3 -s -p 5003 -J > VHF_priority_3.json &')
    h2.cmd('/usr/bin/iperf3 -s -p 5004 -J > VHF_priority_4.json &')
    h2.cmd('/usr/bin/iperf3 -s -p 5005 -J > VHF_priority_5.json &')
    h2.cmd('/usr/bin/iperf3 -s -J > VHF_all_priority.json &')

    sleep(3)
    h3.cmd('/usr/bin/iperf3 -s -J > UHF_dst.json &')
    sleep(1)
    h1.cmd('/usr/bin/iperf3 -c 192.168.0.3 -u -t 150 -i 1 -J > UHF_qdisc.json &')
    h1.cmd('/usr/bin/iperf3 -c 192.168.0.2 -u -p 5001 -S 0x78 -t 150 -i 1 -J > msg_priority_1.json &')
    h1.cmd('/usr/bin/iperf3 -c 192.168.0.2 -u -p 5002 -S 0x58 -t 150 -i 1 -J > msg_priority_2.json &')
    h1.cmd('/usr/bin/iperf3 -c 192.168.0.2 -u -p 5003 -S 0x50 -t 150 -i 1 -J > msg_priority_3.json &')
    h1.cmd('/usr/bin/iperf3 -c 192.168.0.2 -u -p 5004 -S 0x38 -t 150 -i 1 -J > msg_priority_4.json &')
    h1.cmd('/usr/bin/iperf3 -c 192.168.0.2 -u -p 5005 -S 0x10 -t 150 -i 5 -J > msg_priority_5.json &')

    ssh_to_ctrl_2 = paramiko.SSHClient()
    ssh_to_ctrl_2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_to_ctrl_2.connect(hostname=ctl2, username='vagrant', password='vagrant', allow_agent=False, look_for_keys=False)
    stdin, stdout, stderr = ssh_to_ctrl_2.exec_command('python ~/sdn-tactical-network/rest_app/qos_app/qos_rest.py')
    print "STDOUT:\n%s\n\nSTDERR:\n%s\n" % (stdout.read(), stderr.read())

    stdin, stdout, stderr = ssh_to_ctrl_2.exec_command('curl -X GET http://192.168.1.102:8080/stats/meterconfig/16/1')
    print "STDOUT:\n%s\n\nSTDERR:\n%s\n" % (stdout.read(), stderr.read())

    stdin, stdout, stderr = ssh_to_ctrl_2.exec_command('curl -X GET http://192.168.1.102:8080/stats/meterconfig/16/2')
    print "STDOUT:\n%s\n\nSTDERR:\n%s\n" % (stdout.read(), stderr.read())

    stdin, stdout, stderr = ssh_to_ctrl_2.exec_command('curl -X GET http://192.168.1.102:8080/stats/meterconfig/16/3')
    print "STDOUT:\n%s\n\nSTDERR:\n%s\n" % (stdout.read(), stderr.read())

    stdin, stdout, stderr = ssh_to_ctrl_2.exec_command('curl -X GET http://192.168.1.102:8080/stats/meterconfig/16/4')
    print "STDOUT:\n%s\n\nSTDERR:\n%s\n" % (stdout.read(), stderr.read())

    CLI(net)
    sleep(30)
    s1_s2_intf = s1.intf(intf = 's1-eth2')

    print "Changing bandwidth to 4.8 kbps\n"
    s1_s2_intf.config(bw=bandwidth_4_8_kbps, smooth_change=True)
    #ssh_to_ctrl_2.exec_command('curl -X POST -d "{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, "match":{"nw_src": "192.168.0.1", "nw_dst": "192.168.0.2", "dl_type": 2048}, "actions":[{"type":"METER", "meter_id": 2}, {"type":"OUTPUT", "port": 2}]}" http://192.168.1.102:8080/stats/flowentry/modify_strict')

    sleep(30)
    CLI(net)

    print "\nChanging bandwidth to 2.4 kbps\n"
    s1_s2_intf.config(bw=bandwidth_2_4_kbps, smooth_change=True)

    sleep(30)
    CLI(net)

    print "\nChanging bandwidth to 0.6 kbps\n"
    s1_s2_intf.config(bw=bandwidth_0_6_kbps, smooth_change=True)

    sleep(30)
    CLI(net)

    print "\nChanging bandwidth to 9.6 kbps\n"
    s1_s2_intf.config(bw=bandwidth_9_6_kbps, smooth_change=True)
    sleep(30)
    CLI(net)


    h1.cmdPrint('/sbin/tc -s -d qdisc show dev h1-eth0')
    h1.cmdPrint('/sbin/tc -s -d class show dev h1-eth0')
    sleep(5)

    net.stop()
    sleep(5)
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel('info')
    myNet()