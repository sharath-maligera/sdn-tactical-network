import requests
import pprint
import json
import time
import logbook
import threading
from collections import defaultdict

data_log = logbook.Logger('REST App on Controller')


def define_timeout_for_flow_1():
    timeout_set = False
    while True:
        time.sleep(1)
        data = '{"table_id": 0, "priority": 100}'
        response = requests.get('http://192.168.1.101:8080/stats/flow/16', data=data)
        if response.status_code == 200 and not timeout_set:
            data_response = response.json()
            packet_count = data_response['16'][0]['packet_count']
            if packet_count > 0:
                data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 100, ' \
                       '"match":{"ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                delete_response = requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)
                if delete_response.status_code == 200:
                    timeout_set = True
                    data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 300, "priority": 100, ' \
                           '"match":{"ip_dscp": 30, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                    requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

def define_timeout_for_flow_2():
    timeout_set = False
    while True:
        time.sleep(1)
        data = '{"table_id": 0, "priority": 99}'
        response = requests.get('http://192.168.1.101:8080/stats/flow/16', data=data)
        if response.status_code == 200 and not timeout_set:
            data_response = response.json()
            packet_count = data_response['16'][0]['packet_count']
            if packet_count > 0:
                data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 99, ' \
                       '"match":{"ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                delete_response = requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)
                if delete_response.status_code == 200:
                    timeout_set = True
                    data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 150, "priority": 99, ' \
                           '"match":{"ip_dscp": 20, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                    requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

def define_timeout_for_flow_3():
    timeout_set = False
    while True:
        time.sleep(1)
        data = '{"table_id": 0, "priority": 98}'
        response = requests.get('http://192.168.1.101:8080/stats/flow/16', data=data)
        if response.status_code == 200 and not timeout_set:
            data_response = response.json()
            packet_count = data_response['16'][0]['packet_count']
            if packet_count > 0:
                data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 98, ' \
                       '"match":{"ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                delete_response = requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)
                if delete_response.status_code == 200:
                    timeout_set = True
                    data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 3600, "priority": 98, ' \
                           '"match":{"ip_dscp": 10, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                    requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

def define_timeout_for_flow_4():
    timeout_set = False
    while True:
        time.sleep(1)
        data = '{"table_id": 0, "priority": 97}'
        response = requests.get('http://192.168.1.101:8080/stats/flow/16', data=data)
        if response.status_code == 200 and not timeout_set:
            data_response = response.json()
            packet_count = data_response['16'][0]['packet_count']
            if packet_count > 0:
                data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 97, ' \
                       '"match":{"ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                delete_response = requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)
                if delete_response.status_code == 200:
                    timeout_set = True
                    data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 120, "priority": 97, ' \
                           '"match":{"ip_dscp": 1, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                    requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

def define_timeout_for_flow_5():
    timeout_set = False
    while True:
        time.sleep(1)
        data = '{"table_id": 0, "priority": 96}'
        response = requests.get('http://192.168.1.101:8080/stats/flow/16', data=data)
        if response.status_code == 200 and not timeout_set:
            data_response = response.json()
            packet_count = data_response['16'][0]['packet_count']
            if packet_count > 0:
                data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 0, "priority": 96, ' \
                       '"match":{"ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                delete_response = requests.post('http://192.168.1.101:8080/stats/flowentry/delete_strict', data=data)
                if delete_response.status_code == 200:
                    timeout_set = True
                    data = '{"dpid": 16, "table_id": 0, "idle_timeout": 0, "hard_timeout": 120, "priority": 96, ' \
                           '"match":{"ip_dscp": 0, "ip_proto": 17, "eth_type": 2048}, "actions":[{"type":"GOTO_TABLE", "table_id": 1}]}'
                    requests.post('http://192.168.1.101:8080/stats/flowentry/add', data=data)

if __name__ == '__main__':
    t1 = threading.Thread(name="define_timeout_for_flow_1", target=define_timeout_for_flow_1)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(name="define_timeout_for_flow_2", target=define_timeout_for_flow_2)
    t2.daemon = True
    t2.start()

    t3 = threading.Thread(name="define_timeout_for_flow_3", target=define_timeout_for_flow_3)
    t3.daemon = True
    t3.start()

    t4 = threading.Thread(name="define_timeout_for_flow_4", target=define_timeout_for_flow_4)
    t4.daemon = True
    t4.start()

    t5 = threading.Thread(name="define_timeout_for_flow_5", target=define_timeout_for_flow_5)
    t5.daemon = True
    t5.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

