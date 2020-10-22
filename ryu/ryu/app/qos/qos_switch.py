# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import logging

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, HANDSHAKE_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, arp, ether_types, mpls
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from webob import Response

# Topology discovery
from ryu.topology import event
from ryu.topology.api import get_all_switch, get_all_link, get_switch

from ryu.app.qos.qos_tracker import QoSTracker, SWITCH_MAP, FLOW_TABLE_ID, PIR_TABLE_ID, CIR_TABLE_ID
from ryu.app.rest_qos import QoSController

simple_switch_instance_name = "simple_switch_api_app"

add_reservation_url = "/add_reservation"
start_qos_url = "/start_qos"


class QoSSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = { "wsgi": WSGIApplication }

    def __init__(self, *args, **kwargs):
        super(QoSSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.qos = QoSTracker(self)
        self._error_count = 0
        self.switches = {}
        wsgi = kwargs["wsgi"]
        wsgi.register(QoSController, {simple_switch_instance_name : self})


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # Add a flow to forward from table_id:0 to table_id:1
        match = parser.OFPMatch()
        inst = [parser.OFPInstructionGotoTable(CIR_TABLE_ID)]
        req = parser.OFPFlowMod(datapath=datapath, priority=2, match=match, instructions=inst, table_id=PIR_TABLE_ID)
        datapath.send_msg(req)

        match = parser.OFPMatch()
        inst = [parser.OFPInstructionGotoTable(FLOW_TABLE_ID)]
        req = parser.OFPFlowMod(datapath=datapath, priority=2, match=match, instructions=inst, table_id=CIR_TABLE_ID)
        datapath.send_msg(req)

        self.switches[datapath.id] = datapath

    def add_flow(self, datapath, priority, match, actions, table_id=FLOW_TABLE_ID, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        print "About to add flow: dpid:" + str(datapath.id) + " match:" + str(match) + " actions:" + str(actions)
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, table_id=table_id)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, table_id=table_id)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # # learn a mac address to avoid FLOOD next time.
        # self.mac_to_port[dpid][src] = in_port

        # if dst in self.mac_to_port[dpid] and dst != "ff:ff:ff:ff:ff:ff":
        #     return
        # else:
        #     out_port = ofproto.OFPP_FLOOD
        #     # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # mpls_packet = pkt.get_protocols(mpls.mpls)
        # if mpls_packet:
        #     if mpls_packet[0]:
        #         self.logger.info("packet in %s %s %s %s %s", dpid, src, dst, in_port, str(mpls_packet[0]))

        # actions = [parser.OFPActionOutput(out_port)]

        # data = None
        # if msg.buffer_id == ofproto.OFP_NO_BUFFER:
        #     data = msg.data

        # out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
        #                           in_port=in_port, actions=actions, data=data)
        # datapath.send_msg(out)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        mpls_packet = pkt.get_protocols(mpls.mpls)
        if mpls_packet:
            if mpls_packet[0]:
                self.logger.info("packet in %s %s %s %s %s", dpid, src, dst, in_port, str(mpls_packet[0]))


        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                print "About to add flow: dpid:" + str(datapath.id) + " match:" + str(match) + " actions:" + str(actions)
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions, table_id=2)
                self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_all_switch(self)
        self.qos.add_switches(switch_list)

        links_list = get_all_link(self)
        self.qos.add_links(links_list)


    @set_ev_cls(ofp_event.EventOFPErrorMsg,
        [HANDSHAKE_DISPATCHER, CONFIG_DISPATCHER, MAIN_DISPATCHER])
    def _handle_reply(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        self._error_count+=1
        print "***** ERROR - TYPE:" + str(msg.type) + " CODE:" + str(msg.code) + "DPID:" + str(datapath.id) + " COUNT:" + str(self._error_count)


# class QoSController(ControllerBase):

#     def __init__(self, req, link, data, **config):
#         super(QoSController, self).__init__(req, link, data, **config)
#         self.simple_switch_app = data[simple_switch_instance_name]


#     @route("start_qos", start_qos_url, methods=["POST"])
#     def start_qos(self, req, **kwargs):
#         simple_switch = self.simple_switch_app
#         simple_switch.qos.start()


#     @route("add_reservation", add_reservation_url, methods=["POST"])
#     def list_mac_table(self, req, **kwargs):
#         data = req.json
#         simple_switch = self.simple_switch_app
#         request_data = {
#             "src": data["src"],
#             "dst": data["dst"],
#             "bw": data["bw"]
#         }

#         simple_switch.qos.add_reservation(request_data)
#         body = json.dumps({"mac_table": "hi"})
#         return Response(content_type="application/json", body=body)

