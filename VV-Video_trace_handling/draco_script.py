import os
import subprocess

path = "./longdress/Ply"
files = os.listdir(path)

for file in files:
    buffer = "./draco_encoder -point_cloud -i " + path + "/" + file + " -o " + os.path.splitext(file)[0] + ".drc"
    subprocess.call(buffer, shell=True)

subprocess.call("mv *.drc draco_output/")