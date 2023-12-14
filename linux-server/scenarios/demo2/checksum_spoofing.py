import os
import random
import time
import ipaddress
from scapy.all import send, IP, TCP, Ether, Raw, RandIP, RandMAC

OUTPUT_FILES = 'output_files'


def ensure_output_directory(directory=OUTPUT_FILES):
    """Ensure that the output directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_checksum_spoof_traffic(dst_subnet, dst_port, num_packets, iface, normal_payload_size=100, delay=0.1):
    """Generate traffic with the option of spoofing the checksum."""
    dst_network = ipaddress.ip_network(dst_subnet)

    for _ in range(num_packets):
        src_ip = RandIP()
        dst_ip = str(random.choice(list(dst_network.hosts())))
        src_port = random.randint(1024, 65535)

        if random.random() < 0.5:  # 50% chance
            spoofed_checksum = True
            payload = "B" * int(normal_payload_size)
        else:
            spoofed_checksum = False
            payload = "A" * int(normal_payload_size)

        # Craft the packet
        if spoofed_checksum:
            packet = IP(dst=dst_ip, src=src_ip, chksum=0x1234) / TCP(sport=src_port, dport=dst_port) / Raw(load=payload)
        else:
            packet = IP(dst=dst_ip, src=src_ip) / TCP(sport=src_port, dport=dst_port) / Raw(load=payload)

        send(packet, iface=iface, verbose=False)
        time.sleep(delay)


if __name__ == '__main__':
    subnets = ["192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24"]  # Example subnets
    destination_port = 80  # Common port for testing
    number_of_packets = 50  # Number of packets to send for each subnet
    interfaces = ["veth1", "veth3", "veth5"]  # List of veth interfaces
    payload_size = 100  # Size of the payload
    packet_delay = 0.05  # Delay between packets

    ensure_output_directory()

    for interface in interfaces:
        for subnet in subnets:
            print(f"Sending packets to subnet {subnet} with correct checksum\n")
            generate_checksum_spoof_traffic(subnet, destination_port, number_of_packets, interface, payload_size,
                                            delay=packet_delay)
