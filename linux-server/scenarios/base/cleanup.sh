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