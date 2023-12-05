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

## Additional Resources
- **P4 Guide Repository**: [jafingerhut/p4-guide](https://github.com/jafingerhut/p4-guide)
- **Scapy Documentation**: [Scapy Official Documentation](https://scapy.net/)

## Conclusion
This document provides guidelines for using specific repositories to analyze the impact of coding assistants and AI tools on P4 programming. The focus is on identifying potential security vulnerabilities and differences from standard P4 coding practices.
