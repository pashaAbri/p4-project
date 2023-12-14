import os
import random
import time
import ipaddress
from scapy.all import sendp, IP, TCP, Ether, Raw, RandIP, RandMAC

OUTPUT_FILES = 'output_files'


def ensure_output_directory(directory=OUTPUT_FILES):
    """Ensure that the output directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_checksum_spoof_traffic(dst_subnet, dst_port, num_packets, iface, normal_payload_size=100,
                                    overflow_payload_size=1200, delay=0.1):
    """Generate traffic with the option of spoofing the checksum."""
    dst_network = ipaddress.ip_network(dst_subnet)

    for _ in range(num_packets):
        src_ip = RandIP()
        src_mac = RandMAC()
        dst_ip = str(random.choice(list(dst_network.hosts())))
        src_port = random.randint(1024, 65535)

        # Decide whether to generate a normal packet or one that may cause overflow
        if random.random() < 0.5:  # 50% chance
            payload = int(normal_payload_size) / 2
            packet = Ether(src=src_mac) / IP(dst=dst_ip, src=src_ip, chksum=0x1234) / TCP(sport=src_port,
                                                                                          dport=dst_port) / Raw(
                load=payload)
        else:
            payload = int(normal_payload_size)
            packet = Ether(src=src_mac) / IP(dst=dst_ip, src=src_ip) / TCP(sport=src_port, dport=dst_port) / Raw(
                load=payload)

        sendp(packet, iface=iface, verbose=False)
        time.sleep(delay)


if __name__ == '__main__':
    subnets = ["10.10.0.0/16", "11.11.0.0/16", "12.12.0.0/16", "20.20.20.0/24"]
    destination_port = 80  # Common port for testing
    number_of_packets = 100  # Number of packets to send for each subnet
    interfaces = ["veth1", "veth3", "veth5"]  # List of veth interfaces
    packet_delay = 0.05  # Delay between packets
    payload_size = 1024  # Size of the payload

    ensure_output_directory()

    for interface in interfaces:
        for subnet in subnets:
            print(f"Sending packets to subnet {subnet} with potentially spoofed checksum via interface {interface}\n")
            generate_checksum_spoof_traffic(subnet, destination_port, number_of_packets, interface, payload_size,
                                            delay=packet_delay)
