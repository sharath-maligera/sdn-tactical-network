from __future__ import division
import json
import matplotlib.pyplot as plt
import sys
import argparse


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


def chart(args, data):
    # Setting the default values
    expected_bandwidth = 0
    ema_window = 9
    if args.protocol == 'udp':
        sum_string = 'sum'
    else:
        sum_string = 'sum_sent'
    if args.ema is not None:
        ema_window = int(args.ema)
    if args.expectedbw is not None:
        expected_bandwidth = int(args.expectedbw)

    debit = []
    intervals = data['intervals']
    for i in intervals:
        debit.append(i['sum']['bits_per_second'])

    plt.plot(debit, label='Bandwitdh (per second)')

    #plt.axhline(data['end'][sum_string]['bits_per_second'], color='r', label='Avg bandwidth')
    plt.axhline(expected_bandwidth * 8000, color='g', label='Expected bandwidth')
    plt.plot(ema(debit, ema_window), label='Bandwidth {} period moving average'.format(ema_window))

    #plt.title('{}, {}, {:.3}GB file'.format(data['start']['timestamp']['time'],
    #                                     data['start']['test_start']['protocol'],
    #                                    data['end'][sum_string]['bytes']/1000000000))
    plt.legend()
    if args.log:
        plt.yscale('log')
    else:
        plt.yscale('linear')
        plt.ylim(bottom=0)
    plt.ylabel('bit/s')
    plt.xlabel('time interval')
    plt.show()


def be_verbose(args, data):
    print('Version 1.0 - Feb 2019')
    print('Command arguments are {}'.format(args))
    print('Start info : {}'.format(data['start']))
    print('End info : {}'.format(data['end']))


def main(argv):
    parser = argparse.ArgumentParser(description='Simple python iperf JSON data vizualiser. Use -J option with iperf to have a JSON output.')
    parser.add_argument('input', nargs='?', help='JSON output file from iperf', default='UHF_dst.json')
    parser.add_argument('-a', '--ema', help='Exponential moving average used to smooth the bandwidth. Default at 9.', type=int, default=4)
    parser.add_argument('-e', '--expectedbw', help='Expected bandwidth to be plotted in Mb.', default=240)
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')
    parser.add_argument('-l', '--log', help='Plot will be in logarithmic scale', action='store_true')
    args = parser.parse_args(argv)
    with open(args.input) as f:
        data = json.load(f)
        if args.verbose:
            be_verbose(args, data)
        if data['start']['test_start']['protocol'] == 'UDP':
            args.protocol = 'udp'
        else:
            args.protocol = 'tcp'
        chart(args, data)


if __name__ == '__main__':
    main(sys.argv[1:])