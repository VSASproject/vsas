import numpy as np
import subprocess

throughput_list = np.loadtxt("throughput.csv", delimiter=",")

for bandwidth in throughput_list:
    bandwidth = int(bandwidth)
    if bandwidth == 0:
        bandwidth = 10
    subprocess.call("sudo ./network_emulator.sh eth0:" + str(bandwidth)
                    + "mbit:" + str(bandwidth) + "mbit:0ms:0%", shell=True)
    subprocess.call("go run testing_server.go", shell=True)

subprocess.call("sudo ./network_emulator.sh remove", shell=True)