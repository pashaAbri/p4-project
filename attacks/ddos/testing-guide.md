# P4 Program Testing Guide

## Overview
This guide outlines the steps to compile, set up, and test a P4 program using BMv2 and Scapy.

## Compiling the P4 Program
1. **Compile with p4c**:
   ```bash
   p4c --target bmv2 --arch v1model --p4runtime-files your_program.p4info.txt your_program.p4
   ```

## Setting Up BMv2 Switch
1. **Run simple_switch_grpc**:
   ```bash
   sudo simple_switch_grpc --no-p4 -i 1@<your-interface> your_program.json
    ```

## Control Plane Configuration
1. **Populate Match-Action Tables**:
   Use a P4Runtime client to configure the switch.

## Running the Scapy Script
1. **Execute Scapy Script**:
   Run the script as root or using `sudo` to generate network traffic.

## Observation and Analysis
1. **Monitor Switch Behavior**:
   Use tools like Wireshark for detailed traffic analysis.

## Conclusion
This guide provides a basic framework for testing P4 programs. Adjust as necessary for your specific setup.
