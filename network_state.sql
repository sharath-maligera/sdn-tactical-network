
CREATE SCHEMA IF NOT EXISTS test;

-- An entry to switch table represents a switch in the network along with it's data path id
CREATE TABLE IF NOT EXISTS test.switch(
    dpid INTEGER NOT NULL PRIMARY KEY
);

-- An entry to port table represents a port on the switch
CREATE TABLE IF NOT EXISTS test.port(
    id INTEGER NOT NULL PRIMARY KEY,
    switch INTEGER REFERENCES test.switch (dpid),
    port_no INTEGER
);

-- An entry to host table represents a host in the network
-- We keep reference to the port id that the host is connected to the switch
CREATE TABLE IF NOT EXISTS test.host (
    id INTEGER NOT NULL PRIMARY KEY,
    mac VARCHAR,
    ip VARCHAR,
    port INTEGER REFERENCES test.port (id)
);

-- An entry to link table represents the link between two switch
-- Bandwidth column represent the link bandwidth in bits
CREATE TABLE IF NOT EXISTS test.link(
    id INTEGER NOT NULL PRIMARY KEY,
    src INTEGER REFERENCES test.port (id),
    dst INTEGER REFERENCES test.port (id),
    bandwidth INTEGER
);

-- An entry in reservation table represents bandwidth reservation
-- It maintains IP address of both source and destination along with ingress and egress ports of the host
-- in_port is the port of the host->switch; out_port is the port of switch->switch where the bandwidth is reserved
CREATE TABLE IF NOT EXISTS test.reservation(
    id INTEGER NOT NULL PRIMARY KEY,
    src VARCHAR,
    dst VARCHAR,
    bw INTEGER,
    mpls_label INTEGER,
    in_port INTEGER REFERENCES test.port (id),
    out_port INTEGER REFERENCES test.port (id)
);

-- An entry to the port_reservation table represents a switch along a reserved flow
-- It stores the ID of the ingress port to each switch along a flows path
CREATE TABLE IF NOT EXISTS test.port_reservation (
    id INTEGER NOT NULL PRIMARY KEY,
    port INTEGER REFERENCES test.port (id),
    reservation INTEGER REFERENCES test.reservation (id)
);

TRUNCATE TABLE test.port, test.host, test.link, test.switch, test.reservation, test.port_reservation;

