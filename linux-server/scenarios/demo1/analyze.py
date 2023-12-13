import pyshark


def analyze_pcap(file_path):
    # Initialize pyshark FileCapture with debug mode enabled
    cap = pyshark.FileCapture(file_path)
    cap.set_debug(True)

    try:
        # Iterate over packets and extract information
        for packet in cap:
            try:
                # Basic packet data
                protocol = packet.transport_layer  # Protocol type (TCP/UDP)
                src_addr = packet.ip.src  # Source IP address
                src_port = packet[packet.transport_layer].srcport  # Source port
                dst_addr = packet.ip.dst  # Destination IP address
                dst_port = packet[packet.transport_layer].dstport  # Destination port

                # Output packet details
                print(f"Packet: {protocol} {src_addr}:{src_port} -> {dst_addr}:{dst_port}")

            except AttributeError as e:
                # Handle packets that aren't TCP/UDP or are missing IP layer
                print("Non TCP/UDP packet detected or missing IP layer.")

    except Exception as e:
        print(f"Error processing pcap file: {e}")

    finally:
        # Ensure the capture is closed properly
        cap.close()


if __name__ == "__main__":
    pcap_file = "path/to/your/pcap_file.pcap"  # Replace with your pcap file path
    analyze_pcap(pcap_file)
