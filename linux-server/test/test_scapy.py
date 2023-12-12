from scapy.all import Ether, IP, UDP, sendp

def send_packet(interface, dst_ip):
    # Creating the packet
    packet = Ether()/IP(dst=dst_ip)/UDP()

    # Sending the packet
    sendp(packet, iface=interface)

    print(f"Packet sent on {interface} to destination {dst_ip}")


if __name__ == "__main__":
    # Set the interface and destination IP for the packets
    interface = "veth1"
    destination_ip_1 = "11.11.1.1"
    send_packet(interface, destination_ip_1)

    destination_ip_2 = "12.12.1.1"
    send_packet(interface, destination_ip_2)

