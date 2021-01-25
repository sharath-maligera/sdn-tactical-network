import requests
import pprint
import json

data = '"tcp:127.0.0.1:6633"'
response = requests.put('http://192.168.1.101:8080/v1.0/conf/switches/0000000000000010/ovsdb_addr', data=data)


data = '{"port_name": "s1-eth2", "type": "linux-htb", "max_rate": "9600", "queues": [{"min_rate": "270"}, {"min_rate": "210"}, {"min_rate": "60"}, {"min_rate": "30"}, {"min_rate": "30"}]}'
requests.post('http://192.168.1.101:8080/qos/queue/0000000000000010', data=data)

data = '{"port_name": "s1-eth3", "type": "linux-htb", "max_rate": "240000", "queues": [{"min_rate": "6750"}, {"min_rate": "5250"}, {"min_rate": "1500"}, {"min_rate": "750"}, {"min_rate": "750"}]}'
requests.post('http://192.168.1.101:8080/qos/queue/0000000000000010', data=data)

response_queue = requests.get('http://192.168.1.101:8080/qos/queue/0000000000000010')
pprint.pprint(response_queue.json())



data = '{"dpid": 16, "flags": "KBPS", "meter_id": 1, "bands": [{"type": "DSCP_REMARK", "rate": 240, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 2, "bands": [{"type": "DSCP_REMARK", "rate": 120, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 3, "bands": [{"type": "DSCP_REMARK", "rate": 60, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 4, "bands": [{"type": "DSCP_REMARK", "rate": 30, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 5, "bands": [{"type": "DSCP_REMARK", "rate": 15, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 6, "bands": [{"type": "DSCP_REMARK", "rate": 10, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 7, "bands": [{"type": "DSCP_REMARK", "rate": 5, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 8, "bands": [{"type": "DSCP_REMARK", "rate": 3, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 9, "bands": [{"type": "DSCP_REMARK", "rate": 2, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 10, "bands": [{"type": "DSCP_REMARK", "rate": 1, "prec_level": "1"}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)



data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 99, ' \
       '"match":{"ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 98, ' \
       '"match":{"ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 97, ' \
       '"match":{"ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 96, ' \
       '"match":{"ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 0, ' \
       '"match":{}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)
