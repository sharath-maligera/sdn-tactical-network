import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import datetime
import re
from functools import partial
import math
import matplotlib.dates as md
from pathlib import Path


def end_to_end_delay_with_qdisc(receive_events_wo_qdisc=None):
    if receive_events_wo_qdisc is not None:
        event_wo_qdisc_dict = defaultdict(list)
        for event in receive_events_wo_qdisc:
            if len(event) >= 9:
                packet_received_timestamp = datetime.datetime.strptime(event[0], "%H:%M:%S.%f").time()
                protocol = parse_protocol_string(protocol_str=event[2])
                flow_id = parse_flow_id(flow_id_str=event[3])
                packet_seq_id = parse_sequence_id(seq_id_str=event[4])
                source_ip = parse_ip_address(ip_str=event[5], src_addr=True)
                destination_ip = parse_ip_address(ip_str=event[6], dest_addr=True)
                packet_sent_timestamp = parse_timestamp(timestamp_str=event[7])
                packet_size = parse_packet_size(packet_size_str=event[8])

                event_wo_qdisc_dict['packet_received'].append(packet_received_timestamp)
                event_wo_qdisc_dict['protocol'].append(protocol)
                event_wo_qdisc_dict['flow_id'].append(int(flow_id))
                event_wo_qdisc_dict['packet_seq_no'].append(int(packet_seq_id))
                event_wo_qdisc_dict['source_ip'].append(source_ip)
                event_wo_qdisc_dict['destination_ip'].append(destination_ip)
                event_wo_qdisc_dict['packet_sent'].append(packet_sent_timestamp)
                event_wo_qdisc_dict['packet_size'].append(packet_size)


        data_wo_qdisc = pd.DataFrame.from_dict(event_wo_qdisc_dict)
        wo_qdisc_packet_delay_timestamp = [datetime.datetime.combine(datetime.date.today(), t1) - datetime.datetime.combine(datetime.date.today(), t2) for t1, t2 in zip(data_wo_qdisc["packet_received"], data_wo_qdisc["packet_sent"]) if not (t1!=t1 or t2!=t2)]
        wo_qdisc_packet_delay_in_secs = [delay.total_seconds() for delay in wo_qdisc_packet_delay_timestamp]
        data_wo_qdisc.insert(8, "packet_delay_in_secs", wo_qdisc_packet_delay_in_secs, True)
        data_wo_qdisc['packet_seq_no'] += 1

        df_wo_qdisc = pd.DataFrame(data_wo_qdisc, columns=['packet_seq_no', 'packet_delay_in_secs', 'flow_id'])
        df_wo_qdisc.to_csv(os.path.join(os.path.dirname(__file__), 'data_with_qdiscs_0_6_kbps.csv'), index=False, header=True)

def parse_protocol_string(protocol_str=None):
    if protocol_str is not None:
        if re.search("UDP", protocol_str) is not None:
            protocol = 'UDP'
        elif re.search('TCP', protocol_str) is not None:
            protocol = 'TCP'
        else:
            protocol = None

        return protocol

def parse_flow_id(flow_id_str=None):
    if flow_id_str is not None:
        flow_id = None
        if re.search("flow", flow_id_str) is not None:
            match = re.search(r'\d', flow_id_str)
            if match:
                flow_id = int(match.group())
        return flow_id

def parse_sequence_id(seq_id_str=None):
    if seq_id_str is not None:
        seq_id = None
        if re.search("seq", seq_id_str) is not None:
            match = re.search(r'[0-9]+', seq_id_str)
            if match:
                seq_id = match.group()
        return seq_id

def parse_ip_address(ip_str=None, src_addr=False, dest_addr=False):
    if ip_str is not None:
        ip_addr = None
        if src_addr:
            if re.search("src", ip_str) is not None:
                ip_pattern = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{4}")
                match = re.findall(ip_pattern, ip_str)
                if len(match) > 0:
                    ip_addr = match[0]
        elif dest_addr:
            if re.search("dst", ip_str) is not None:
                ip_pattern = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{4}")
                match = re.findall(ip_pattern, ip_str)
                if len(match) > 0:
                    ip_addr = match[0]

        return ip_addr

def parse_timestamp(timestamp_str=None):
    if timestamp_str is not None:
        timestamp = None
        if re.search("sent", timestamp_str) is not None:
            timestamp_pattern = re.compile("\d{2}\:\d{2}\:\d{2}\.\d{6}")
            match = re.findall(timestamp_pattern, timestamp_str)
            if len(match) > 0:
                timestamp = datetime.datetime.strptime(match[0], "%H:%M:%S.%f").time()
        return timestamp

def parse_packet_size(packet_size_str=None):
    if packet_size_str is not None:
        packet_size = None
        if re.search("size", packet_size_str) is not None:
            match = re.search(r'[0-9]+', packet_size_str)
            if match:
                packet_size = match.group()
        return packet_size

def plot_with_qdiscs():
    experiments_folder = Path(__file__).resolve().parents[1]
    receive_log_wo_qdisc = os.path.join(experiments_folder, os.path.join('data', os.path.join('with_shaping_and_scheduling_wo_everchanging','receive_log_0_6_kbps.txt')))
    receive_events_wo_qdisc = []

    with open(receive_log_wo_qdisc, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()
        for line in lines:
            value_list = line.split()
            if 'START' not in value_list and 'LISTEN' not in value_list:
                receive_events_wo_qdisc.append(value_list)

    end_to_end_delay_with_qdisc(receive_events_wo_qdisc=receive_events_wo_qdisc)


if __name__ == '__main__':
    plot_with_qdiscs()