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
import pyshark
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import HANDSHAKE_DISPATCHER # for Exchange of HELLO message
from ryu.controller.handler import CONFIG_DISPATCHER # for Waiting to receive SwitchFeatures message
from ryu.controller.handler import MAIN_DISPATCHER # Normal status
from ryu.controller.handler import DEAD_DISPATCHER # Disconnection of connection
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4, udp
from ryu.topology import event, switches
from ryu import utils
import binascii
from ryu.lib.packet import bfd
from ryu.lib import hub
from ryu.lib.packet import stream_parser
import base64
"""
In order to implement 'debug_qos_simple_switch_13.py' as a Ryu application, 
ryu.base.app_manager.RyuApp is inherited in the SimpleSwitch13 class.
"""
class SimpleSwitch13(app_manager.RyuApp):
    # the OpenFlow 1.3 version is specified for OFP_VERSIONS
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # *args is a list of arbitrary arguments
    # **kwargs is a dictionary of arbitrary arguments
    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        # MAC address table mac_to_port is defined
        self.mac_to_port = {}
        self.datapath_list = {}
        self.sender_switch = 16
        self.capture_live_packets()
        # import mgen
        # self.mgen = mgen
        # self.set_mgen_receive_event = False
        # self.dpid = 16
        # self.tos = None
        # self.receiver = mgen.Controller("receiver")
        # self.monitor_thread = self._monitor_mgen

    """
    -   set_ev_cls specifies the event class supporting the received message and the state of the OpenFlow switch for the argument.
    -   After handshake with the OpenFlow switch is completed, the Table-miss flow entry is added to the flow table to get ready to receive the Packet-In message.
    -   Specifically, upon receiving the Switch Features(Features Reply) message, the Table-miss flow entry is added.
    """
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        In ev.msg, the instance of the OpenFlow message class corresponding to the event is stored. In this case, it is ryu.ofproto.ofproto_v1_3_parser.OFPSwitchFeatures.
        In msg.datapath, the instance of the ryu.controller.controller.Datapath class corresponding to the OpenFlow switch that issued this message is stored.
        """
        datapath = ev.msg.datapath

        # ofproto -    Indicates the ofproto module that supports the OpenFlow version in use. In the case of OpenFlow 1.3 format will be following module. ryu.ofproto.ofproto_v1_3
        ofproto = datapath.ofproto

        # ofproto_parser -  indicates the ofproto_parser module
        parser = datapath.ofproto_parser

        # An empty match is generated to match all packets. Match is expressed in the OFPMatch class.
        match = parser.OFPMatch()

        # - by specifying the output action to output to the controller port, in case the received packet does not match any of the normal flow entries, Packet-In is issued.
        # - an instance of the OUTPUT action class (OFPActionOutput) is generated to transfer to the controller port. The controller is specified as the output destination and OFPCML_NO_BUFFER is specified to max_len in
        #   order to send all packets to the controller.
        # When you specify 0 for max_len, binary data of packet is not attached to the Packet-In message. If OFPCML_NO_BUFFER is specified, the entire packet is attached to the Packet-In message without buffering the packet on the OpenFlow switch.
        actions = [parser.OFPActionOutput(port=ofproto.OFPP_CONTROLLER,
                                          max_len=ofproto.OFPCML_NO_BUFFER)]

        # install table-miss flow entry
        # The Table-miss flow entry has the lowest (0) priority and this entry matches all packets.
        table_id = 1
        self.add_flow(datapath, 0, match, actions, table_id)

    def add_flow(self, datapath, priority, match, actions, table_id, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, table_id=table_id, hard_timeout=0, command=ofproto.OFPFC_ADD)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, table_id=table_id, hard_timeout=0, command=ofproto.OFPFC_ADD)

        # send_msg(mod) - The main method of the Datapath class - used to send the OpenFlow message
        datapath.send_msg(mod)

    # implements an event handler corresponding to the message desired to be received.
    # The event class name is ryu.controller.ofp_event.EventOFP + <OpenFlow message name>. For example, in case of a Packet-In message, it becomes EventOFPPacketIn
    # Create the handler of the Packet-In event handler in order to accept received packets with an unknown destination.
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        # ev.msg.total_len - Data length of the received packets.
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        #actions = []
        # get the received port number from packet_in message.
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        self.logger.debug("Ethernet type is %s",eth.ethertype)
        if eth.ethertype == ether_types.ETH_TYPE_IP:
            ip = pkt.get_protocol(ipv4.ipv4)
            udp_pkt = pkt.get_protocol(udp.udp)
            if ip.tos != 0:
                payload_as_hex_str = ''.join('%02x' % byte for byte in bytearray(pkt.data))
                payload_as_ascii = payload_as_hex_str.decode('hex','strict')
                payload_as_hex_array = bytearray(pkt.data)
                # another = "".join(map(chr, payload_as_hex_array))
                # for payload_byte in payload_as_hex_array:
                #     s = binascii.unhexlify(payload_byte)
                #     print s
                len_of_array = len(payload_as_hex_array)
                # get the hexadecimal representation of the binary data
                #payload_as_hex = binascii.hexlify(bytearray(pkt.data))
                #text_string = bytearray.fromhex(payload_as_hex).decode('utf8', 'ignore')
                # payload_as_ascii = binascii.unhexlify(payload_as_hex)
                # bytes_object = base64.b16decode(payload_as_hex)
                # text_object = bytes_object.decode('latin1')

                pass
                # self.tos = ip.tos
                # for line in self.receiver:
                #     event = self.mgen.Event(line)
                #     print "Received MGEN event"
                #     print self.tos, event.rx_time, event.size
                # for line in self.receiver:
                #     print line
                # payload_as_str = utils.binary_str(pkt[3])
                # #bytes_object = bytes.fromhex(payload_as_str)
                # #ascii_string = bytes_object.decode("ASCII")
                # #print('data=%s' % payload_as_hex_array.strip().decode('utf-8', 'strict'))
                # #data = binascii.hexlify(bytearray(pkt[3])) # string format
                # data = binascii.hexlify(pkt[3])
                # ascii_string = bytearray.fromhex(data).decode('utf-8', 'ignore')
                # # bytes_object = bytes.fromhex(data)
                # # ascii_string = bytes_object.decode("ASCII")
                # # udp_payload = pkt[3]
                # # data = bfd.bfd.parser(udp_payload)
                # print('data=%s' % ascii_string)
                # messages = stream_parser.StreamParser.parse(pkt.data)
            # actions.append()
            src_ip = ip.src
            dst_ip = ip.dst
            protocol = ip.proto
            pass

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return


        # The destination MAC address and sender MAC address are obtained from the Ethernet header of the received packets using Ryu packet library.
        dst = eth.dst
        src = eth.src

        # In order to support connection with multiple OpenFlow switches, the MAC address table is so designed to be
        # managed for each OpenFlow switch. The data path ID is used to identify OpenFlow switches.
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # construct action list
        actions=[parser.OFPActionOutput(port=out_port), parser.OFPActionOutput(port=ofproto.OFPP_CONTROLLER, max_len=ofproto.OFPCML_NO_BUFFER)]
        # actions.append(parser.OFPActionOutput(out_port))
        # actions.append(parser.OFPActionOutput(ofproto.OFPP_CONTROLLER))
        # inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            # Unlike the Table-miss flow entry, set conditions for match this time. Implementation of the switching hub this
            # time, the receive port (in_port) and destination MAC address (eth_dst) have been specified.
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            # verify if we have a valid buffer_id, if yes avoid to send both flow_mod & packet_out
            # For the flow entry this time, the priority is specified to 1. The greater the value, the higher the priority, therefore,
            # the flow entry added here will be evaluated before the Table-miss flow entry.
            table_id = 1
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, table_id, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions, table_id)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            # Specifies the binary data of packets. This is used when OFP_NO_BUFFER is specified for buffer_id When the OpenFlow switch\'s buffer is used, this is omitted.
            data = msg.data
        # Regardless whether the destination MAC address is found from the MAC address table, at the end the Packet-Out
        # message is issued and received packets are transferred.
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    # @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, event):
        switch = event.switch
        ofp_parser = switch.dp.ofproto_parser
        if switch.dp.id not in self.datapath_list:
            self.datapath_list[switch.dp.id] = switch
        if switch.dp.id == self.sender_switch:
            pass

    def _monitor_mgen(self):
        self.receiver.send_event("listen udp 1024-65535")
        self.set_mgen_receive_event = True
        while True:
            for line in self.receiver:
                event = self.mgen.Event(line)
                print "Received MGEN event"
                print self.tos, event.rx_time, event.size

    def capture_live_packets(self):
            try:
                cap = pyshark.LiveCapture(interface='enp0s8',
                                          bpf_filter='host 192.168.0.1 and not arp', only_summaries=False,
                                          use_json=False)  # bpf_filter='host 192.168.0.2 and not arp',,capture_filter='host 192.168.0.2 and not arp'

                cap.set_debug()
                while True:
                    for packet in cap.sniff_continuously():
                        if 'ipv6' in packet:
                            pass
                        else:
                            try:
                                self.logger.info('Packet Just arrived:')
                                packet_sniff_time = packet.sniff_time.strftime('%b %d, %Y %H:%M:%S.%f')

                                packet_msg = '\nPacket Data:\t' \
                                             + 'packet_id: ' + str(packet.number) + '\n\t\t' \
                                             + 'packet_timestamp: ' + packet_sniff_time + '\n\t\t' \
                                             + 'source_ip: ' + str(packet.ip.src_host) + '\n\t\t' \
                                             + 'destination_ip: ' + str(packet.ip.dst_host) + '\n\t\t' \
                                             + 'protocol: ' + str(packet.transport_layer) + '\n\t\t' \
                                             + 'dsfield: ' + str(packet.ip.dsfield) + '\n\t\t' \
                                             + 'packet_length: ' + str(packet.length)
                                self.logger.info(packet_msg)
                            except Exception as exception:
                                pass

            except Exception as exception:
                pass