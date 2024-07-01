import numpy as np
import csv

# SDFP
packets_csv = np.genfromtxt('packets.csv', delimiter=",")
dt_packets = packets_csv[:]
sdfp = np.std(dt_packets)

#SDFB
bytes_csv = np.genfromtxt('bytes.csv', delimiter=",")
dt_bytes = bytes_csv[0]
sdfb = np.std(dt_bytes)

# nIP & SSIP
n_ip = np.prod(dt_bytes.shape)
ssip = n_ip // 3

# SFE
sfe = n_ip // 3

# RFIP
file_one = None
file_two = None

with open('ipsrc.csv', 'r' ) as f1, open('ipdst.csv', 'r') as f2:
    file_one = f1.readlines()
    file_two = f2.readlines()

with open('intflow.csv', 'w') as f:
    for line in file_one:
        if line not in file_two:
            f.write

with open('intflow.csv') as f:
    reader = csv.reader(f, delimiter=',')
    dt = list(reader)
    row_count_non_int = len(dt)

rfip = abs(float(n_ip - row_count_non_int)/n_ip)

headers = ['SSIP', 'SDFP', 'SDFB', 'SFE', 'RFIP']
features = [ssip, sdfp, sdfb, sfe, rfip]

with open('/home/antonio/Desktop/NCI/code/tracker/rt_data.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=',')
    cursor.writerow(headers)
    cursor.writerow(features)

    f.close()
