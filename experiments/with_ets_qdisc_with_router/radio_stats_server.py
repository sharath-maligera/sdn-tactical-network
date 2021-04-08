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


@dispatcher.public
def get_vhf_data_rate():
    output = subprocess.check_output(['tc', '-s', '-j', 'class', 'show', 'dev', 'r1-eth1'])
    match = re.findall(re.escape('rate ') + "(.*)" + re.escape('ceil'), output)
    if match:
        vhf_date_rate = {'vhf_rate': None}
        digit = re.findall(r'\d+', match[0])
        if digit:
            vhf_date_rate['vhf_rate'] = int(digit[0])
            return vhf_date_rate
        else:
            pass
    else:
        pass

@dispatcher.public
def get_uhf_data_rate():
    output = subprocess.check_output(['tc', '-s', '-j', 'class', 'show', 'dev', 'r1-eth2'])
    match = re.findall(re.escape('rate ') + "(.*)" + re.escape('ceil'), output)
    if match:
        uhf_date_rate = {'uhf_rate': None}
        digit = re.findall(r'\d+', match[0])
        if digit:
            uhf_date_rate['uhf_rate'] = int(digit[0])
            return uhf_date_rate
        else:
            pass
    else:
        pass

@dispatcher.public
def get_sat_comm_data_rate():
    output = subprocess.check_output(['tc', '-s', '-j', 'class', 'show', 'dev', 'r1-eth3'])
    match = re.findall(re.escape('rate ') + "(.*)" + re.escape('ceil'), output)
    if match:
        satcomm_date_rate = {'satcomm_rate': None}
        digit = re.findall(r'\d+', match[0])
        if digit:
            satcomm_date_rate['satcomm_rate'] = int(digit[0])
            return satcomm_date_rate
        else:
            pass
    else:
        pass

# in the main greenlet, run our rpc_server
rpc_server.serve_forever()

