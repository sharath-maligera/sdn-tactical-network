import requests
import pprint
import json

data = '"tcp:127.0.0.1:6633"'
response = requests.put('http://192.168.1.101:8080/v1.0/conf/switches/0000000000000010/ovsdb_addr', data=data)


# data = '{"port_name": "s1-eth2", "type": "linux-htb", "max_rate": "9600", "queues": [{"min_rate": "210"}, {"min_rate": "180"}, {"min_rate": "90"}, {"min_rate": "60"}, {"min_rate": "60"}]}'
# response_port_2 = requests.post('http://192.168.1.101:8080/qos/queue/0000000000000010', data=data)
#
# data = '{"port_name": "s1-eth3", "type": "linux-htb", "max_rate": "240000", "queues": [{"min_rate": "84000"}, {"min_rate": "72000"}, {"min_rate": "36000"}, {"min_rate": "24000"}, {"min_rate": "24000"}]}'
# response_port_3 = requests.post('http://192.168.1.101:8080/qos/queue/0000000000000010', data=data)
#
# data = '{"port_name": "s1-eth4", "type": "linux-htb", "max_rate": "512000", "queues": [{"min_rate": "179200"}, {"min_rate": "153600"}, {"min_rate": "76800"}, {"min_rate": "51200"}, {"min_rate": "51200"}]}'
# response_port_4 = requests.post('http://192.168.1.101:8080/qos/queue/0000000000000010', data=data)
# #
# # response_queue = requests.get('http://192.168.1.101:8080/qos/queue/0000000000000010')

###########################################################################################################################################
data = '{"dpid": 16, "flags": "KBPS", "meter_id": 1, "bands": [{"type": "DSCP_REMARK", "rate": 512, "burst_size": 512}]}'
response = requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 2, "bands": [{"type": "DSCP_REMARK", "rate": "256", "burst_size": 256}]}'
response = requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 3, "bands": [{"type": "DSCP_REMARK", "rate": 128, "burst_size": 128}]}'
response = requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 4, "bands": [{"type": "DSCP_REMARK", "rate": 64, "burst_size": 64}]}'
response = requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 5, "bands": [{"type": "DSCP_REMARK", "rate": 32, "burst_size": 240}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 6, "bands": [{"type": "DSCP_REMARK", "rate": 240, "burst_size": 240}]}'
response = requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 7, "bands": [{"type": "DSCP_REMARK", "rate": "120", "burst_size": 240}]}'
response = requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 8, "bands": [{"type": "DSCP_REMARK", "rate": 60, "burst_size": 240}]}'
response = requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 9, "bands": [{"type": "DSCP_REMARK", "rate": 30, "burst_size": 240}]}'
response = requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 10, "bands": [{"type": "DSCP_REMARK", "rate": 15, "burst_size": 240}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 11, "bands": [{"type": "DSCP_REMARK", "rate": 10, "burst_size": 10}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 12, "bands": [{"type": "DSCP_REMARK", "rate": 5, "burst_size": 10}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 13, "bands": [{"type": "DSCP_REMARK", "rate": 5, "burst_size": 10}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 14, "bands": [{"type": "DSCP_REMARK", "rate": 5, "burst_size": 10}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

data = '{"dpid": 16, "flags": "KBPS", "meter_id": 15, "bands": [{"type": "DSCP_REMARK", "rate": 5, "burst_size": 10}]}'
requests.post('http://192.168.1.101:8080/qos/meter/0000000000000010', data=data)

####################################################################################################################################################################

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 5}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 5}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 5}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 5}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.40.10", "ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 5}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

####################################################################################################################################################################

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 10}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 10}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 10}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 10}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.30.10", "ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 10}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

# data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 0, ' \
#        '"match":{}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
# requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)

####################################################################################################################################################################

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 15}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 15}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 15}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10","ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 15}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
       '"match":{"ipv4_src": "192.168.10.10", "ipv4_dst": "192.168.20.10", "ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}, {"type":"METER", "meter_id": 15}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

############################################################################################################################################################################
data = '{"dpid": 16, "table_id": 1, "idle_timeout": 0, "hard_timeout": 0, "priority": 1, ' \
       '"match":{"eth_dst": "01:00:00:00:01:00", "in_port":1}, "actions":[{"type":"OUTPUT", "port": 2}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 1, "idle_timeout": 0, "hard_timeout": 0, "priority": 1, ' \
       '"match":{"eth_dst": "01:00:00:00:02:00", "in_port":1}, "actions":[{"type":"OUTPUT", "port": 2}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 1, "idle_timeout": 0, "hard_timeout": 0, "priority": 1, ' \
       '"match":{"eth_dst": "01:00:00:00:03:00", "in_port":1}, "actions":[{"type":"OUTPUT", "port": 2}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 1, "idle_timeout": 0, "hard_timeout": 0, "priority": 1, ' \
       '"match":{"eth_dst": "01:00:00:00:04:00", "in_port":1}, "actions":[{"type":"OUTPUT", "port": 2}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 1, "idle_timeout": 0, "hard_timeout": 0, "priority": 1, ' \
       '"match":{"eth_dst": "00:00:00:00:01:01", "in_port":1}, "actions":[{"type":"OUTPUT", "port": 2}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 1, "idle_timeout": 0, "hard_timeout": 0, "priority": 1, ' \
       '"match":{"eth_dst": "00:00:00:00:01:02", "in_port":1}, "actions":[{"type":"OUTPUT", "port": 2}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 1, "idle_timeout": 0, "hard_timeout": 0, "priority": 1, ' \
       '"match":{"eth_dst": "00:00:00:00:01:03", "in_port":1}, "actions":[{"type":"OUTPUT", "port": 2}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

data = '{"dpid": 16, "table_id": 1, "idle_timeout": 0, "hard_timeout": 0, "priority": 1, ' \
       '"match":{"eth_dst": "00:00:00:00:01:04", "in_port":1}, "actions":[{"type":"OUTPUT", "port": 2}]}'
requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

#################################################################################################


