import subprocess
import time
import csv
import os

n = 4  # number of switches
iterations = 2000

#Flow table information extracted
#NXST_FLOWreply(xid = 0 × 4) : cookie = 0 × 0,
#duration = 21.098s,
#table = 0,
#n_packets = 1,
#n_bytes = 42,
#idle_age = 21, #
#priority = 65535, tcp,
#in_port = 1,
#dl_src = 00 : 00 : 00 : 00 : 00 : 01,
#dl_dst = 00 : 00 : 00 : 00 : 00 : 02,
#nw_src = 95.141.141.242,
#tp_src=3786,
#tp_dst=0

del_flows = []

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e.stderr}")
        return None

def extract_field(data, field_name, delimiter=",", field_delimiter="="):
    extracted = []
    for row in data.splitlines():
        fields = row.split(delimiter)
        for field in fields:
            if field_name in field:
                extracted.append(field.split(field_delimiter)[1])
    return extracted

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    for i in range(1, iterations + 1):
        for j in range(1, n + 1):
            print(f"Inspection no. {i} at s{j}")

            # Extract essential data from raw data
            raw_data = run_command(f"sudo ovs-ofctl dump-flows s{j}")
            if raw_data is None:
                continue

            with open('raw', 'w') as raw_file:
                raw_file.write(raw_data)

            flowentries = [line for line in raw_data.splitlines() if "nw_src" in line]
            with open('flowentries.csv', 'w') as flowentries_file:
                flowentries_file.write("\n".join(flowentries))

            packets = extract_field(raw_data, "packets")
            bytes_data = extract_field(raw_data, "bytes")
            ipsrc = extract_field(raw_data, "nw_src")
            ipdst = extract_field(raw_data, "nw_dst")

            # Check if there are no traffics in the network at the moment
            if not packets or not bytes_data or not ipsrc or not ipdst:
                state = 0
            else:
                save_to_csv(packets, 'packets.csv')
                save_to_csv(bytes_data, 'bytes.csv')
                save_to_csv(ipsrc, 'ipsrc.csv')
                save_to_csv(ipdst, 'ipdst.csv')

                subprocess.run("python3 tuples.py", shell=True)
                subprocess.run("python3 inspector.py", shell=True)

                with open('.result', 'r') as result_file:
                    state = int(result_file.read().strip())

            if state == 1:
                print(f"Network is under attack occurring at s{j}")
                default_flow = run_command(f"sudo ovs-ofctl dump-flows s{j} | tail -n 1")
                run_command(f"sudo ovs-ofctl del-flows s{j}")
                run_command(f"sudo ovs-ofctl add-flow s{j} \"{default_flow.strip()}\"")
                run_command(f"killall hping3")
                print(default_flow)
        time.sleep(3)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    main()

