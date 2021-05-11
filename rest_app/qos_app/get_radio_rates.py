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
    vhf_data_rate = None
    uhf_data_rate = None
    sat_comm_data_rate = None
    while True:
        time.sleep(2)
        vhf_data_rate_json = remote_server.get_vhf_data_rate()
        vhf_data_rate = vhf_data_rate_json['vhf_rate']

        uhf_data_rate_json = remote_server.get_uhf_data_rate()
        uhf_data_rate = uhf_data_rate_json['uhf_rate']

        sat_comm_data_rate_json = remote_server.get_sat_comm_data_rate()
        sat_comm_data_rate = sat_comm_data_rate_json['satcomm_rate']

        print("\n\n\nCurrent VHF data rate is: ", vhf_data_rate)
        print("\n\n\nCurrent UHF data rate is: ", uhf_data_rate)
        print("\n\n\nCurrent SatComm data rate is: ", sat_comm_data_rate)

except KeyboardInterrupt:
    sys.exit(1)



