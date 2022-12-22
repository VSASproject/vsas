import subprocess
import time


Limit = 500

subprocess.call("rm stall_timing.log", shell=True)

for i in range(Limit):
    print("Packet:", str(i))
    subprocess.call("go run ply_testing_client.go", shell=True)

