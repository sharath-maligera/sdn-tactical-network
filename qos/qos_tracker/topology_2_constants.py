s0_DPID = "16"

PIR_TABLE_ID = 0
CIR_TABLE_ID = 1
FLOW_TABLE_ID = 2

SWITCH_NUMBER_TABLE = {
    s0_DPID: 0
}

# Mapping of port numbers to mac addresses
HOST_MAP = {
    s0_DPID: {
        2: {
            "mac": '00:00:00:00:00:02',
            "ip": '10.0.0.2'
        },
        1: {
            "mac": '00:00:00:00:00:01',
            "ip": '10.0.0.1'
        },
        3: {
            "mac": '00:00:00:00:00:03',
            "ip": '10.0.0.3'
        },
        4: {
            "mac": '00:00:00:00:00:04',
            "ip": '10.0.0.4'
        }
    }
}

SWITCH_LOOKUP = {
    s0_DPID: "0000000000000010"
}
SWITCHES = [s0_DPID]

BEST_EFFORT_QUEUE_ID = 0
HIGH_PRIORITY_QUEUE_ID = 1

# Mapping of links to port_nos and their bandwidth
SWITCH_MAP = {
}