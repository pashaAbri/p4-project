#!/bin/bash

# Remove the compiled P4 program directory
echo "Cleaning up compiled P4 program directory..."
rm -rf base.bmv2

# Terminate any running simple_switch processes
echo "Terminating any running simple_switch processes..."
pkill simple_switch

# Function to delete a veth pair if it exists
delete_veth_pair() {
    if ip link show "$1" > /dev/null 2>&1; then
        echo "Deleting veth pair: $1 and its peer"
        sudo ip link delete "$1"
    else
        echo "Veth pair $1 does not exist, skipping deletion."
    fi
}

# Delete the virtual Ethernet pairs
delete_veth_pair veth0
delete_veth_pair veth2
delete_veth_pair veth4

echo "Cleanup complete."

# Compile the P4 program.
# In the commands below, the -b option selects bmv2 (Behavioral Model Version 2) as the target,
# which is the software switch that we will use to run the P4 program.
p4c -b bmv2 base.p4 -o base.bmv2

# start the software switch as a background process:
sudo simple_switch --interface 0@veth0 --interface 1@veth2 --interface 2@veth4 base.bmv2/base.json &

# First pair: veth0-veth1
sudo ip link add name veth0 type veth peer name veth1
sudo ip link set dev veth0 up
sudo ip link set dev veth1 up
sudo ip link set veth0 mtu 9500
sudo ip link set veth1 mtu 9500
sudo sysctl net.ipv6.conf.veth0.disable_ipv6=1
sudo sysctl net.ipv6.conf.veth1.disable_ipv6=1

# Second pair: veth2-veth3
sudo ip link add name veth2 type veth peer name veth3
sudo ip link set dev veth2 up
sudo ip link set dev veth3 up
sudo ip link set veth2 mtu 9500
sudo ip link set veth3 mtu 9500
sudo sysctl net.ipv6.conf.veth2.disable_ipv6=1
sudo sysctl net.ipv6.conf.veth3.disable_ipv6=1

# Second pair: veth4-veth5
sudo ip link add name veth4 type veth peer name veth5
sudo ip link set dev veth4 up
sudo ip link set dev veth5 up
sudo ip link set veth4 mtu 9500
sudo ip link set veth5 mtu 9500
sudo sysctl net.ipv6.conf.veth4.disable_ipv6=1
sudo sysctl net.ipv6.conf.veth5.disable_ipv6=1
