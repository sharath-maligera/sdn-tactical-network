import gevent
import gevent.pywsgi
import gevent.queue
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport
from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
import subprocess
import json

dispatcher = RPCDispatcher()
transport = WsgiServerTransport(queue_class=gevent.queue.Queue)

# start wsgi server as a background-greenlet
wsgi_server = gevent.pywsgi.WSGIServer(('192.168.1.100', 8080), transport.handle)
gevent.spawn(wsgi_server.serve_forever)

rpc_server = RPCServerGreenlets(transport, JSONRPCProtocol(), dispatcher)

@dispatcher.public
def get_r1_to_s2_stats():
    output = subprocess.check_output(['tc', '-s', '-j', 'qdisc', 'show', 'dev', 'r1-eth1'])
    return_value = json.dumps(json.loads(output))
    print 'return value send back: {return_value}'.format(return_value=return_value)
    return return_value

@dispatcher.public
def get_r1_to_s3_stats():
    output = subprocess.check_output(['tc', '-s', '-j', 'qdisc', 'show', 'dev', 'r1-eth2'])
    return_value = json.dumps(json.loads(output))
    print 'return value send back: {return_value}'.format(return_value=return_value)
    return return_value

# in the main greenlet, run our rpc_server
rpc_server.serve_forever()