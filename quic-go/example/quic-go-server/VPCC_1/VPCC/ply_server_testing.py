import numpy as np
import subprocess
import time

throughput_list = np.loadtxt("throughput.csv", delimiter=",")
#throughput_list = np.loadtxt("throughput_wifi_1.csv", delimiter=",")
#throughput_list = np.loadtxt("throughput_5G_1.csv", delimiter=",")

for bandwidth in throughput_list:
    bandwidth = int(bandwidth)
    if bandwidth == 0:
        bandwidth = 10
    subprocess.call("sudo ./network_emulator.sh eth0:" + str(int(bandwidth * 0.8))
                   + "mbit:" + str(int(bandwidth * 0.8)) + "mbit:0ms:0%", shell=True)
    if bandwidth < 12:
        subprocess.call("go run ply_testing_server.go Mesh_500", shell=True)
    elif bandwidth < 25:
        subprocess.call("go run ply_testing_server.go Mesh_1000", shell=True)
    elif bandwidth < 50:
        subprocess.call("go run ply_testing_server.go Mesh_2000", shell=True)
    else:
        subprocess.call("go run ply_testing_server.go Mesh_4000", shell=True)

subprocess.call("sudo ./network_emulator.sh remove", shell=True)
