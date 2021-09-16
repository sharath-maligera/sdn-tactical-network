import requests
import pprint
import json

data = '"tcp:127.0.0.1:6633"'
response = requests.put('http://192.168.1.101:8080/v1.0/conf/switches/0000000000000010/ovsdb_addr', data=data)


data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 4}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 4}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 4}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 4}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 4}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

####################################################################################################################################################################

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 9}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 9}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 9}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 9}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 9}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 0, ' \
#        '"match":{}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)

####################################################################################################################################################################

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 14}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 14}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 14}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10","ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 14}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 14}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/modify_strict', data=data)





