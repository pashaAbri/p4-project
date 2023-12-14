import pyshark
import pandas as pd
import os


def analyze_pcap(file_path, spoofed_payload_size):
    cap = pyshark.FileCapture(file_path, only_summaries=False)
    cap.set_debug(True)

    data = []

    try:
        for packet in cap:
            try:
                protocol = packet.transport_layer
                src_addr = packet.ip.src
                dst_addr = packet.ip.dst
                src_port = packet[protocol].srcport
                dst_port = packet[protocol].dstport
                length = int(packet.length)

                # Determine if packet is suspicious based on payload length
                suspicious = length == spoofed_payload_size

                data.append({
                    'protocol': protocol,
                    'src_addr': src_addr,
                    'src_port': src_port,
                    'dst_addr': dst_addr,
                    'dst_port': dst_port,
                    'length': length,
                    'suspicious': 'Yes' if suspicious else 'No'
                })
            except AttributeError:
                continue
            except KeyError:
                continue
    except Exception as e:
        print(f"Error processing pcap file: {e}")
    finally:
        cap.close()

    return pd.DataFrame(data)


def save_dataframe_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    SPOOFED_PAYLOAD_SIZE = 566
    pcap_files = [
        "./output_files/traffic_veth1.pcap",
        "./output_files/traffic_veth3.pcap",
        "./output_files/traffic_veth5.pcap"
    ]

    for file_path in pcap_files:
        print(f"Analyzing {file_path}...")
        traffic_df = analyze_pcap(file_path, SPOOFED_PAYLOAD_SIZE)
        traffic_csv_filename = os.path.splitext(file_path)[0] + '_traffic.csv'
        save_dataframe_to_csv(traffic_df, traffic_csv_filename)
