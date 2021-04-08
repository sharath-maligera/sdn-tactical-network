from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.http import HttpPostClientTransport
from tinyrpc import RPCClient
import time
import sys

rpc_client = RPCClient(
    JSONRPCProtocol(),
    HttpPostClientTransport('http://192.168.1.100:8080/'))

remote_server = rpc_client.get_proxy()

def adapt_vhf_data_rate(data_rate=None):
    data = '{"table_id": 0, "priority": 100}'
    response = requests.get('http://192.168.1.101:8080/stats/flow/16', data=data)
    if response.status_code == 200:
        hard_timeout = data_response['16'][0]['hard_timeout']
        print 'Hard timeout value is {timeout}'.format(timeout=hard_timeout)
        data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": '+hard_timeout+', "priority": 100, ' \
               '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 11}]}'
        delete_response = requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)
        if delete_response.status_code == 200:
            timeout_set = True
            data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 120, "priority": 100, ' \
                   '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.3", "ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 5}]}'
            requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

def adapt_uhf_data_rate():
    pass

def adapt_sat_comm_data_rate():
    pass


try:
    vhf_data_rate = None
    uhf_data_rate = None
    sat_comm_data_rate = None
    while True:
        time.sleep(2)
        vhf_data_rate_json = remote_server.get_vhf_data_rate()
        vhf_data_rate = vhf_data_rate_json['vhf_rate']
        adapt_vhf_data_rate(data_rate=None)

        uhf_data_rate = remote_server.get_uhf_data_rate()
        sat_comm_data_rate = remote_server.get_sat_comm_data_rate()

        print("\n\n\nCurrent VHF data rate is: ", vhf_data_rate)
        print("\n\n\nCurrent UHF data rate is: ", uhf_data_rate)
        print("\n\n\nCurrent SatComm data rate is: ", sat_comm_data_rate)

except KeyboardInterrupt:
    sys.exit(1)



