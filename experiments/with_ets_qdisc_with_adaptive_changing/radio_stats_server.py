import gevent
import gevent.pywsgi
import gevent.queue
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport
from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
import subprocess
import json
import radio_data_rate
import time
import re

dispatcher = RPCDispatcher()
transport = WsgiServerTransport(queue_class=gevent.queue.Queue)

# start wsgi server as a background-greenlet
wsgi_server = gevent.pywsgi.WSGIServer(('192.168.1.100', 8080), transport.handle)
gevent.spawn(wsgi_server.serve_forever)

rpc_server = RPCServerGreenlets(transport, JSONRPCProtocol(), dispatcher)

current_radio_rate_r1 = {'vhf': 9600, 'uhf': 240, 'sat_comm': 512}

def set_vhf_data_rate(interface=None, rate=None, parent=None, classid=None):
    if None not in (interface, rate, parent, classid):
        if rate == 9600:
            rate_in_kbps = '9.6kbps'
        elif rate == 4800:
            rate_in_kbps = '4.8kbps'
        elif rate == 2400:
            rate_in_kbps = '2.4kbps'
        elif rate == 1200:
            rate_in_kbps = '1.2kbps'
        else:
            rate_in_kbps = '0.6kbps'

        sudo_password = 'wifi'
        command_str = 'tc class change dev '+interface+' parent '+parent+' classid '+classid+' htb rate '+rate_in_kbps+''
        print("\n\ncommand string is {command_str}".format(command_str=command_str))
        command = command_str.split()
        print("Command is {command}".format(command=command))

        cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
        cmd2 = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)
        #output = cmd2.stdout.read.decode()
        #output = subprocess.check_output(['tc', 'class', 'change', interface, 'parent', parent, 'classid', classid, 'htb', 'rate', rate_in_kbps])
        #print("\n\n\nOutput on VHF rate change is {output}".format(output=output))

@dispatcher.public
def get_vhf_data_rate():
    global current_radio_rate_r1
    output = subprocess.check_output(['tc', '-s', '-j', 'class', 'show', 'dev', 'r1-eth1'])
    match = re.findall(re.escape('rate ') + "(.*)" + re.escape('ceil'), output)
    if match:
        vhf_date_rate = {'vhf_rate': None}
        digit = re.findall(r'\d+', match[0])
        if digit:
            data_rate = int(digit[0])
            if data_rate == current_radio_rate_r1.get('vhf'):
                print('VHF data rate is same')
            else:
                print('VHF data rate has changed so changing it to {rate}'.format(rate=data_rate))
                current_radio_rate_r1['vhf'] = data_rate
                set_vhf_data_rate(interface='s1-eth2', rate=data_rate, parent='1:1', classid='1:11')
            vhf_date_rate['vhf_rate'] = data_rate
            return vhf_date_rate
        else:
            pass
    else:
        pass

def set_uhf_data_rate(interface=None, rate=None, parent=None, classid=None):
    sudo_password = 'wifi'
    command_str = 'tc class change dev ' + interface + ' parent ' + parent + ' classid ' + classid + ' htb rate ' + str(rate) + ''
    print("\n\ncommand string is {command_str}".format(command_str=command_str))
    command = command_str.split()
    print("Command is {command}".format(command=command))

    cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)
    #output = cmd2.stdout.read.decode()
    #output = subprocess.check_output(['tc', 'class', 'change', interface, 'parent', parent, 'classid', classid, 'htb', 'rate', ''+rate+'kbps'])
    #print("\n\n\nOutput on UHF rate change is {output}".format(output=output))

@dispatcher.public
def get_uhf_data_rate():
    global current_radio_rate_r1
    output = subprocess.check_output(['tc', '-s', '-j', 'class', 'show', 'dev', 'r1-eth2'])
    match = re.findall(re.escape('rate ') + "(.*)" + re.escape('ceil'), output)
    if match:
        uhf_date_rate = {'uhf_rate': None}
        digit = re.findall(r'\d+', match[0])
        if digit:
            data_rate = int(digit[0])
            if data_rate == current_radio_rate_r1.get('uhf'):
                print('UHF data rate is same')
            else:
                print('UHF data rate has changed so changing it to {rate}'.format(rate=data_rate))
                current_radio_rate_r1['uhf'] = data_rate
                set_uhf_data_rate(interface='s1-eth2', rate=data_rate, parent='1:1', classid='1:12')
            uhf_date_rate['uhf_rate'] = data_rate
            return uhf_date_rate
        else:
            pass
    else:
        pass

def set_sat_comm_data_rate(interface=None, rate=None, parent=None, classid=None):
    sudo_password = 'wifi'
    command_str = 'tc class change dev ' + interface + ' parent ' + parent + ' classid ' + classid + ' htb rate ' + str(rate) + ''
    print("\n\ncommand string is {command_str}".format(command_str=command_str))
    command = command_str.split()
    print("Command is {command}".format(command=command))

    cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)
    #output = cmd2.stdout.read.decode()
    #output = subprocess.check_output(['tc', 'class', 'change', interface, 'parent', parent, 'classid', classid, 'htb', 'rate', ''+rate+'kbps'])
    #print("\n\n\nOutput on SatComm rate change is {output}".format(output=output))


@dispatcher.public
def get_sat_comm_data_rate():
    global current_radio_rate_r1
    output = subprocess.check_output(['tc', '-s', '-j', 'class', 'show', 'dev', 'r1-eth3'])
    match = re.findall(re.escape('rate ') + "(.*)" + re.escape('ceil'), output)
    if match:
        satcomm_date_rate = {'satcomm_rate': None}
        digit = re.findall(r'\d+', match[0])
        if digit:
            data_rate = int(digit[0])
            if data_rate == current_radio_rate_r1.get('sat_comm'):
                print('SatComm data rate is same')
            else:
                print('SatComm data rate has changed so changing it to {rate}'.format(rate=data_rate))
                current_radio_rate_r1['sat_comm'] = data_rate
                set_uhf_data_rate(interface='s1-eth2', rate=data_rate, parent='1:1', classid='1:13')
            satcomm_date_rate['satcomm_rate'] = data_rate
            return satcomm_date_rate
        else:
            pass
    else:
        pass

# in the main greenlet, run our rpc_server
rpc_server.serve_forever()

