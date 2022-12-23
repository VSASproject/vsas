import csv
import re
import numpy as np

form_end = r'Chunk  arrived.'
form_time = r'\d+:\d+:(\d+\.\d+)'
form_start = r'failed to sufficiently increase receive buffer size'
form_normal = r'Nal File'

low = [42.38, 53.56, 66.61]
Medium = [45.46, 55.93, 68.36]
High = [48.59, 59.08, 69.60]
Very_High = [51.51, 61.39, 70.81]

chunk_length = 558

def QoE_func(stalling_time, psnr):
    alpha = 2
    beta = 0.5
    return alpha*psnr - beta * stalling_time + 50

def extract_log(input_file, output_file, chunk_length, throughput_file, indicator):
    throughput_list = np.loadtxt(throughput_file, delimiter=",")
    chunk_counter = 0
    file_counter = 0
    current_sec = 0
    header = ["Chunk_num"]
    for i in range(chunk_length):
        header.append("index " + str(i))
    header.append("stalling time")
    header.append("PSNR")
    header.append("Chunk Bitrate")
    header.append("QoE")
    file_list = ["-1"] * chunk_length
    chunk_time = 0
    with open(output_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for log_line in open(input_file):
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
                if delay > 1000:
                    delay = 1000
                chunk_time += delay
                current_sec = float(match_pattern.group(1))
                file_list[file_counter] = str(delay)
                # received_size += sizelist[file_counter]
                file_counter += 1
            elif re.search(form_end, log_line):
                file_counter = 0
                if chunk_time == 0:
                    continue
                if file_list[-1] == "-1":
                    chunk_time = chunk_time * chunk_length / file_list.index("-1") * 1.2

                chunk_time = chunk_time / 1000 - 1
                throughput = throughput_list[chunk_counter]
                if chunk_time < 0:
                    chunk_time = 0
                if throughput < 12:
                    PSNR = low[indicator]
                    bitrate = 7
                elif throughput < 25:
                    PSNR = Medium[indicator]
                    bitrate = 12
                elif throughput < 50:
                    PSNR = High[indicator]
                    bitrate = 25
                else:
                    PSNR = Very_High[indicator]
                    bitrate = 50
                chunk_counter += 1
                writer.writerow(
                    [str(chunk_counter)] + file_list + [str(chunk_time * 1000)] + [str(PSNR)]
                    + [str(bitrate)] + [str(QoE_func(chunk_time * 1000, PSNR))])


extract_log("stall_timing_logs/stall_timing_4G0.8_VPCC.log", "VPCC_csv/4G_1.csv", 558, "throughputs/throughput.csv", 2)
extract_log("stall_timing_logs/stall_timing_Wifi0.8_VPCC.log", "VPCC_csv/Wifi_1.csv", 558, "throughputs/throughput_wifi_1.csv", 2)
extract_log("stall_timing_logs/stall_timing_5G0.8_VPCC.log", "VPCC_csv/5G_1.csv", 558, "throughputs/throughput_5G_1.csv", 2)

extract_log("stall_timing_logs/stall_timing_4G0.8_Mesh.log", "Mesh_csv/4G_1.csv", 30, "throughputs/throughput.csv", 0)
extract_log("stall_timing_logs/stall_timing_Wifi0.8_Mesh.log", "Mesh_csv/Wifi_1.csv", 30, "throughputs/throughput_wifi_1.csv", 0)
extract_log("stall_timing_logs/stall_timing_5G0.8_Mesh.log", "Mesh_csv/5G_1.csv", 30, "throughputs/throughput_5G_1.csv", 0)

extract_log("stall_timing_logs/stall_timing_4G0.8_DRC.log", "DRC_csv/4G_1.csv", 30, "throughputs/throughput.csv", 1)
extract_log("stall_timing_logs/stall_timing_Wifi0.8_drc.log", "DRC_csv/Wifi_1.csv", 30, "throughputs/throughput_wifi_1.csv", 1)
extract_log("stall_timing_logs/stall_timing_5G0.8_drc.log", "DRC_csv/5G_1.csv", 30, "throughputs/throughput_5G_1.csv", 1)
