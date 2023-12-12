# P4 Project

# High-Level Outline

#### 1. Running and Analyzing Demo Programs:
Start with the demo programs in the jafingerhut/p4-guide repository to understand standard P4 code practices.

#### 2. Creating Network Scenarios with Scapy:
Use Scapy to simulate network scenarios that can test the AI-generated P4 code, focusing on how well it handles security threats.

#### 3. Reviewing PSA Examples:
Analyze the PSA examples to see how complex switch configurations are handled and where AI tools might introduce vulnerabilities.

#### 4. Benchmarking AI Tool Outputs: 
Compare the outputs from AI coding assistants against the benchmarks established in the packet classification and TCP options parser sections.

#### 5. Documenting Findings:
As you progress through these steps, document your findings, especially noting any discrepancies or unique insights gained about the impact of AI coding assistants on P4 programming and network security.

# P4-Guide Repositories

## Overview
This document outlines how to use the jafingerhut/p4-guide GitHub resources for assessing the impact of coding assistants and generative AI tools on P4 programming and network security.

## Repositories and Their Uses

### 1. Demo Programs (`demo1` to `demo7`)
- **Purpose**: Analyze standard P4 coding patterns.
- **Method**: Run these programs and compare their structure and function with AI-generated P4 code.

### 2. Scapy (`scapy`)
- **Purpose**: Create and analyze network packets.
- **Method**: Develop scenarios to test the robustness of AI-generated P4 code against security threats.

### 3. PSA Examples (`psa-examples`)
- **Purpose**: Understand complex switch configurations.
- **Method**: Review examples for insights into potential vulnerabilities introduced by AI tools.

### 4. Packet Classification (`packet-classification`)
- **Purpose**: Benchmark AI tool outputs.
- **Method**: Use classification algorithms as a security effectiveness measure for AI-generated code.

### 5. TCP Options Parser (`tcp-options-parser`)
- **Purpose**: Study network protocol handling.
- **Method**: Compare AI tool outputs against standard implementations for vulnerability assessment.

### 6. CRC Calculations (`crc`)
- **Purpose**: Ensure data integrity.
- **Method**: Study CRC implementations in P4 and their AI-generated counterparts.

### 7. Data Plane Writable State (`data-plane-writable-per-table-entry-state`)
- **Purpose**: Explore data plane state manipulations.
- **Method**: Assess how AI tools handle state changes in P4 programming.

# Attack Scenarios for Testing

## Overview
This section outlines specific network attack scenarios to test AI-generated P4 code's robustness and security.

### 1. DDoS Attacks
- **Purpose**: Test handling of high-volume network traffic.
- **Method**: Simulate a DDoS scenario and analyze the AI-generated P4 code's response.

### 2. Packet Spoofing
- **Purpose**: Evaluate effectiveness against spoofed packets.
- **Method**: Create scenarios with spoofed packets and observe the AI-generated code's detection capabilities.

### 3. Side-Channel Attacks
- **Purpose**: Assess vulnerability to side-channel exploits.
- **Method**: Test for variations in processing times or other side channels that could leak information.

### 4. Zero-Day Vulnerabilities
- **Purpose**: Examine response to unknown threats.
- **Method**: Introduce new, uncommon network traffic and analyze the AI-generated P4 code's adaptability and security response.

## Using the Open Networking Foundation's Guide for P4 Setup

This section provides an overview of how we utilized the resources provided by the Open Networking Foundation (ONF) in their blog post titled ["Getting Started with P4"](https://opennetworking.org/news-and-events/blog/getting-started-with-p4/) to set up our P4 programming environment.

### Overview of the Guide

The ONF's guide offers a comprehensive introduction to P4 programming, targeting beginners who are new to the P4 language. It covers the following key areas:

1. **Introduction to P4**: The guide begins with a basic introduction to P4 and its significance in programmable networks.
2. **Setting Up the Environment**: It provides detailed instructions on setting up a development environment for P4, including software requirements and installation steps.
3. **Creating and Running a P4 Program**: The guide walks through the process of writing a basic P4 program, compiling it, and running it on a simulated software switch.

### Key Components Used in Our Setup

In our project, we specifically focused on the following components from the ONF guide:

1. **P4 Compiler Installation**: We followed the guide to install the P4 compiler (`p4c`) on our Linux server, ensuring that we had the necessary tools to compile P4 programs.
2. **Software Switch (BMv2)**: The Behavioral Model version 2 (BMv2), also known as `simple_switch`, was set up as per the instructions in the guide. This software switch allows us to run and test P4 programs in a simulated environment.
3. **Sample P4 Program**: We used the sample P4 program provided in the guide as a starting point for our development. This program helped us understand the basics of P4 syntax and functionality.
4. **Network Simulation using veth Interfaces**: The guide's methodology for creating virtual Ethernet interfaces and using them for network simulation was crucial in our setup. It allowed us to create a controlled environment for testing P4 programs.

### Adaptations and Extensions

While the ONF guide provided the foundational knowledge, we adapted and extended the setup as follows:

- **Custom P4 Programs**: Beyond the sample program, we developed custom P4 applications tailored to our project requirements.
- **Scapy for Packet Testing**: We integrated Scapy, a Python-based packet crafting tool, to generate and send test packets through our simulated network, allowing us to observe and analyze the behavior of our P4 programs.

** The ONF's "Getting Started with P4" blog post was instrumental in setting up our P4 development environment. It provided clear, step-by-step instructions that we could easily follow and adapt to our specific project needs. This setup has been essential for our exploration and research into P4 programming and its applications in network security and management.

## Environment Setup and Running the P4 Simulation

This section outlines the steps to set up the environment for P4 programming and running simulations. It includes the installation of necessary packages and software components.

### Prerequisites

Before beginning the setup, ensure the following prerequisites are met:

- A Linux-based operating system (preferably Ubuntu 18.04 LTS).
- Sufficient disk space and computing resources (especially if running in a virtualized environment like AWS).
- Python installed, with Pip for package management.

### Installation Steps

1. **Install Dependencies**:
   Install the necessary dependencies for P4 programming and the behavioral model:
   ```bash
   sudo apt-get update
   sudo apt-get install -y cmake g++ git automake libtool libgc-dev bison flex libfl-dev libgmp-dev libboost-dev libboost-iostreams-dev libboost-graph-dev llvm pkg-config python python-scapy python-ipaddr python-ply tcpdump doxygen graphviz texlive-full
    ```
2. **Install Protobuf**:
   Protobuf is required for the P4 compiler:
    ```bash
    git clone https://github.com/protocolbuffers/protobuf.git
    cd protobuf
    git checkout v3.2.0
    ./autogen.sh
    ./configure
    make
    sudo make install
    sudo ldconfig
    cd ..
   ```
3. **Install P4 Compiler (p4c)**
   Clone and build the P4 compiler:
    ```bash
   git clone --recursive https://github.com/p4lang/p4c.git
    cd p4c
    mkdir build
    cd build
    cmake ..
    make -j4
    sudo make install
    cd ../..
   ```
4. **Install BMv2 (Behavioral Model v2)**
   Install the software switch to run P4 programs:
    ```bash
   git clone https://github.com/p4lang/behavioral-model.git
    cd behavioral-model
    ./install_deps.sh
    ./autogen.sh
    ./configure
    make
    sudo make install
    sudo ldconfig
    cd ..
   ```

### Running the Simulation
1. **Set Up Virtual Ethernet Interfaces**
    Create virtual Ethernet interfaces for the simulation:
    ```bash
    # Example for creating one pair of veth interfaces
    sudo ip link add name veth0 type veth peer name veth1
    sudo ip link set dev veth0 up
    sudo ip link set dev veth1 up
    sudo ip link set veth0 mtu 9500
    sudo ip link set veth1 mtu 9500
    sudo sysctl net.ipv6.conf.veth0.disable_ipv6=1
    sudo sysctl net.ipv6.conf.veth1.disable_ipv6=1
   ```
2. **Run the P4 Program:**
    Start the BMv2 switch with your P4 program:
    ```bash
    sudo simple_switch --interface 0@veth0 --interface 1@veth2 --interface 2@veth4 your_p4_program.json &
   ```
3. **Using Scapy for Packet Testing:**
    Run the Scapy script to send packets through the veth interfaces:
    ```bash
    sudo python3 /path/to/send_packet.py
   ```


## Additional Resources
- **P4 Guide Repository**: [jafingerhut/p4-guide](https://github.com/jafingerhut/p4-guide)
- **Scapy Documentation**: [Scapy Official Documentation](https://scapy.net/)
- **Getting Started with P4** (https://opennetworking.org/news-and-events/blog/getting-started-with-p4/)

## Conclusion
This document provides guidelines for using specific repositories to analyze the impact of coding assistants and AI tools on P4 programming. The focus is on identifying potential security vulnerabilities and differences from standard P4 coding practices.
