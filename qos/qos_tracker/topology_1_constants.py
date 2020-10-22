s0_DPID = "16"
s1_DPID = "32"
s2_DPID = "48"

PIR_TABLE_ID = 0
CIR_TABLE_ID = 1
FLOW_TABLE_ID = 2

SWITCH_NUMBER_TABLE = {
    s0_DPID: 0,
    s1_DPID: 1,
    s2_DPID: 2
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
        }
    },
    s1_DPID: {
        1: {
            "mac": '00:00:00:00:00:03',
            "ip": '10.0.0.3'
        },
        2: {
            "mac": '00:00:00:00:00:04',
            "ip": '10.0.0.4'
        }
    },
    s2_DPID: {
    }
}

SWITCH_LOOKUP = {
    s0_DPID: "0000000000000010",
    s1_DPID: "0000000000000020",
    s2_DPID: "0000000000000030"
}

BEST_EFFORT_QUEUE_ID = 0
HIGH_PRIORITY_QUEUE_ID = 1

# Mapping of links to port_nos and their bandwidth
SWITCH_MAP = {
    s0_DPID: { # DPID: 16
        3: {
            "dpid": s2_DPID,
            "bw": 1000000
        }
    },
    s1_DPID: { # DPID: 32
        3: {
            "dpid": s2_DPID,
            "bw": 1000000
        }
    },
    s2_DPID: {
        1: {
            "dpid": s0_DPID,
            "bw": 1000000
        },
        2: {
            "dpid": s1_DPID,
            "bw": 1000000
        }
    }
}