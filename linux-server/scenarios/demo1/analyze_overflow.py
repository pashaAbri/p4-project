import pyshark
import pandas as pd
import os


def analyze_pcap(file_path):
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
                length = int(packet[protocol].length)

                data.append({
                    'protocol': protocol,
                    'src_addr': src_addr,
                    'src_port': src_port,
                    'dst_addr': dst_addr,
                    'dst_port': dst_port,
                    'length': length
                })
            except AttributeError:
                # This will skip packets that aren't TCP/UDP or are missing an IP layer.
                continue
            except KeyError:
                # This will occur if a packet doesn't have a transport layer (protocol).
                continue
    except Exception as e:
        print(f"Error processing pcap file: {e}")
    finally:
        cap.close()

    return pd.DataFrame(data)


def mark_large_payloads(df, payload_size_threshold):
    """Mark packets with payload sizes larger than the threshold."""
    suspicious_packets = df[df['length'] > payload_size_threshold].copy()
    suspicious_packets['suspicious'] = 'Yes'
    return suspicious_packets


def save_dataframe_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    SUSPICIOUS_PAYLOAD_SIZE = 1000  # Define a threshold for suspicious payload size
    pcap_files = [
        "./output_files/traffic_veth1.pcap",
        "./output_files/traffic_veth3.pcap",
        "./output_files/traffic_veth5.pcap"
    ]

    for file_path in pcap_files:
        print(f"Analyzing {file_path}...")
        traffic_df = analyze_pcap(file_path)

        # Mark the suspicious packets
        suspicious_df = mark_large_payloads(traffic_df, SUSPICIOUS_PAYLOAD_SIZE)

        # Save the full traffic data and the suspicious packets separately
        traffic_csv_filename = os.path.splitext(file_path)[0] + '_traffic.csv'
        suspicious_csv_filename = os.path.splitext(file_path)[0] + '_suspicious.csv'
        save_dataframe_to_csv(traffic_df, traffic_csv_filename)
        save_dataframe_to_csv(suspicious_df, suspicious_csv_filename)
