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

def end_to_end_delay(event_list):
    event_dict = defaultdict(list)
    for event in event_list:
        if len(event) >= 9:
            packet_received_timestamp = datetime.datetime.strptime(event[0], "%H:%M:%S.%f").time()
            protocol = parse_protocol_string(protocol_str=event[2])
            flow_id = parse_flow_id(flow_id_str=event[3])
            packet_seq_id = parse_sequence_id(seq_id_str=event[4])
            source_ip = parse_ip_address(ip_str=event[5], src_addr=True)
            destination_ip = parse_ip_address(ip_str=event[6], dest_addr=True)
            packet_sent_timestamp = parse_timestamp(timestamp_str=event[7])
            packet_size = parse_packet_size(packet_size_str=event[8])

            event_dict['packet_received'].append(packet_received_timestamp)
            event_dict['protocol'].append(protocol)
            event_dict['flow_id'].append(flow_id)
            event_dict['packet_seq_no'].append(packet_seq_id)
            event_dict['source_ip'].append(source_ip)
            event_dict['destination_ip'].append(destination_ip)
            event_dict['packet_sent'].append(packet_sent_timestamp)
            event_dict['packet_size'].append(packet_size)

    data = pd.DataFrame.from_dict(event_dict)

    start_time = data["packet_sent"].min()
    duration_timestamp = [datetime.datetime.combine(datetime.date.today(), t1) - datetime.datetime.combine(datetime.date.today(), start_time) for t1, t2 in zip(data["packet_sent"], data["packet_sent"]) if not (t1!=t1 or t2!=t2)]
    duration_in_secs = [duration.total_seconds() for duration in duration_timestamp]

    packet_delay_timestamp = [datetime.datetime.combine(datetime.date.today(), t1) - datetime.datetime.combine(datetime.date.today(), t2) for t1, t2 in zip(data["packet_received"], data["packet_sent"]) if not (t1!=t1 or t2!=t2)]
    packet_delay_in_secs = [delay.total_seconds() for delay in packet_delay_timestamp]

    # conditions = [data['flow_id'] == '1', data['flow_id'] == '2', data['flow_id'] == '3', data['flow_id'] == '4']
    # colors = ["#9b59b6" , "#3D85C6", "#F1C232", "#4C9C23"]
    # data["color"] = np.select(conditions, colors, default=np.nan)

    #colors = {'1': "#8E7CC3", '2': "#76A5AF", '3': "#FFD966", '4': "#C27BA0", '5': "#E06666" }
    #colors = {'1': "#340000", '2': "#B40101", '3': "#BF9000" , '4': "#F4D679",'5': "#E5ADAD" }
    #data_sorted = data[data[:, 2].argsort()]
    colors = ["#340000", "#B40101", "#BF9000", "#F4D679", "#E5ADAD"]
    sns.set_style("darkgrid")
    customPalette = sns.set_palette(sns.color_palette(colors))
    markers = {"4": "*", "3": "*", "2": '*', "1": '*'}

    ax = sns.relplot(x=duration_in_secs, y=packet_delay_in_secs, data=data, hue='flow_id', dashes=True, kind='scatter',
                     palette={1: "#340000", 2: "#B40101", 3: "#BF9000", 4: "#F4D679", 5: "#E5ADAD"}).set(ylim=(0)) #size="flow_id", palette=colors
    ax.set(xlabel='Time (sec)', ylabel='End-to-End delay (sec)')

    ax.fig.suptitle("End-to-End delay in non-QoS", y=1)
    ax._legend.set_title("Priority")
    new_labels = ['Medical Evacuation (Flash-0)', 'Obstacle Alert (Immediate-1)', 'Video (Immediate-1)', 'Picture (Priority-2)', 'FFT (Routine-3)']
    for t, l in zip(ax._legend.texts, new_labels): t.set_text(l)

    ax._legend.set_bbox_to_anchor([0.9, 0.83])
    plt.savefig('E2E-Delay-non-QoS.eps', format='eps')
    plt.savefig('E2E-Delay-non-QoS.png', format='png')
    plt.show()


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

def init():
    base_folder = os.path.dirname(__file__)
    filename = os.path.join(base_folder, 'receive_log_copy.txt')

    with open(filename, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()
        receive_events = []
        for line in lines:
            value_list = line.split()
            if 'START' not in value_list and 'LISTEN' not in value_list:
                receive_events.append(value_list)

        end_to_end_delay(event_list=receive_events)


def parse_packet_size(packet_size_str=None):
    if packet_size_str is not None:
        packet_size = None
        if re.search("size", packet_size_str) is not None:
            match = re.search(r'[0-9]+', packet_size_str)
            if match:
                packet_size = match.group()
        return packet_size

if __name__ == '__main__':
    init()