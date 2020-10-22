sudo ovs-vsctl set Bridge s1 protocols=OpenFlow13
sudo ovs-vsctl set-manager ptcp:6632

echo "Adding ovsdb address to switch:"
# Add ovsdb address to switch
curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr
echo "\n"

echo "Adding queue settings to switch:"
# Add queue settings to switch
#curl -X POST -d '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues": [{"max_rate": "500000"},{"min_rate": "800000"}]}' http://localhost:8080/qos/queue/0000000000000001
curl -X POST -d '{"port_name":"s1-eth1","type":"linux-htb", "max_rate":"1000000","queues":[{"max_rate":"500000"},{"min_rate":"800000"}]}' http://localhost:8080/qos/queue/0000000000000001
echo "\n"

echo "Adding queue-assignment flow:"
# Install flow entry to assign queue id
curl -X POST -d '{"match":{"nw_dst":"10.0.0.1","nw_proto":"UDP","tp_dst":"5002"},"actions":{"queue":1}}' http://localhost:8080/qos/rules/0000000000000001
echo "\n"
