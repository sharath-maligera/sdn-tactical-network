import sys
import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange, dumpNodeConnections, dumpPorts, dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import OVSKernelSwitch, RemoteController

class Switches4HostsTopo(Topo):

    def __init__(self, **opts):
        super(Switches4HostsTopo, self).__init__(**opts)

        host0 = self.addHost('h0')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')

        switch0 = self.addSwitch('s0', dpid='0000000000000010')
        switch1 = self.addSwitch('s1', dpid='0000000000000020')
        switch2 = self.addSwitch('s2', dpid='0000000000000030')

        # 100 Mbps
        self.addLink(host0, switch0, bw=100) # s0.port_1: host0
        self.addLink(host1, switch0, bw=100) # s0.port_2: host1

        self.addLink(host2, switch1, bw=100) # s1.port_1: host0
        self.addLink(host3, switch1, bw=100) # s1.port_1: host0

        # 1 Mbps bandwidth
        self.addLink(switch0, switch2, bw=1) # s0.port_3: s2.port_1
        self.addLink(switch1, switch2, bw=1) # s1.port_3: s2.port_2

topos = {'2switch4host': (lambda: Switches4HostsTopo())}

LOCAL_IP = "127.0.0.1"

def add_controller(net, controller_ip=None):
    if not controller_ip:
        net.addController(name="c0", controller=RemoteController, ip=LOCAL_IP, port=6633)
    else:
        net.addController(name="c0", controller=RemoteController, ip=controller_ip, port=6633)

def start_network(controller_ip=None):
    topo = Switches4HostsTopo()
    net = Mininet(topo=None, switch=OVSKernelSwitch, link=TCLink, autoSetMacs=True)
    add_controller(net, controller_ip)
    net.topo = topo
    net.start()
    CLI(net)
    net.stop()
    os.system('sudo mn -c')

if __name__ == '__main__':
    setLogLevel('info')
    if len(sys.argv) > 1:
        controller_ip = str(sys.argv[1])
    else:
        controller_ip = None
    start_network(controller_ip)
