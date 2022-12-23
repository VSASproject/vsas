import numpy as np
import csv

header = ["Mesh", "Draco", "VPCC"]
low = [42.38, 53.56, 66.61]
Medium = [45.46, 55.93, 68.36]
High = [48.59, 59.08, 69.60]
Very_High = [51.51, 61.39, 70.81]


def throughput_generation(throughput_file, output_file):
    throughput_list = np.loadtxt(throughput_file, delimiter=",")
    with open(output_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for throughput in throughput_list:
            if throughput < 12:
                writer.writerow(low)
            elif throughput < 25:
                writer.writerow(Medium)
            elif throughput < 50:
                writer.writerow(High)
            else:
                writer.writerow(Very_High)


throughput_generation("throughputs/throughput.csv", "Output/simulate_4G.csv")
throughput_generation("throughputs/throughput_wifi_1.csv", "Output/simulate_wifi.csv")
throughput_generation("throughputs/throughput_5G_1.csv", "Output/simulate_5G.csv")