import subprocess
import time


Limit = 441

subprocess.call("rm stall_timing.log", shell=True)

for i in range(Limit):
    subprocess.call("go run testing_client.go", shell=True)
    time.sleep(1)

