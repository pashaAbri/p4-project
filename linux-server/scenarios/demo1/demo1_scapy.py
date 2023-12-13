import os
from scapy.all import sendp, IP, TCP, Ether, RandIP, RandMAC
import random
import time
import ipaddress
import subprocess

OUTPUT_FILES = 'output_files'


def ensure_output_directory(directory=OUTPUT_FILES):
    """Ensure that the output directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def start_tcpdump(iface, output_directory=OUTPUT_FILES):
    """Start tcpdump on the specified interface and return the process handle."""
    filename = f"{output_directory}/traffic_{iface}.pcap"
    cmd = ["sudo", "tcpdump", "-i", iface, "-w", filename]
    process = subprocess.Popen(cmd)
    print(f"Started tcpdump on {iface}, saving to {filename}\n")
    return process


def generate_traffic(dst_subnet, dst_port, num_packets, iface, delay=0.1):
    dst_network = ipaddress.ip_network(dst_subnet)

    for _ in range(num_packets):
        # Random source IP and MAC addresses for variation
        src_ip = RandIP()
        src_mac = RandMAC()

        # Random destination IP within the subnet
        dst_ip = str(random.choice(list(dst_network.hosts())))

        # Random source port
        src_port = random.randint(1024, 65535)

        # Constructing the Ethernet and IP/TCP layers
        packet = Ether(src=src_mac) / IP(dst=dst_ip, src=src_ip) / TCP(sport=src_port, dport=dst_port)

        # Sending the packet on specified interface
        sendp(packet, iface=iface, verbose=False)

        # Delay between packet sends
        time.sleep(delay)


if __name__ == '__main__':
    subnets = ["10.10.0.0/16", "11.11.0.0/16", "12.12.0.0/16", "20.20.20.0/24"]
    destination_port = 80  # Common port for testing
    number_of_packets = 10  # Number of packets to send for each subnet
    interfaces = ["veth1", "veth3", "veth5"]  # List of veth interfaces
    packet_delay = 0.05  # Delay between packets

    ensure_output_directory()

    tcpdump_processes = []
    for iface in interfaces:
        process = start_tcpdump(iface)
        tcpdump_processes.append(process)

    try:
        for interface in interfaces:
            for subnet in subnets:
                print(f"Sending packets to subnet {subnet} via interface {interface}\n")
                generate_traffic(subnet, destination_port, number_of_packets, interface, packet_delay)
    finally:
        # Terminate all tcpdump processes
        for process in tcpdump_processes:
            process.terminate()
            process.wait()  # Wait for the process to terminate
        print("All tcpdump processes have been terminated.")
