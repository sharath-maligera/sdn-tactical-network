from models import *

from sqlalchemy import create_engine
from sqlalchemy.sql import exists
from models import Base
from sqlalchemy.orm import sessionmaker


class DBConnection:

    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.session = Session()

    def add_queue(self, port, queue_id, max_rate=None, min_rate=None):
        exist = self.session.query(exists()
                    .where(QoSQueue.port==port.id)).scalar()
        if not exist:
            queue = QoSQueue(port=port.id, max_rate=max_rate, min_rate=min_rate,
                queue_id=queue_id)
            return self.add_record(queue)
        else:
            return self.session.query(QoSQueue) \
                .filter(QoSQueue.port==port.id).first()

    def get_all_queues(self):
        return self.session.query(QoSQueue).all()

    def add_link(self, link_data):
        exist = self.session.query(exists()
                    .where(QoSLink.src == link_data["src_port"])
                    .where(QoSLink.dst == link_data["dst_port"])).scalar()
        if not exist:
            link = QoSLink(src=link_data["src_port"],
                           dst=link_data["dst_port"],
                           bandwidth=link_data["bw"])
            return self.add_record(link)
        else:
            return self.session.query(QoSLink) \
                .filter(QoSLink.src == link_data["src_port"] and
                    QoSLink.dst == link_data["dst_port"]).first()

    def add_port(self, port):
        exist = self.session.query(exists()
                    .where(QoSPort.switch == port.dpid)
                    .where(QoSPort.port_no == port.port_no)).scalar()
        if not exist:
            port = QoSPort(switch=port.dpid, port_no=port.port_no)
            return self.add_record(port)
        else:
            return self.session.query(QoSPort) \
                .filter(QoSPort.switch == port.dpid and
                    QoSPort.port_no == port.port_no).first()

    def add_host(self, host_data, port_id):
        exist = self.session.query(
            exists().where(QoSHost.mac == host_data["mac"])).scalar()
        if not exist:
            host = QoSHost(
                mac=host_data["mac"], ip=host_data["ip"], port=port_id)
            return self.add_record(host)
        else:
            return self.session.query(QoSHost.mac == host_data["mac"]).first()

    def add_switch(self, switch, host_data):
        exist = self.session.query(
            exists().where(QoSSwitch.dpid == switch.dp.id)).scalar()
        if not exist:
            qos_switch = QoSSwitch(dpid=switch.dp.id)
            for port in switch.ports:
                port = self.add_port(port)
                if int(port.port_no) in host_data:
                    self.add_host(
                        host_data[port.port_no],
                        port.id
                    )
            return self.add_record(qos_switch)
        else:
            return self.session.query(QoSSwitch) \
                .filter(QoSSwitch.dpid == switch.dp.id).first()

    def add_switch_1(self, dpid, host_data):
        exist = self.session.query(
            exists().where(QoSSwitch.dpid == dpid)).scalar()
        if not exist:
            qos_switch = QoSSwitch(dpid=dpid)
            for port_no in host_data[dpid]:
                port = self.add_port_1(port_no, dpid)
                if int(port.port_no) in host_data[dpid]:
                    self.add_host(
                        host_data[dpid][port.port_no],
                        port.id
                    )
            return self.add_record(qos_switch)
        else:
            return self.session.query(QoSSwitch) \
                .filter(QoSSwitch.dpid == switch.dp.id).first()


    def add_port_1(self, port_no, dpid):
        exist = self.session.query(exists()
                    .where(QoSPort.switch == dpid)
                    .where(QoSPort.port_no == port_no)).scalar()
        if not exist:
            port = QoSPort(switch=dpid, port_no=port_no)
            return self.add_record(port)
        else:
            return self.session.query(QoSPort) \
                .filter(QoSPort.switch == port.dpid and
                    QoSPort.port_no == port.port_no).first()

    def add_reservation(self, rsv, mpls_label):
        """
        rsv: dict containing reservation info
        """
        exist = self.session.query(exists()
                    .where(QoSReservation.src == rsv["src"])
                    .where(QoSReservation.dst == rsv["dst"])).scalar()
        if not exist:
            in_switch = self.get_switch_for_ip(rsv["src"])
            in_port = self.get_port_for_ip(rsv["src"])
            out_switch = self.get_switch_for_ip(rsv["dst"])
            out_port = self.get_port_for_ip(rsv["dst"])
            reservation = QoSReservation(
                src=rsv["src"], dst=rsv["dst"], bw=rsv["bw"], mpls_label=mpls_label,
                in_port=in_port.id, out_port=out_port.id)
            return self.add_record(reservation)
        else:
            return self.session.query(QoSReservation) \
                .filter(QoSReservation.src == rsv["src"]) \
                .filter(QoSReservation.dst == rsv["dst"]).first()

    def add_port_reservation(self, reservation, port):
        """
        prsv: dict containing port reservation info
        """
        exist = self.session.query(exists()
                    .where(QoSPortReservation.reservation == reservation)
                    .where(QoSPortReservation.port == port)).scalar()
        if not exist:
            p_reservation = QoSPortReservation(
                port=port, reservation=reservation)
            return self.add_record(p_reservation)

    def get_all_links(self):
        return self.session.query(QoSLink).all()

    def get_all_switches(self):
        return self.session.query(QoSSwitch).all()

    def get_all_ports(self):
        return self.session.query(QoSPort).all()

    def get_all_hosts(self):
        return self.session.query(QoSHost).all()

    def get_all_reservations(self):
        return self.session.query(QoSReservation).all()

    def get_all_port_reservations(self):
        return self.session.query(QoSPortReservation).all()

    def get_port_for_id(self, port_id):
        return self.session.query(QoSPort).filter(QoSPort.id==port_id).first()

    def get_out_port_no_between_switches(self, src, dst, switch_map):
        port_no = None
        for port in switch_map[str(src.dpid)]:
            if switch_map[str(src.dpid)][port]["dpid"] == str(dst.dpid):
                port_no = port
        return port_no

    def get_in_port_no_between_switches_1(self, src, dst, switch_map):
        port_no = None
        for port in switch_map[str(dst.dpid)]:
            if switch_map[str(dst.dpid)][port]["dpid"] == str(src.dpid):
                port_no = port
        return port_no

    def get_in_port_no_between_switches(self, src, dst, switch_map):
        port_no = None
        for port in switch_map[str(dst.dpid)]:
            if switch_map[str(dst.dpid)][port]["dpid"] == str(src.dpid):
                port_no = port
        return port_no

    def get_port_reservations_for_reservation(self, reservation):
        return self.session.query(QoSPortReservation) \
            .filter(QoSPortReservation.reservation == reservation)

    def get_switches_for_reservation(self, reservation):
        port_reservations = self.get_port_reservations_for_reservation(
            reservation)
        switches = []
        for p_reserve in port_reservations:
            port = p_reserve.port
            switches.append(self.get_switch_for_port(port))
        return switches

    def get_port_reservations_for_link(self, link, switch_map):
        switch_1 = self.get_switch_for_dpid(link.src)
        switch_2 = self.get_switch_for_dpid(link.dst)

        in_port_no = self.get_in_port_no_between_switches(switch_1, switch_2, switch_map)
        out_port_no = self.get_out_port_no_between_switches(switch_1, switch_2, switch_map)

        in_port = self.get_port_for_port_no(in_port_no, switch_2.dpid)
        out_port = self.get_port_for_port_no(out_port_no, switch_1.dpid)

        # port = self.get_port_for_id(link.src)
        reservations = self.get_port_reservations_for_port(in_port)
        reservations_2 = self.get_port_reservations_for_port(out_port)
        return reservations + reservations_2
        # if reservations is None:
        #     reservations = self.get_port_reservations_for_port(out_port)
        # else:
        #     reservations_2 = self.get_port_reservations_for_port(out_port)
        #     if reservations_2:
        #         return res
        # if not reservations:
        #     return None
        # return reservations


    def get_switch_for_ip(self, ip):
        host = self.session.query(QoSHost) \
            .filter(QoSHost.ip == ip).first()
        if not host:
            return None
        port = self.session.query(QoSPort) \
            .filter(QoSPort.id == host.port).first()
        return self.get_switch_for_port(port)

    def get_port_reservations_for_port(self, port):
        return self.session.query(QoSPortReservation) \
            .filter(QoSPortReservation.port==port.id).all()

    def get_ports_for_switch(self, dpid):
        return self.session.query(QoSPort) \
            .filter(QoSPort.switch == dpid).all()

    def get_host_for_ip(self, ip):
        return self.session.query(QoSHost).filter(QoSHost.ip == ip).first()

    def get_port_for_ip(self, ip):
        host = self.get_host_for_ip(ip)
        return self.get_port_for_id(host.port)

    def get_port_for_host(self, host):
        return self.session.query(QoSPort) \
            .filter(QoSPort.id == host.port).first()

    def get_ports_for_link(self, link):
        return self.session.query(QoSPort).filter(QoSPort.link == link).first()

    def get_switch_for_port(self, port):
        return self.session.query(QoSSwitch) \
            .filter(QoSSwitch.dpid == port.switch).first()

    def get_reservation_for_src_dst(self, src, dst):
        return self.session.query(QoSReservation) \
            .filter(QoSReservation.src == src and QoSReservation.dst == dst) \
            .first()

    def get_reservation_for_id(self, res_id):
        return self.session.query(QoSReservation) \
            .filter(QoSReservation.id == res_id).first()

    def get_switch_for_dpid(self, dpid):
        return self.session.query(QoSSwitch).filter(QoSSwitch.dpid == dpid).first()

    def get_port_for_port_no(self, port_no, dpid):
        return self.session.query(QoSPort) \
            .filter(QoSPort.switch == dpid and QoSPort.port_no == port_no) \
            .first()

    def get_switch_neighbours(self, dpid, exclude=None):
        # TODO: may not work. prob need to join these for performance later.
        links = self.session.query(QoSLink).filter(QoSLink.src == dpid).all()
        switches = []
        for link in links:
            switch = self.session.query(QoSSwitch) \
                        .filter(QoSSwitch.dpid == link.dst).first()
            if switch:
                if not exclude:
                    switches.append(switch)
                else:
                    if switch.dpid != exclude.dpid:
                        switches.append(switch)
        return switches

    def get_hosts_for_switch(self, dpid):
        ports = self.get_ports_for_switch(dpid)
        hosts = []
        for port in ports:
            host = self.session.query(QoSHost) \
                        .filter(QoSHost.port == port.id).first()
            if host:
                hosts.append(host)
        return hosts

    def get_link_for_ports(self, src, dst):
        src = self.get_switch_for_port(src)
        dst = self.get_switch_for_port(dst)
        link = self.session.query(QoSLink).filter(QoSLink.src==src.dpid and QoSLink.dst==dst.dpid).first()
        if not link:
            return None
        return link

    def get_link_between_switches(self, switch_1, switch_2):
        ports_1 = self.get_ports_for_switch(switch_1.dpid)
        ports_2 = self.get_ports_for_switch(switch_2.dpid)

        for p1 in ports_1:
            for p2 in ports_2:
                link = self.get_link_for_ports(p1, p2)
                if link:
                    return link
                else:
                    link = self.get_link_for_ports(p2, p1)
                    if link:
                        return link
        return None

    def get_non_neighbouring_hosts(self, dpid):
        ports = self.get_ports_for_switch(dpid)
        hosts = self.get_all_hosts()

    def update_reservation(self, res_id, new_bw):
        res = self.get_reservation_for_id(res_id)
        if not res:
            return None
        res.bw = new_bw
        self.session.commit()
        return res

    def delete_reservations(self):
        port_reservations = self.get_all_port_reservations()
        for p in port_reservations:
            self.session.delete(p)
        reservations = self.get_all_reservations()
        for r in reservations:
            self.session.delete(r)
        self.session.commit()

    def delete_queues(self):
        queues = self.get_all_queues()
        for q in queues:
            self.session.delete(q)
        self.session.commit()

    def delete_switches(self):
        switches = self.get_all_switches()
        for q in switches:
            self.session.delete(q)
        self.session.commit()

    def delete_links(self):
        links = self.get_all_links()
        for q in links:
            self.session.delete(q)
        self.session.commit()

    def delete_ports(self):
        ports = self.get_all_ports()
        for q in ports:
            self.session.delete(q)
        self.session.commit()

    def delete_hosts(self):
        hosts = self.get_all_hosts()
        for q in hosts:
            self.session.delete(q)
        self.session.commit()

    def add_record(self, record):
        print "ADDING " + str(record) + " TO DATABASE"
        self.session.add(record)
        self.session.commit()
        return record
