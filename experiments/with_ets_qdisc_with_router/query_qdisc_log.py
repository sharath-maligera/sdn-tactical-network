import os
import subprocess
from subprocess import call
import sys
import json
import re
from time import sleep
import datetime
from collections import defaultdict
import csv

def main():
    with open(r'qdisc_log.csv', 'a') as csvfile:
        fieldnames = ['timestamp', 'handle', 'packets', 'bytes', 'qlen', 'drops']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        while True:
            sleep(2)
            command_str = 'tc -s -j qdisc show dev h1-eth0'
            result_command = str(subprocess.check_output(command_str,shell = True))
            ct = datetime.datetime.now()
            try:
                data = json.loads(result_command)
                for qdisc in data:
                    writer.writerow({'timestamp': ct, 'handle': qdisc['handle'], 'packets': qdisc['packets'], 'bytes': qdisc['bytes'], 'qlen': qdisc['qlen'],'drops': qdisc['drops']})
            except ValueError:
                pass


if __name__ == '__main__':
    main()