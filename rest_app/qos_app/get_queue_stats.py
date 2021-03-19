from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.http import HttpPostClientTransport
from tinyrpc import RPCClient
import time
import sys

rpc_client = RPCClient(
    JSONRPCProtocol(),
    HttpPostClientTransport('http://192.168.1.100:8080/'))

remote_server = rpc_client.get_proxy()

try:
    while True:
        time.sleep(2)
        r1_to_s2_stats = remote_server.get_r1_to_s2_stats()
        r1_to_s3_stats = remote_server.get_r1_to_s3_stats()
        print("\n\n\nR1 to S2 queue stats: ", r1_to_s2_stats)
        print("\n\n\nR1 to S3 queue stats", r1_to_s3_stats)
except KeyboardInterrupt:
    sys.exit(1)



