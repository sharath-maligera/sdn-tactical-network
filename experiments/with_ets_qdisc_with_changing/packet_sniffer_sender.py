import codecs
import sys
import pyshark
import argparse
import logbook
from collections import defaultdict
import os
from datetime import datetime
from pprint import pprint
import pandas as pd

packet_log = logbook.Logger('Packet Capture App!')

def init_logging(filename = None):
    """
    function to initialize logging, if filename is provided log to the file else log to console(stdout mode)
    @param filename: filename to log into(optional)
    """
    level = logbook.TRACE
    if filename:
        logbook.TimedRotatingFileHandler(filename, level=level).push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()

    msg = 'Logging initialized, level: {}, mode: {}'.format(
        level,
        "stdout mode" if not filename else 'file mode: ' + filename
    )
    logger = logbook.Logger('Startup')
    logger.notice(msg)

def parse_datetime_prefix(datetime_string=None, date_time_format=None):
    """
    function to parse timestamp string and convert to required format to be written to database
    @param datetime_string:     timestamp string
    @param date_time_format:    format to which timestamp to be parsed into
    @return:                    datetime value in string format
    """
    if None not in (datetime_string,date_time_format):
        try:
            string_len = len(datetime_string)
            if string_len > 29:
                datetime_string = datetime_string[:28]
            datetime_value = datetime.datetime.strptime(datetime_string, date_time_format)
        except ValueError as v:
            if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                datetime_stripped = datetime_string[:-(len(v.args[0]) - 26)]
                datetime_value = datetime.datetime.strptime(datetime_stripped, date_time_format)
            else:
                raise
        return str(datetime_value)

def parse_string(string):
    """
    function to convert acquired data to string format
    @param string:  data
    @return:        data in string format if it exists else return None to fill 'null' value in the corresponding table record
    """
    if not string:
        return None
    else:
        return str(string)


def capture_live_packets(config_dict=None):
    function_logger = '[capture_live_packets]'
    if config_dict is not None:
        packet_data_dict = defaultdict(list)
        try:
            cap = pyshark.LiveCapture(interface=config_dict.get('from_interface'),bpf_filter='host 192.168.0.2 and not arp',only_summaries=False,use_json=False)#bpf_filter='host 192.168.0.2 and not arp',,capture_filter='host 192.168.0.2 and not arp'

            cap.set_debug()
            while True:
                for packet in cap.sniff_continuously():
                    if 'ipv6' in packet:
                        pass
                    else:
                        try:
                            packet_log.trace(function_logger + ' Packet Just arrived:')
                            packet_data_dict['packet_id'].append(packet.number)
                            packet_sniff_time = packet.sniff_time.strftime('%b %d, %Y %H:%M:%S.%f')
                            packet_data_dict['packet_timestamp'].append(packet_sniff_time)
                            packet_data_dict['source_ip'].append(parse_string(packet.ip.src_host))
                            packet_data_dict['destination_ip'].append(parse_string(packet.ip.dst_host))
                            packet_data_dict['protocol'].append(parse_string(packet.transport_layer))
                            packet_data_dict['dsfield'].append(packet.ip.dsfield)
                            packet_data_dict['packet_length'].append(packet.length)

                            packet_msg = '\nPacket Data:\t' \
                                         + 'packet_id: ' + str(packet.number) + '\n\t\t' \
                                         + 'packet_timestamp: ' + packet_sniff_time + '\n\t\t' \
                                         + 'source_ip: ' + str(packet.ip.src_host) + '\n\t\t' \
                                         + 'destination_ip: ' + str(packet.ip.dst_host) + '\n\t\t' \
                                         + 'protocol: ' + str(packet.transport_layer) + '\n\t\t' \
                                         + 'dsfield: ' + str(packet.ip.dsfield) + '\n\t\t' \
                                         + 'packet_length: ' + str(packet.length)
                            packet_log.trace(function_logger + packet_msg)
                        except Exception as exception:
                            pass
                            packet_log.trace(exception)
                #data = pd.DataFrame.from_dict(packet_data_dict)
                #data.to_csv(os.path.join(os.path.dirname(__file__), 'packet_sniffer_sender.csv'), index=False, header=True)

        except Exception as exception:
            pass
            packet_log.trace(exception)


if __name__ == '__main__':
    try:
        init_logging()
        parser = argparse.ArgumentParser(description="Packet Capture App!")
        parser.add_argument("-i", "--interface", help="The interface from which the packets have to be captured", type=str, default='h1-eth0')
        args = parser.parse_args()
        if args.interface:
            msg = "Packet will be captured with interface: {interface} \n".format(interface=args.interface)
            packet_log.trace(msg)
            config_dict = {
                'from_interface': str(args.interface)
            }
            capture_live_packets(config_dict=config_dict)
    except SystemExit:
        packet_log.trace("Exit of Packet Capture App!")