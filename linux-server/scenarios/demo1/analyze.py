import pyshark
import pandas as pd
import os

# Define a threshold payload size that is considered suspicious
SUSPICIOUS_PAYLOAD_SIZE = 1000  # Adjust this value as necessary


def analyze_pcap(file_path):
    cap = pyshark.FileCapture(file_path, only_summaries=False)
    cap.set_debug(True)

    data = []

    try:
        for packet in cap:
            try:
                # Check if the payload length is greater than the suspicious size
                payload_len = int(packet.tcp.len) if 'TCP' in packet and hasattr(packet.tcp, 'len') else 0
                if payload_len > SUSPICIOUS_PAYLOAD_SIZE:
                    data.append({
                        'protocol': packet.transport_layer,
                        'src_addr': packet.ip.src,
                        'src_port': packet[packet.transport_layer].srcport,
                        'dst_addr': packet.ip.dst,
                        'dst_port': packet[packet.transport_layer].dstport,
                        'payload_len': packet.tcp.len
                    })
            except AttributeError:
                # Skipping non TCP/UDP packets or packets missing IP layer
                continue
    except Exception as e:
        print(f"Error processing pcap file: {e}")
    finally:
        cap.close()

    return pd.DataFrame(data)


def save_dataframe_to_csv(df, filename):
    if not df.empty:
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print(f"No data to save for {filename}")


if __name__ == "__main__":
    pcap_files = ["./output_files/traffic_veth1.pcap",
                  "./output_files/traffic_veth3.pcap",
                  "./output_files/traffic_veth5.pcap"]

    for file in pcap_files:
        print(f"Analyzing {file}...")
        df = analyze_pcap(file)

        # Filter out normal traffic if you only want to save suspicious packets
        df_suspicious = df[df['payload_len'] > SUSPICIOUS_PAYLOAD_SIZE]

        # Construct a CSV filename based on the pcap filename
        csv_filename = os.path.splitext(file)[0] + '_suspicious.csv'
        save_dataframe_to_csv(df_suspicious, csv_filename)
