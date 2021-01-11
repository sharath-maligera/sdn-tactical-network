import requests
import pprint
import json

data = '"tcp:127.0.0.1:6633"'
response = requests.put('http://192.168.1.101:8080/v1.0/conf/switches/0000000000000010/ovsdb_addr', data=data)


data = '{"port_name": "s1-eth2", "type": "linux-htb", "max_rate": "1000000", "queues": [{"min_rate": "4800"}, {"min_rate": "4800"}, {"min_rate": "4800"}, {"min_rate": "4800"}]}'
requests.post('http://192.168.1.101:8080/qos/queue/0000000000000010', data=data)

# data = '{"match": {"ip_dscp":30}, "actions":{"queue": "0"}}'
# requests.post('http://localhost:8080/qos/rules/0000000000000010', data=data)
#
# data = '{"match": {"ip_dscp":22}, "actions":{"queue": "1"}}'
# requests.post('http://localhost:8080/qos/rules/0000000000000010', data=data)
#
# data = '{"match": {"ip_dscp":4}, "actions":{"queue": "2"}}'
# requests.post('http://localhost:8080/qos/rules/0000000000000010', data=data)
#
# data = '{"match": {"ip_dscp":0}, "actions":{"queue": "3"}}'
# requests.post('http://localhost:8080/qos/rules/0000000000000010', data=data)

response = requests.get('http://192.168.1.101:8080/qos/queue/0000000000000010')
pprint.pprint(response.json())

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 1, "bands": [{"type": "DROP", "rate": 10}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 2, "bands": [{"type": "DROP", "rate": 5}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 3, "bands": [{"type": "DROP", "rate": 3}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 4, "bands": [{"type": "DROP", "rate": 2}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ip_dscp": 30, "dl_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
#        '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 30, "ip_ecn": 0, "ip_proto": 1, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)
#
# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 99, ' \
#        '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 22, "ip_ecn": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)
#
# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 98, ' \
#        '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 14, "ip_ecn": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)
#
# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 97, ' \
#        '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 16, "ip_ecn": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)
#
# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 96, ' \
#        '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)
#
# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 95, ' \
#        '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 0, "ip_ecn": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 0, ' \
#        '"match":{}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# response = requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)

# "ip_dscp": 30
#  "ip_dscp": 22",
# "ip_dscp": 14,
# "ip_dscp": 4,
# "ip_dscp": 0,