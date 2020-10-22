#!/usr/bin/python

# autor: Ramon dos Reis Fontes
# book: Wireless Network Emulation with Mininet-WiFi
# github: https://github.com/ramonfontes/mn-wifi-book-en

import sys
from mn_wifi.node import UserAP, OVSBridgeAP
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import RemoteController
from mininet.link import TCLink

def topology():
    "Create a network."
    #net = Mininet_wifi(controller=Controller)
    net = Mininet_wifi(controller=RemoteController)
    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='20,40,0')
    sta2 = net.addStation('sta2', position='40,40,0')
    sta3 = net.addStation('sta3', position='60,40,0')
    sta4 = net.addStation('sta4', position='80,40,0')
    ap1 = net.addAccessPoint('ap1', ssid="ssid-ap1", mode="g", channel="5", failMode="standalone", position='30,70,0')
    ap2 = net.addAccessPoint('ap2', ssid="ssid-ap2", mode="g", channel="11", failMode="standalone", position='70,70,0')
    c1 = net.addController('c1', ip='192.168.1.101', port=6633)
    c2 = net.addController('c2', ip='192.168.1.102', port=6633)



    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating Stations\n")
    net.addLink(ap1, ap2)
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)
    net.addLink(sta3, ap2)
    net.addLink(sta4, ap2)

    net.plotGraph(max_x=100, max_y=100)
    info("*** Starting network\n")
    net.build()
    c1.start()
    c2.start()
    ap1.start([c1,c2])
    ap2.start([c1,c2])


    sta1.cmd("ip link add link sta1-wlan0 name sta1-wlan0.10 type vlan id 10")
    sta2.cmd("ip link add link sta2-wlan0 name sta2-wlan0.10 type vlan id 10")
    sta3.cmd("ip link add link sta3-wlan0 name sta3-wlan0.20 type vlan id 20")
    sta4.cmd("ip link add link sta4-wlan0 name sta4-wlan0.20 type vlan id 20")

    sta1.cmd("route del -net 10.0.0.0 netmask 255.0.0.0")
    sta2.cmd("route del -net 10.0.0.0 netmask 255.0.0.0")
    sta3.cmd("route del -net 10.0.0.0 netmask 255.0.0.0")
    sta4.cmd("route del -net 10.0.0.0 netmask 255.0.0.0")

    sta1.cmd("ifconfig sta1-wlan0.10 10.0.0.1")
    sta2.cmd("ifconfig sta2-wlan0.10 10.0.0.2")
    sta3.cmd("ifconfig sta3-wlan0.20 10.0.0.3")
    sta4.cmd("ifconfig sta4-wlan0.20 10.0.0.4")

    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,arp,in_port=1,dl_vlan=10,actions=mod_vlan_vid:20,output:2,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,icmp,in_port=1,dl_vlan=10,actions=mod_vlan_vid:20,output:2,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,udp,in_port=1,dl_vlan=10,actions=mod_vlan_vid:20,output:2,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,tcp,in_port=1,dl_vlan=10,actions=mod_vlan_vid:20,output:2,normal"')

    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,arp,in_port=2,dl_vlan=20,actions=mod_vlan_vid:10,output:1,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,icmp,in_port=2,dl_vlan=20,actions=mod_vlan_vid:10,output:1,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,udp,in_port=2,dl_vlan=20,actions=mod_vlan_vid:10,output:1,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,tcp,in_port=2,dl_vlan=20,actions=mod_vlan_vid:10,output:1,normal"')

    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,arp,in_port=1,dl_vlan=20,actions=mod_vlan_vid:10,output:2,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,icmp,in_port=1,dl_vlan=20,actions=mod_vlan_vid:10,output:2,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,udp,in_port=1,dl_vlan=20,actions=mod_vlan_vid:10,output:2,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,tcp,in_port=1,dl_vlan=20,actions=mod_vlan_vid:10,output:2,normal"')

    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,arp,in_port=2,dl_vlan=10,actions=mod_vlan_vid:20,output:1,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,icmp,in_port=2,dl_vlan=10,actions=mod_vlan_vid:20,output:1,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,udp,in_port=2,dl_vlan=10,actions=mod_vlan_vid:20,output:1,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,tcp,in_port=2,dl_vlan=10,actions=mod_vlan_vid:20,output:1,normal"')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
