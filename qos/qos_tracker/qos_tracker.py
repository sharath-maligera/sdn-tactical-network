import requests
import json
import struct
import time
import threading
from models import *
from topology_1_constants import *
from topology import TopologyManager
from ryu import RyuManager
from dbconnection import DBConnection
from IPython import embed


class QoSTracker:

    def __init__(self):
        self.db = DBConnection('postgresql://postgres:postgres@192.168.1.102/controllerdb')
        self.topology_manager = TopologyManager(self.db)
        self.ryu = RyuManager(self.db)
        self._current_mpls_label = 0
        self._flows_added = 0

    def start(self):
        self.db.delete_reservations()
        self.db.delete_queues()
        # self.topology_manager.init_db()
        switches = self.db.get_all_switches()
        for switch in switches:
            ryu_response = self.ryu.put_ovsdb_addr(switch.dpid)
            print "++ Adding ovsdb_addr for dpid:" + str(switch.dpid) + " returned: " + str(ryu_response.text)

    def generate_mpls_label(self):
        self._current_mpls_label += 1
        return self._current_mpls_label

    def get_bw_for_src_dst(self, src, dst):
        src_map = SWITCH_MAP[str(src)]
        for port in src_map:
            if str(SWITCH_MAP[str(src)][port]["dpid"]) == str(dst):
                return SWITCH_MAP[str(src)][port]["bw"]

    def add_links(self, link_data):
        # TODO: Not great way to do this
        for link in link_data:
            bw = self.get_bw_for_src_dst(link.src.dpid, link.dst.dpid)
            self.db.add_link({
                "src_port": link.src.dpid,
                "dst_port": link.dst.dpid,
                "bw": bw
            })

    def add_switches(self, switch_data):
        for switch in switch_data:
            s = self.db.add_switch(switch, HOST_MAP[str(switch.dp.id)])

    def add_single_switch_rules(self, switch, out_port, reservation):
        queues = [{"max_rate": "500000"}, {"min_rate": str(reservation.bw)}]
        response = self.ryu.add_egress_port_queue(switch, out_port.port_no, queues, 1000000)
        print response.text
        respone = self.ryu.add_single_switch_packet_checking_flow(switch, reservation.dst)
        print response.text
        print "Added single switch_rules"

    def add_reservation(self, rsv):
        print "Adding reservation"
        reservation = self.db.add_reservation(rsv, self.generate_mpls_label())
        print "Added"
        in_port = self.db.get_port_for_id(reservation.in_port)
        in_switch = self.db.get_switch_for_port(in_port)

        last_port = self.db.get_port_for_id(reservation.out_port)
        last_switch = self.db.get_switch_for_port(last_port)

        path = self.topology_manager.get_route_to_host(rsv["dst"], in_switch)
        total_bw = self.topology_manager.get_max_bandwidth_for_path(path)
        print "Total Bandwidth: " + str(total_bw)

        available_bw = self.topology_manager.get_available_bandwidth_for_path(path)
        print "Available Bandwidth: " + str(available_bw)
        if not path:
            return
        if len(path) == 1:
            print "Correct path length"
            switch = path[0]
            print "Correct switch"
            self.add_single_switch_rules(switch, last_port, reservation)

        else:
            in_port_reservation = self.db.add_port_reservation(reservation.id, in_port.id)
            # TODO: this is stupid
            last_port_reservation = self.db.add_port_reservation(reservation.id, last_port.id)
            
            # Get the out port of the first switch and add the ingress rule
            first_switch_out_port_no = self.db.get_out_port_no_between_switches(in_switch, path[1], SWITCH_MAP)
            self.add_ingress_rules(in_switch, first_switch_out_port_no, reservation.src, reservation.dst, reservation.bw, total_bw)

            for i in range(1, len(path) - 1):
                in_port_no = self.db.get_in_port_no_between_switches_1(path[i-1], path[i], SWITCH_MAP)
                in_port = self.db.get_port_for_port_no(in_port_no, path[i].dpid)

                out_port_no = self.db.get_out_port_no_between_switches(path[i], path[i+1], SWITCH_MAP)
                self.add_switch_rules(path[i], out_port_no, reservation.src, reservation.dst, reservation.bw, total_bw)

            in_port_no = self.db.get_in_port_no_between_switches_1(path[-1], path[-2], SWITCH_MAP)
            in_port = self.db.get_port_for_port_no(in_port_no, path[i].dpid)
            out_port = self.db.get_port_for_id(reservation.out_port)
            self.add_switch_rules(path[-1], out_port.port_no, reservation.src, reservation.dst, reservation.bw, total_bw)

    def add_ingress_rules(self, switch, out_port_no, src_ip, dst_ip, bw, max_bw):
        # Add queues
        queues = [{"max_rate": str(max_bw)}, {"min_rate": str(bw)}]
        ryu_response = self.ryu.add_egress_port_queue(switch, out_port_no, queues, max_bw)
        print "++ Adding port queue for dpid:" + str(switch.dpid) + " returned: " + str(ryu_response.text)

        # Mark the packets on their way in
        ryu_response = self.ryu.add_packet_marking_flow(switch, src_ip, dst_ip)
        print "++ Adding packet marking flow for dpid:" + str(switch.dpid) + " returned: " + str(ryu_response.text)

    def add_switch_rules(self, switch, out_port_no, src_ip, dst_ip, bw, max_bw):
        # Add queues
        queues = [{"max_rate": str(max_bw)}, {"min_rate": str(bw)}]
        ryu_response = self.ryu.add_egress_port_queue(switch, out_port_no, queues, max_bw)
        print "++ Adding port queue for dpid:" + str(switch.dpid) + " returned: " + str(ryu_response.text)

        ryu_response = self.ryu.add_packet_checking_flow(switch)
        print "++ Adding packet checking flow for dpid:" + str(switch.dpid) + " returned: " + str(ryu_response.text)
