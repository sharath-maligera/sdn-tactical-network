import json
import matplotlib.pyplot as plt
import pandas as pd
import math
from collections import defaultdict

def ema(data, window):
    if len(data) < window + 2:
        return None
    alpha = 2 / float(window + 1)
    ema = []
    for i in range(0, window):
        ema.append(None)
    ema.append(data[window])
    for i in range(window+1, len(data)):
        ema.append(ema[i-1] + alpha*(data[i]-ema[i-1]))
    return ema

def plot_bandwidth_from_json(filenames=None, plot=None):
    if None not in (filenames,plot):
        cumulative_packet_arrival_data = defaultdict(dict)
        p = 0
        for filename in filenames:
            with open(filename, 'r') as f:
                server_log_dict = json.load(f)
                packet_arrival_data = defaultdict(list)
                intervals = server_log_dict['intervals']
                for i in intervals:
                    data_dict = i['streams'][0]
                    packet_arrival_data['start'].append(math.floor(data_dict['start']))
                    packet_arrival_data['end'].append(math.floor(data_dict['end']))
                    packet_arrival_data['kilo_bytes'].append(data_dict['bytes']*0.001)
                    packet_arrival_data['n_packets'].append(data_dict['packets'])
                    packet_arrival_data['jitter_ms'].append(data_dict['jitter_ms'])
                    packet_arrival_data['n_packets_lost'].append(data_dict['lost_packets'])
                    packet_arrival_data['packet_lost_percent'].append(data_dict['lost_percent'])
                    pass
                p=p+1
                priority='priority_'+str(p)
                cumulative_packet_arrival_data[priority]=packet_arrival_data

        seconds = cumulative_packet_arrival_data['priority_1']['start']

        kilobytes = [cumulative_packet_arrival_data['priority_1']['kilo_bytes'][i] +
                     cumulative_packet_arrival_data['priority_2']['kilo_bytes'][i] +
                     cumulative_packet_arrival_data['priority_3']['kilo_bytes'][i] +
                     cumulative_packet_arrival_data['priority_4']['kilo_bytes'][i] +
                     cumulative_packet_arrival_data['priority_5']['kilo_bytes'][i] for i in range(min(len(cumulative_packet_arrival_data['priority_1']['kilo_bytes']),
                                                                                                      len(cumulative_packet_arrival_data['priority_2']['kilo_bytes']),
                                                                                                      len(cumulative_packet_arrival_data['priority_3']['kilo_bytes']),
                                                                                                      len(cumulative_packet_arrival_data['priority_4']['kilo_bytes']),
                                                                                                      len(cumulative_packet_arrival_data['priority_5']['kilo_bytes'])))]

        bandwidth = []
        received_kilo_bytes = 0.0
        time_interval = 0
        for i in kilobytes:
            time_interval=time_interval+1
            received_kilo_bytes = float(received_kilo_bytes+i)
            bandwidth.append(received_kilo_bytes/time_interval)

        plt.plot(bandwidth, label='bandwidth')

        plt.legend()
        plt.title("Throughput")
        plt.ylabel("Throughput [KiloBytes / s]")
        plt.xlabel("Time")
        plt.savefig("plotname")
        plt.show()

        fig, axis = plt.subplots()
        axis.vlines(cumulative_packet_arrival_data['priority_1']['n_packets'], 0.0, 12, colors="green", linewidth=3.0, label='Priority 1 packets')
        axis.vlines(cumulative_packet_arrival_data['priority_2']['n_packets'], 0.0, 12, colors="red", linewidth=2.5, label='Priority 2 packets')
        axis.vlines(cumulative_packet_arrival_data['priority_3']['n_packets'], 0.0, 12, colors="blue", linewidth=2.0, label='Priority 3 packets')
        axis.vlines(cumulative_packet_arrival_data['priority_4']['n_packets'], 0.0, 12, colors="olive", linewidth=1.5, label='Priority 4 packets')
        axis.vlines(cumulative_packet_arrival_data['priority_5']['n_packets'], 0.0, 12, colors="slategrey", linewidth=1.0, label='Priority 5 packets')

        axis.set_title("Packet Arrival")
        axis.set_xlabel("time")
        #axis.set_ylim([0, 10])
        axis.set_xlim([0, 20])
        axis.legend()
        axis.set_ylabel("# of packets")
        fig.savefig("Arrival.png")
        plt.show()

if __name__ == '__main__':
    plot_bandwidth_from_json(filenames=['VHF_priority_1.json','VHF_priority_2.json','VHF_priority_3.json','VHF_priority_4.json','VHF_priority_5.json'], plot='VHF_priority_1.png')