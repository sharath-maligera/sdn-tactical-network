from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import UserAP, OVSBridgeAP
from mininet.node import RemoteController
from mn_wifi.link import wmediumd, WifiDirectLink
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.link import TCLink
from time import sleep
import os
from mininet.term import makeTerm
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost, Host, Node

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
        else:
            server.cmd('iperf3 -s -J > ' + server_op_file_name + ' &')
        sleep(1)

        # Initiate iPerf client with connection to server IP
        # -t : The time in seconds to transmit for. iPerf normally works by repeatedly sending an array of len bytes for time seconds. Default is 10 seconds.
        # -u : Telling iPerf to generate UDP packets
        # -l : The length of UDP data payload in bytes
        if UDP:
            client.cmd('iperf3 -c ' + str(server.IP()) + ' -u -t 100 -i 1 -J > '+ client_op_file_name +' &')
        else:
            client.cmd('iperf3 -c ' + str(server.IP()) + ' -t 100 -i 1 -J > '+ client_op_file_name +' &')
        sleep(1)


def plot_bandwidth_limit(traces, plotname, UDP):
    for trace in traces:
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



def multiControllerNet(initial_bw=None, target_bw=None, change_interval=None, server_op_file_name=None,
                       client_op_file_name=None, plotname=None, UDP=True):
    "Create a network."
    net = Mininet_wifi(controller=RemoteController, accessPoint=OVSBridgeAP)

    info("*** Creating Stations\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1', position='20,10,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:04', ip='10.0.0.4', position='30,10,0')

    info("*** Creating Access Points\n")
    ap1 = net.addAccessPoint('ap1', ssid="vhf_network_1", mode="g", channel="1", failMode="standalone", position='20,20,0')
    ap2 = net.addAccessPoint('ap2', ssid="vhf_network_2", mode="g", channel="6", failMode="standalone", position='30,20,0')

    info("*** Creating multiple controllers\n")
    c1 = net.addController('c1', ip='192.168.1.101', port=6633)
    #c2 = net.addController('c2', ip='192.168.1.102', port=6633)


    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    #net.addLink(sta1, ap1, cls=TCLink)
    net.addLink(sta1, ap1, cls=wmediumd)
    net.addLink(ap1, ap2, cls=TCLink)
    net.addLink(sta2, ap2, cls=wmediumd)

    net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    c1.start()
    #c2.start()
    ap1.start([c1])
    ap2.start([c1])

    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,arp,in_port=1, actions=output:2,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,icmp,in_port=1, actions=output:2,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,udp,in_port=1, actions=output:2,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,tcp,in_port=1, actions=output:2,normal"')

    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,arp,in_port=2, actions=output:1,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,icmp,in_port=2, actions=output:1,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,udp,in_port=2, actions=output:1,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=100,tcp,in_port=2, actions=output:1,normal"')

    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,arp,in_port=1, actions=output:2,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,icmp,in_port=1, actions=output:2,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,udp,in_port=1, actions=output:2,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,tcp,in_port=1, actions=output:2,normal"')

    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,arp,in_port=2, actions=output:1,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,arp,in_port=2, actions=output:1,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,arp,in_port=2, actions=output:1,normal"')
    ap2.cmd('ovs-ofctl add-flow ap2 "priority=100,arp,in_port=2, actions=output:1,normal"')

    net.startTerms()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Testing network connectivity\n")
    sleep(5)
    sta1_ip = sta1.params['ip']
    sta2_ip = sta2.params['ip']
    info("Station 1 IP: "+sta1_ip)
    info("Station 2 IP: "+sta2_ip)

    makeTerm(sta1, cmd="ping 10.0.0.1 -c 2 & sleep 10")
    makeTerm(sta2, cmd="ping 10.0.0.2 -c 2 & sleep 10")
    sleep(20)

    initialize_iperf(client=sta1, server=sta2, server_op_file_name=server_op_file_name,
                     client_op_file_name=client_op_file_name, target_bw=target_bw, UDP=UDP)

    sleep(change_interval)
    change_bw_limit(client=sta1, initial_bw=initial_bw, target_bw=target_bw, interval=change_interval)

    info("*** Stopping network\n")
    net.stop()
    sleep(5)
    os.system('sudo mn -c')



if __name__ == '__main__':
    setLogLevel('info')
    target_bandwidth = 0.0384  # 4.8 kBps => 0.0384 Mbit/s
    initial_bandwidth = 0.0768  # 9.6 kBps => 0.0768 Mbit/s
    change_interval = 20  # in seconds
    server_op_file_name = 'iperf_server_udp.json'
    client_op_file_name = 'iperf_client_udp.json'
    plotname = 'throughput_udp.png'
    UDP = True
    multiControllerNet(initial_bw=initial_bandwidth, target_bw=target_bandwidth, change_interval=change_interval,
                       server_op_file_name=server_op_file_name, client_op_file_name=client_op_file_name, plotname=plotname, UDP=UDP)
