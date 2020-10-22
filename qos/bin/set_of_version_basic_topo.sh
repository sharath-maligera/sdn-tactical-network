sudo ovs-vsctl set Bridge s0 protocols=OpenFlow13
sudo ovs-vsctl set Bridge s1 protocols=OpenFlow13
sudo ovs-vsctl set Bridge s2 protocols=OpenFlow13
sudo ovs-vsctl set-manager ptcp:6632
