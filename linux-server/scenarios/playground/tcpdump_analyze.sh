#!/bin/bash

PCAP_FILE="./output_files/traffic_veth5.pcap"
MIN_SIZE=1000  # Define a minimum payload size that you consider suspicious, adjust as needed.

# Check if the pcap file exists
if [ ! -f "$PCAP_FILE" ]; then
    echo "The pcap file $PCAP_FILE does not exist."
    exit 1
fi

# Use tcpdump to read the pcap file and look for packets with a payload size greater than MIN_SIZE
tcpdump -r "$PCAP_FILE" -nn 'greater $MIN_SIZE' -A

