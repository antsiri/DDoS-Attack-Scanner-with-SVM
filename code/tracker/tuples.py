import numpy as np
import csv

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

with open('rt_data.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=',')
    cursor.writerow(headers)
    cursor.writerow(features)

    f.close()
