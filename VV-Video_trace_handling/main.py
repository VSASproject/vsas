import csv
import re

chunk_length = 558

form_end = r'Chunk  arrived.'
form_time = r'\d+:\d+:(\d+\.\d+)'
form_start = r'failed to sufficiently increase receive buffer size'
form_normal = r'Nal File'

chunk_counter = 0
file_counter = 0
current_sec = 0
received_size = 0
sizelist = [30, 10, 7458, 8109, 3779, 10694, 4124, 2299, 8702, 4040, 11781, 4385, 7420, 3103, 8360, 3654, 8026, 4161, 10353, 4095, 8691, 4117, 10976, 5399, 8884, 10323, 5068, 11850, 5157, 2750, 11200, 4405, 9775, 4356, 9198, 4718, 10880, 4606, 10080, 4051, 8566, 3891, 10996, 3964, 9679, 3100, 8554, 7518, 3105, 9879, 3597, 2711, 9327, 3211, 8112, 2561, 6976, 2596, 9173, 3135, 7785, 3071, 11112, 3260, 6510, 2563, 9419, 3363, 8313, 7773, 2881, 8936, 2496, 2592, 6327, 2234, 9024, 3220, 7811, 2761, 8563, 2519, 6266, 2197, 4169, 2237, 30, 10, 24696, 9412, 3207, 6942, 8565, 2668, 7493, 2842, 9256, 3615, 2500, 7930, 3309, 9592, 3244, 8303, 3388, 9032, 3939, 9592, 3702, 8146, 2993, 7594, 3356, 18868, 7518, 5242, 4222, 3182, 2765, 6506, 2593, 6039, 2864, 6459, 10124, 4440, 8166, 4159, 10841, 4536, 10155, 4149, 8742, 4095, 8358, 9295, 4950, 11298, 3936, 2507, 7589, 3502, 10764, 4217, 8217, 3361, 10386, 3525, 5318, 2605, 9603, 4087, 8540, 4044, 10632, 4158, 2695, 2308, 2285, 1973, 2294, 2452, 2493, 2254, 2532, 2392, 1123, 1844, 1676, 1914, 2327, 2278, 2343, 1313, 2695, 2257, 2216, 2231, 3004, 3176, 2906, 2823, 2820, 2810, 2394, 2382, 2466, 2536, 1487, 2569, 2484, 2521, 2520, 2324, 2141, 1598, 2198, 2534, 2322, 2400, 1981, 1620, 1667, 1732, 2258, 1976, 2102, 1863, 1619, 1459, 690, 1671, 1526, 1665, 1836, 2152, 1756, 1874, 1709, 1869, 1719, 1485, 1553, 2013, 2138, 1810, 1900, 1701, 1320, 1300, 1736, 2133, 1773, 1460, 1844, 1936, 1878, 1311, 1415, 1751, 1504, 2239, 1939, 2103, 1755, 1507, 1592, 1762, 2511, 1929, 1711, 2127, 2011, 1798, 1619, 1808, 2243, 2462, 2146, 1618, 2322, 1930, 1840, 1626, 1848, 2408, 2527, 2347, 1688, 1869, 1776, 1599, 1792, 2018, 2509, 2735, 2368, 2292, 1115, 2829, 2538, 2691, 2309, 2337, 2440, 2661, 2693, 2483, 1980, 2007, 2245, 2577, 2500, 1031, 1950, 2042, 2255, 1778, 1416, 1547, 1253, 2045, 2758, 2361, 2559]
flag = True

header = ["Chunk_num"]
for i in range(chunk_length):
    header.append("index " + str(i))
header.append("total time (ms)")
header.append("Received Size (MB)")
header.append("throughput (Mbit/s)")
header.append("QoE")

file_list = ["-1"] * chunk_length
chunk_time = 0

def QoE_func(stalling_time, psnr):
    alpha = 2
    beta = 0.5
    return alpha*psnr - beta * stalling_time + 50

with open("output_vpcc.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for log_line in open("stall_timing_logs/stall_timing_4G0.8_VPCC.log"):
        match_pattern = re.search(form_time, log_line.replace(',', '.'))
        if re.search(form_start, log_line):
            current_sec = float(match_pattern.group(1))
            chunk_time = 0
            received_size = 0
            file_list = ["-1"] * chunk_length
        elif re.search(form_normal, log_line):
            temp = float(match_pattern.group(1))
            if temp < current_sec:
                diff = temp + 60 - current_sec
            else:
                diff = temp - current_sec
            delay = 1000 * diff  # ms
            if delay > 1000:
                delay = 1000
            chunk_time += delay
            current_sec = float(match_pattern.group(1))
            file_list[file_counter] = str(delay)
            #received_size += sizelist[file_counter]
            file_counter += 1
        elif re.search(form_end, log_line):
            chunk_counter += 1
            file_counter = 0
            if chunk_time == 0:
                continue
            throughput = str(100000/chunk_time * 0.01)
            if file_list[-1] == "-1":
                chunk_time = chunk_time * 558/file_list.index("-1") * 1.2
            chunk_time = chunk_time/1000 - 1
            if chunk_time < 0:
                chunk_time = 0
            writer.writerow([str(chunk_counter)] + file_list + [str(chunk_time * 1000)]  + [str(received_size/1000000)]
                            + [throughput] + [str(QoE_func(chunk_time, 15))])

chunk_length = 30
header = ["Chunk_num"]
for i in range(chunk_length):
    header.append("index " + str(i))
header.append("total time (ms)")
header.append("Received Size (MB)")
header.append("throughput (Mbit/s)")
header.append("QoE")
file_list = ["-1"] * chunk_length
chunk_counter = 0
file_counter = 0
with open("output_drc.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for log_line in open("stall_timing_logs/stall_timing_4G_DRC.log"):
        match_pattern = re.search(form_time, log_line.replace(',', '.'))
        if re.search(form_start, log_line):
            current_sec = float(match_pattern.group(1))
            chunk_time = 0
            file_list = ["-1"] * chunk_length
        elif re.search(form_normal, log_line):
            temp = float(match_pattern.group(1))
            if temp < current_sec:
                diff = temp + 60 - current_sec
            else:
                diff = temp - current_sec
            delay = 1000 * diff  # ms
            chunk_time += delay
            current_sec = float(match_pattern.group(1))
            file_list[file_counter] = str(delay)
            file_counter += 1
        elif re.search(form_end, log_line):
            chunk_counter += 1
            file_counter = 0
            if chunk_time == 0:
                continue
            throughput = str(70000000/chunk_time * 0.01)
            if file_list[-1] == "-1":
                chunk_time = chunk_time * 30/29
            chunk_time = chunk_time/1000 - 1
            if chunk_time < 0:
                chunk_time = 0
            writer.writerow([str(chunk_counter)] + file_list + [str(chunk_time * 1000)]  + [str(received_size/1000000)]
                            + [throughput] + [str(QoE_func(chunk_time, 45))])

chunk_length = 30
header = ["Chunk_num"]
for i in range(chunk_length):
    header.append("index " + str(i))
header.append("total time (ms)")
header.append("Received Size (MB)")
header.append("throughput (Mbit/s)")
header.append("QoE")
file_list = ["-1"] * chunk_length
chunk_counter = 0
file_counter = 0
with open("output_Mesh.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for log_line in open("stall_timing_logs/stall_timing_4G0.8_Mesh.log"):
        match_pattern = re.search(form_time, log_line.replace(',', '.'))
        if re.search(form_start, log_line):
            current_sec = float(match_pattern.group(1))
            chunk_time = 0
            file_list = ["-1"] * chunk_length
        elif re.search(form_normal, log_line):
            temp = float(match_pattern.group(1))
            if temp < current_sec:
                diff = temp + 60 - current_sec
            else:
                diff = temp - current_sec
            delay = 1000 * diff  # ms
            chunk_time += delay
            current_sec = float(match_pattern.group(1))
            file_list[file_counter] = str(delay)
            file_counter += 1
        elif re.search(form_end, log_line):
            chunk_counter += 1
            file_counter = 0
            if chunk_time == 0:
                continue
            throughput = str(70000000/chunk_time * 0.01)
            if file_list[-1] == "-1":
                chunk_time = chunk_time * 30/29
            chunk_time = chunk_time/1000 - 1
            if chunk_time < 0:
                chunk_time = 0
            writer.writerow([str(chunk_counter)] + file_list + [str(chunk_time * 1000)]  + [str(received_size/1000000)]
                            + [throughput] + [str(QoE_func(chunk_time, 45))])