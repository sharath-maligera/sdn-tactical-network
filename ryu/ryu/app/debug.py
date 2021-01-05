#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from ryu.cmd import manager


def main():
    sys.argv.append('--ofp-tcp-listen-port')
    sys.argv.append('6633')
    sys.argv.append('debug_qos_simple_switch_13')
    sys.argv.append('rest_qos')
    sys.argv.append('rest_conf_switch')
    sys.argv.append('ofctl_rest')
    sys.argv.append('flowmanager')
    sys.argv.append('--verbose')
    sys.argv.append('--enable-debugger')
    sys.argv.append('--observe-links')
    manager.main()

if __name__ == '__main__':
    main()