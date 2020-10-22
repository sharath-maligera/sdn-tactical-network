import requests
import json

from topology_1_constants import *

LOCALHOST = "http://localhost:8080"
# LOCALHOST = "http://10.0.2.15:8080"
CONF_SWITCH_URI = "/v1.0/conf/switches/"
QOS_QUEUES_URI = "/qos/queue/"
QOS_RULES_URI = "/qos/rules/"

OVSDB_ADDR = "tcp:127.0.0.1:6632"

OVS_LINK_TYPE = "linux-htb"

PORT_NAME_STR = "s{}-eth{}"

class RyuManager:

    def __init__(self, db):
        self.db = db

    def get_switch_id_for_dpid(self, dpid):
        return SWITCH_LOOKUP[str(dpid)]

    def add_single_switch_packet_checking_flow(self, switch, dst_ip):
        switch_id = self.get_switch_id_for_dpid(switch.dpid)
        data = {
            "match":{
                "nw_dst": str(dst_ip),
                "nw_proto": "UDP",
                "tp_dst": "5002"
            },
            "actions": {
                "queue": 1
            }
        }
        url = LOCALHOST + QOS_RULES_URI + switch_id
        return requests.post(url, data=json.dumps(data))

    def add_packet_checking_flow(self, switch):
        switch_id = self.get_switch_id_for_dpid(switch.dpid)
        data = {
            "match": {
                "ip_dscp": 26
            },
            "actions": {
                "queue": 1
            }
        }
        url = LOCALHOST + QOS_RULES_URI + switch_id
        return requests.post(url, data=json.dumps(data))

    def add_packet_marking_flow(self, switch, src, dst):
        switch_id = self.get_switch_id_for_dpid(switch.dpid)
        data = {
            "match": {
                "nw_dst": dst,
                "nw_src": src,
                "nw_proto": "UDP"
            },
            "actions": {
                "mark": 26,
                "queue": 1
            }
        }
        url = LOCALHOST + QOS_RULES_URI + switch_id
        return requests.post(url, data=json.dumps(data))

    def add_egress_port_queue(self, switch, port_no, queues, max_bw):
        print "Adding port queue"
        switch_id = self.get_switch_id_for_dpid(switch.dpid)
        print "Switch id: " + str(switch_id)
        port_name = self.get_port_name_for_port_no(port_no, switch.dpid)
      
        data = {
            "port_name": port_name,
            "type": OVS_LINK_TYPE,
            "max_rate": str(max_bw),
            "queues": queues
        }
        url = LOCALHOST + QOS_QUEUES_URI + switch_id
        return requests.post(url, data=json.dumps(data))

    def put_ovsdb_addr(self, dpid):
        switch_id = self.get_switch_id_for_dpid(dpid)
        url = LOCALHOST + CONF_SWITCH_URI + switch_id + "/ovsdb_addr"
        return requests.put(url, data=json.dumps(OVSDB_ADDR))

    def get_port_name_for_port_no(self, port_no, dpid):
        switch_no = str(SWITCH_NUMBER_TABLE[str(dpid)])
        return PORT_NAME_STR.format(switch_no, port_no)
