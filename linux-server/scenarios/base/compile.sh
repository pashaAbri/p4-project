#!/bin/bash
# Compile the P4 program.
echo "Compiling the P4 program..."
p4c -b bmv2 base.p4 -o base.bmv2

# Start the software switch as a background process
echo "Starting simple_switch..."
# sudo simple_switch --interface 0@veth0 --interface 1@veth2 --interface 2@veth4 base.bmv2/base.json &
echo "run the following command: "
echo "sudo simple_switch --interface 0@veth0 --interface 1@veth2 --interface 2@veth4 base.bmv2/base.json &"
