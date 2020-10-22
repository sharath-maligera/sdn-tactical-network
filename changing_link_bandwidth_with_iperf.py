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


class StaticTopology(Topo):
    "Simple topo with 2 hosts"

    def __init__(self, init_bw):
        self.init_bw = init_bw
        Topo.__init__(self)

    def build(self):
        switch1 = self.addSwitch('s1', listenPort=6634, mac='00:00:00:00:00:01')
        switch2 = self.addSwitch('s2', listenPort=6634, mac='00:00:00:00:00:02')

        "iperf client host"
        host1 = self.addHost('h1', ip='192.168.1.1')
        self.addLink(host1, switch1, bw=self.init_bw)

        "iperf server host"
        host2 = self.addHost('h2', ip='192.168.1.2')
        self.addLink(host2, switch2, bw=self.init_bw)

        self.addLink(switch1, switch2, )


def plot_bandwidth_limit(trace, plotname, UDP):
    bw_list = []
    for line in open(trace, 'r'):
        if UDP:
            matchObj = re.match(r'(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)', line, re.M)
        else:
            matchObj = re.match(r'(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)', line, re.M)

        if matchObj:
            if UDP:
                bw = float(matchObj.group(9))   # KiloBytes / s
            else:
                bw = float(matchObj.group(9))   # KiloBytes / s
            bw_list.append(bw)
    plt.plot(bw_list, label='bandwidth')

    plt.legend()
    plt.title("Throughput Comparison")
    plt.ylabel("Throughput [KiloBytes / s]")
    plt.xlabel("Time")
    plt.savefig(plotname)
    #plt.show()

def ema(data, window):
    if len(data) < window + 2:
        return None
    alpha = 2 / float(window + 1)
    ema = []
    for i in range(0, window):
        ema.append(None)
    ema.append(data[window])
    for i in range(window+1, len(data)):
        ema.append(ema[i-1] + alpha*(data[i]-ema[i-1]))
    return ema

def plot_bandwidth_from_json(filename=None, plot=None):
    if None not in (filename,plot):
        with open(filename, 'r') as f:
            server_log_dict = json.load(f)
            debit = []
            intervals = server_log_dict['intervals']
            for i in intervals:
                debit.append(i['sum']['bits_per_second'])
            #df = pd.DataFrame(server_log_dict['intervals'][1])
            #print (df)
            conv_int = 8000
            bandwidth = [x / conv_int for x in debit]
            plt.plot(bandwidth, label='bandwidth')

            plt.axhline(10, color='g', label='Expected bandwidth')
            plt.plot(ema(bandwidth, 4), label='Bandwidth {} period moving average'.format(4))

            plt.legend()
            #plt.yscale('log')
            plt.title("Throughput Comparison for VHF host")
            plt.ylabel("Throughput [KiloBytes / s]")
            plt.xlabel("Time")
            plt.savefig(plot)
            plt.show()

        print "Completed"


def initialize_iperf(client=None, server=None, server_op_file_name=None, client_op_file_name=None, target_bw=None, UDP=True):
    if None not in (client, server, server_op_file_name, client_op_file_name, target_bw):
        info("Starting iperf Measurement\n")

        # stop old iperf server
        os.system('pkill -f \'iperf -s\'')
        #server.cmd('pkill -f \'iperf -s\'')
        sleep(1)
        # iPerf (iPerf v2) is a tool for active measurements of the maximum achievable bandwidth on IP networks.
        # Initiate iPerf server with -s option
        # -i : Sets the interval time in seconds between periodic bandwidth, jitter, and loss reports.
        #       If non-zero, a report is made every interval seconds of the bandwidth since the last report.
        #       If zero, no periodic reports are printed. Default is zero.
        # -y : Report as a Comma-Separated Values
        # -C : Set the congestion control algorithm
        # > : redirect standard output to file and close the file descriptor with & symbol
        if UDP:
            server.cmd('iperf3 -s -J > ' + server_op_file_name + ' &')
            #server.cmd('iperf -s -u -l 1248b -f K -w 65k -i 1 -e -t 120 -y C > ' + server_op_file_name + ' &')
        else:
            server.cmd('iperf3 -s -J > ' + server_op_file_name + ' &')
        sleep(1)

        # Initiate iPerf client with connection to server IP
        # -t : The time in seconds to transmit for. iPerf normally works by repeatedly sending an array of len bytes for time seconds. Default is 10 seconds.
        # -u : Telling iPerf to generate UDP packets
        # -l : The length of UDP data payload in bytes
        if UDP:
            client.cmd('iperf3 -c ' + str(server.IP()) + ' -u -t 100 -i 1 -J > '+ client_op_file_name +' &')
            #client.cmd('iperf -c ' + str(server.IP()) + ' -u -l 1248b -f K -b 160K -w 64k -t 120 -e --isochronous=1:20K,0 --ipg 5 -y C &')
        else:
            client.cmd('iperf3 -c ' + str(server.IP()) + ' -t 100 -i 1 -J > '+ client_op_file_name +' &')
        sleep(1)


def change_bw_limit(client=None, initial_bw=None, target_bw=None, smooth_change=True, interval=None):

    if None not in (client, initial_bw, target_bw, interval):
        client_interface = client.intf()

        info("Setting BW Limit for Interface " + str(client_interface) + " to " + str(target_bw) + "\n")
        # change the bandwidth of link to target bandwidth
        client_interface.config(bw=target_bw, smooth_change=smooth_change)
        sleep(interval)

        # reset bw to initial value
        info("Resetting BW Limit for Interface " + str(client_interface) + " to " + str(initial_bw) + "\n")
        client_interface.config(bw=initial_bw, smooth_change=smooth_change)
        sleep(interval)

        info("Setting BW Limit for Interface " + str(client_interface) + " to " + str(target_bw) + "\n")
        client_interface.config(bw=target_bw, smooth_change=smooth_change)
        sleep(interval)

        info("Resetting BW Limit for Interface " + str(client_interface) + " to " + str(initial_bw) + "\n")
        client_interface.config(bw=initial_bw, smooth_change=smooth_change)
        sleep(interval)



def main(initial_bw=None, target_bw=None, change_interval=None, server_op_file_name=None, client_op_file_name=None, plotname=None, UDP=True):
    if None not in (initial_bw, target_bw, change_interval, server_op_file_name, client_op_file_name, plotname):
        topology = StaticTopology(initial_bw)
        ctl1 = RemoteController("c0", ip='192.168.1.101', port=6633)
        ctl2 = RemoteController("c1", ip='192.168.1.102', port=6633)
        net = Mininet(topo=topology, link=TCLink, controller=RemoteController)
        s1, s2 = net.getNodeByName('s1', 's2')
        s1.start([ctl1])
        s2.start([ctl2])
        net.start()

        print "Testing network connectivity\n"
        net.pingAll()
        print "Dumping host connections\n"
        dumpNodeConnections(net.hosts)
        info("Testing bandwidth between h1 and h2\n")
        h1, h2 = net.getNodeByName('h1', 'h2')
        sleep(5)

        initialize_iperf(client=h1, server=h2, server_op_file_name=server_op_file_name, client_op_file_name=client_op_file_name, target_bw=target_bw, UDP=UDP)

        sleep(change_interval)
        change_bw_limit(client=h1, initial_bw=initial_bw, target_bw=target_bw, interval=change_interval)

        net.stop()
        sleep(5)
        os.system('sudo mn -c')
        #plot_bandwidth_limit(traces, plotname, UDP)
        #plot_bandwidth_limit_from_json(server_op_file_name=server_op_file_name, client_op_file_name=server_op_file_name)

def myNet():

    ctl1='192.168.1.101'
    ctl2='192.168.1.102'

    net = Mininet( topo=None, build=False)

    # Create nodes
    h1 = net.addHost( 'h1', mac='01:00:00:00:01:00', ip='192.168.0.1/24' )
    h2 = net.addHost( 'h2', mac='01:00:00:00:02:00', ip='192.168.0.2/24' )
    h3 = net.addHost( 'h3', mac='01:00:00:00:03:00', ip='192.168.0.3/24')

    # Create switches
    s1 = net.addSwitch( 's1', listenPort=6634, mac='00:00:00:00:00:01' )
    s2 = net.addSwitch( 's2', listenPort=6634, mac='00:00:00:00:00:02' )

    print "*** Creating links"
    net.addLink(h1, s1, )
    net.addLink(h2, s2, )
    net.addLink(h3, s2, )
    net.addLink(s1, s2, )

    # Add Controllers
    ctrl_1 = net.addController( 'c0', controller=RemoteController, ip=ctl1, port=6633)

    ctrl_2 = net.addController( 'c1', controller=RemoteController, ip=ctl2, port=6633)


    net.build()

    # Connect each switch to a different controller
    s1.start( [ctrl_1] )
    s2.start( [ctrl_1] )

    s1.cmdPrint('ovs-vsctl show')

    print "Testing network connectivity\n"
    net.pingAll()
    print "Dumping host connections\n"
    dumpNodeConnections(net.hosts)

    h1, h2, h3, s1, s2 = net.getNodeByName('h1', 'h2', 'h3', 's1', 's2')

    h1_intf = str(h1.intf())
    h2_intf = str(h2.intf())
    h3_intf = str(h3.intf())

    info("h1 interface: " + h1_intf +"\n")
    info("h2 interface: " + h2_intf +"\n")
    info("h3 interface: " + h3_intf +"\n")

    sleep(5)
    #h1.cmd('nohup sudo sh ~/wifi/mininet-wifi/sdn-tactical-network/shaping.sh > h1_shaping.log &')
    h1.cmd('/sbin/tc qdisc del dev h1-eth0 root')
    sleep(5)
    h1.cmd('/sbin/tc qdisc add dev h1-eth0 root handle 1:0 htb default 20 && '
           '/sbin/tc class add dev h1-eth0 parent 1:0 classid 1:1 htb rate 250kbps ceil 250kbps && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:10 htb rate 240kbps ceil 240kbps && '
           '/sbin/tc class add dev h1-eth0 parent 1:1 classid 1:20 htb rate 10kbps ceil 10kbps && '
           '/sbin/tc filter add dev h1-eth0 protocol ip parent 1:0 prio 1 u32 match ip dst 192.168.0.3 flowid 1:10 && '
           '/sbin/tc filter add dev h1-eth0 protocol ip parent 1:0 prio 1 u32 match ip dst 192.168.0.2 flowid 1:20')
    sleep(5)
    h1.cmdPrint('/sbin/tc -s -d qdisc show dev h1-eth0')
    sleep(5)
    h1.cmdPrint('/sbin/tc -s -d class show dev h1-eth0')
    sleep(5)
    h2.cmd('/usr/bin/iperf3 -s -J > VHF_dst.json &')
    sleep(1)
    h3.cmd('/usr/bin/iperf3 -s -J > UHF_dst.json &')
    sleep(1)
    h1.cmd('/usr/bin/iperf3 -c 192.168.0.2 -u -t 100 -i 1 -J > VHF_qdisc.json &')
    h1.cmd('/usr/bin/iperf3 -c 192.168.0.3 -u -t 100 -i 1 -J > UHF_qdisc.json &')
    sleep(105)
    sleep(5)
    h1.cmdPrint('/sbin/tc -s -d qdisc show dev h1-eth0')
    sleep(5)
    h1.cmdPrint('/sbin/tc -s -d class show dev h1-eth0')
    sleep(5)

    net.stop()
    sleep(5)
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel('info')
    target_bandwidth = 0.0384 # 4.8 kBps => 0.0384 Mbit/s
    initial_bandwidth =0.0768 # 9.6 kBps => 0.0768 Mbit/s
    change_interval = 20 # in seconds
    server_op_file_name = 'iperf_server_udp.json'
    client_op_file_name = 'iperf_client_udp.json'
    plotname = 'throughput_udp.png'
    UDP = True
    myNet()
    #plot_bandwidth_from_json(filename='VHF_dst.json', plot='VHF_dst_1.png')
    #plot_bandwidth_limit('iperf_server_udp.log', plotname, UDP)
    #main(initial_bw=initial_bandwidth, target_bw=target_bandwidth, change_interval=change_interval, server_op_file_name=server_op_file_name, client_op_file_name=client_op_file_name, plotname=plotname, UDP=UDP)