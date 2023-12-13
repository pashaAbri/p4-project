import os
from scapy.all import sendp, IP, TCP, Ether, Raw, RandIP, RandMAC
import random
import time
import ipaddress

OUTPUT_FILES = 'output_files'


def ensure_output_directory(directory=OUTPUT_FILES):
    """Ensure that the output directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_traffic(dst_subnet, dst_port, num_packets, iface, payload_size=100, delay=0.1):
    dst_network = ipaddress.ip_network(dst_subnet)

    for _ in range(num_packets):
        # Random source IP and MAC addresses for variation
        src_ip = RandIP()
        src_mac = RandMAC()

        # Random destination IP within the subnet
        dst_ip = str(random.choice(list(dst_network.hosts())))

        # Random source port
        src_port = random.randint(1024, 65535)

        # Payload that might cause buffer overflow if improperly handled
        # This is a string of 'A's of the specified payload size
        payload = "A" * payload_size

        # Constructing the Ethernet and IP/TCP layers with Raw payload
        packet = Ether(src=src_mac) / IP(dst=dst_ip, src=src_ip) / TCP(sport=src_port, dport=dst_port) / Raw(
            load=payload)

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
    payload_size = 1200  # Size of the payload to test buffer overflow

    ensure_output_directory()

    for interface in interfaces:
        for subnet in subnets:
            print(f"Sending packets to subnet {subnet} with potential overflow payload via interface {interface}\n")
            generate_traffic(subnet, destination_port, number_of_packets, interface, payload_size, packet_delay)
