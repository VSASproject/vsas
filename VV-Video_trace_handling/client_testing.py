import subprocess

Limit = 441

subprocess.call("rm stall_timing_vpcc.log", shell=True)

for i in range(Limit):
    subprocess.call("go run testing_client.go", shell=True)
