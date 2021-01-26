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


def view_qdisc_meter_log():
    experiments_folder = Path(__file__).resolve().parents[1]
    qdisc_log = os.path.join(experiments_folder, os.path.join('data', os.path.join('with_shaping_and_ets_scheduling_no_timeout','qdisc_log_2_4_60_kbps.csv')))
    df_qdisc = pd.read_csv(qdisc_log)
    meter_log = os.path.join(experiments_folder, os.path.join('data',os.path.join('with_shaping_and_ets_scheduling_no_timeout','meter_log_2_4_60_kbps.csv')))
    df_meter = pd.read_csv(meter_log)
    pass

def parse_qdisc_meter_log():
    experiments_folder = Path(__file__).resolve().parents[1]
    qdisc_log = os.path.join(experiments_folder, os.path.join('data', os.path.join('with_shaping_and_ets_scheduling_no_timeout', 'qdisc_log_0_6_15_kbps.csv')))
    df_qdisc = pd.read_csv(qdisc_log)
    start_time = df_qdisc["timestamp"].min()
    format = '%Y-%m-%d %H:%M:%S.%f'
    duration_timestamp = [datetime.datetime.strptime(t1, format) - datetime.datetime.strptime(start_time, format) for t1, t2 in zip(df_qdisc["timestamp"], df_qdisc["timestamp"]) if not (t1!=t1 or t2!=t2)]
    duration_in_secs = [duration.total_seconds() for duration in duration_timestamp]
    df_qdisc.insert(6, "duration_in_secs", duration_in_secs, True)
    df_qdisc = pd.DataFrame(df_qdisc, columns=['duration_in_secs', 'handle', 'packets', 'bytes'])
    df_qdisc.to_csv(os.path.join(os.path.dirname(__file__), 'plot_qdisc_log_0_6_15_kbps.csv'), index=False, header=True)

    meter_log = os.path.join(experiments_folder, os.path.join('data', os.path.join('with_shaping_and_ets_scheduling_no_timeout', 'meter_log_0_6_15_kbps.csv')))
    df_meter = pd.read_csv(meter_log)
    start_time = df_meter["timestamp"].min()
    format = '%Y-%m-%d %H:%M:%S.%f'
    duration_timestamp = [datetime.datetime.strptime(t1, format) - datetime.datetime.strptime(start_time, format) for
                          t1, t2 in zip(df_meter["timestamp"], df_meter["timestamp"]) if not (t1 != t1 or t2 != t2)]
    duration_in_secs = [duration.total_seconds() for duration in duration_timestamp]
    df_meter.insert(4, "duration_in_secs", duration_in_secs, True)
    df_meter = pd.DataFrame(df_meter, columns=['duration_in_secs', 'handle', 'packets', 'bytes'])
    df_meter.to_csv(os.path.join(os.path.dirname(__file__), 'plot_meter_log_0_6_15_kbps.csv'), index=False,header=True)


if __name__ == '__main__':
    #view_qdisc_meter_log()
    parse_qdisc_meter_log()