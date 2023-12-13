import pyshark
import pandas as pd
import os


def analyze_pcap(file_path):
    cap = pyshark.FileCapture(file_path)
    cap.set_debug(True)

    data = []

    try:
        for packet in cap:
            try:
                data.append({
                    'protocol': packet.transport_layer,
                    'src_addr': packet.ip.src,
                    'src_port': packet[packet.transport_layer].srcport,
                    'dst_addr': packet.ip.dst,
                    'dst_port': packet[packet.transport_layer].dstport
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
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    pcap_files = ["./output_files/traffic_veth1.pcap",
                  "./output_files/traffic_veth3.pcap",
                  "./output_files/traffic_veth5.pcap"]

    for file in pcap_files:
        df = analyze_pcap(file)

        # Construct a CSV filename based on the pcap filename
        csv_filename = os.path.splitext(file)[0] + '.csv'
        save_dataframe_to_csv(df, csv_filename)
