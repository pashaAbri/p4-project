#!/bin/bash
# Compile the P4 program.
echo "Compiling the P4 program..."
p4c -b bmv2 demo2.p4 -o demo2.bmv2

# Start the software switch as a background process
echo "Starting simple_switch..."
# sudo simple_switch --interface 0@veth0 --interface 1@veth2 --interface 2@veth4 demo2.bmv2/demo2.json &
echo "run the following command: "
echo "sudo simple_switch --interface 0@veth0 --interface 1@veth2 --interface 2@veth4 demo2.bmv2/demo2.json &"
