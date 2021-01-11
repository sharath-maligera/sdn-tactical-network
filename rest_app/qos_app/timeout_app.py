import requests
import pprint
import json
import time
while True:
    data = '{"table_id": 0, "priority": 96}'
    response = requests.get('http://192.168.1.101:8080/stats/flow/16', data=data)
    data_response = response.json()
    packet_count = data_response['16'][0]['packet_count']
    if packet_count > 0:
        data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 96, ' \
               '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 0, "ip_ecn": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
        response = requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)
        data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 120, "priority": 96, ' \
               '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 0, "ip_ecn": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
        response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)
        time.sleep(120)
        data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 120, "priority": 96, ' \
               '"match":{"ipv4_src": "192.168.0.1", "ipv4_dst": "192.168.0.2", "ip_dscp": 0, "ip_ecn": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[]}'
        response = requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)