import requests
import pprint
import json

data = '"tcp:127.0.0.1:6633"'
response = requests.put('http://192.168.1.102:8080/v1.0/conf/switches/0000000000000010/ovsdb_addr', data=data)


data = '{"port_name": "s1-eth2", "type": "linux-htb", "max_rate": "1000000", "queues": [{"min_rate": "38400"}, {"min_rate": "19200"}, {"min_rate": "19200"}, {"min_rate": "4800"}]}'
requests.post('http://192.168.1.102:8080/qos/queue/0000000000000010', data=data)

data = '{"match": {"ip_dscp":120}, "actions":{"queue": "0"}}'
requests.post('http://localhost:8080/qos/rules/0000000000000010', data=data)

data = '{"match": {"ip_dscp":88}, "actions":{"queue": "1"}}'
requests.post('http://localhost:8080/qos/rules/0000000000000010', data=data)

data = '{"match": {"ip_dscp":80}, "actions":{"queue": "2"}}'
requests.post('http://localhost:8080/qos/rules/0000000000000010', data=data)

data = '{"match": {"ip_dscp":56}, "actions":{"queue": "3"}}'
requests.post('http://localhost:8080/qos/rules/0000000000000010', data=data)

response = requests.get('http://192.168.1.102:8080/qos/queue/0000000000000010')
pprint.pprint(response.json())

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 1, "bands": [{"type": "DROP", "rate": 10}]}'
requests.post('http://192.168.1.102:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 2, "bands": [{"type": "DROP", "rate": 5}]}'
requests.post('http://192.168.1.102:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 3, "bands": [{"type": "DROP", "rate": 3}]}'
requests.post('http://192.168.1.102:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 4, "bands": [{"type": "DROP", "rate": 2}]}'
requests.post('http://192.168.1.102:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"nw_src": "192.168.0.1", "nw_dst": "192.168.0.2", "dl_type": 2048}, "actions":[{"type":"METER", "meter_id": 1}, {"type":"OUTPUT", "port": 2}]}'
response = requests.post('http://192.168.1.102:8080/stats/flowentry/add', data=data)

