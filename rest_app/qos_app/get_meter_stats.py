import requests
import pprint
import json
import time
import csv
import datetime

with open(r'meter_log.csv', 'a') as csvfile:
    fieldnames = ['timestamp', 'meter_id', 'packets', 'bytes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    while True:
        time.sleep(1)
        ct = datetime.datetime.now()
        response = requests.get('http://192.168.1.101:8080/qos/meter/0000000000000010')
        if response.status_code == 200:
            try:
                data_response = response.json()
                result_dict = data_response[0]
                switch_ids = result_dict['command_result']
                for meter in switch_ids['16']:
                    writer.writerow({'timestamp': ct, 'meter_id': meter['meter_id'], 'packets': meter['packet_in_count'], 'bytes': meter['byte_in_count']})
            except ValueError:
                pass
