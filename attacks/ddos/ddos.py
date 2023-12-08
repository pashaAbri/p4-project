from scapy.all import sendp, IP, TCP, Ether, RandIP, RandMAC
import random


def generate_traffic(dst_ip, dst_port, num_packets):
    for _ in range(num_packets):
        # Random source IP and MAC addresses for variation
        src_ip = RandIP()
        src_mac = RandMAC()

        # Constructing the Ethernet and IP/TCP layers
        packet = Ether(src=src_mac) / IP(dst=dst_ip, src=src_ip) / TCP(dport=dst_port)

        # Sending the packet
        sendp(packet)


# Example usage
if __name__ == '__main__':
    target_ip = "192.168.1.100"  # Target IP address of your P4 program
    target_port = 80  # Target port
    number_of_packets = 100  # Number of packets to send

    generate_traffic(target_ip, target_port, number_of_packets)
