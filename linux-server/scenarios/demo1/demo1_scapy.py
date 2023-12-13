from scapy.all import sendp, IP, TCP, Ether, RandIP, RandMAC
import random
import time
import ipaddress

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
        sendp(packet, iface=iface)

        # Delay between packet sends
        time.sleep(delay)

# Example usage
if __name__ == '__main__':
    subnets = ["10.10.0.0/16", "11.11.0.0/16", "12.12.0.0/16", "20.20.20.0/24"]
    destination_port = 80  # Common port for testing
    number_of_packets = 100  # Number of packets to send for each subnet
    interfaces = ["veth1", "veth3", "veth5"]  # List of veth interfaces
    packet_delay = 0.05  # Delay between packets

    for interface in interfaces:
        for subnet in subnets:
            print(f"Sending packets to subnet {subnet} via interface {interface}")
            generate_traffic(subnet, destination_port, number_of_packets, interface, packet_delay)
