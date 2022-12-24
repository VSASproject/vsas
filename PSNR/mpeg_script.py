import subprocess

min_QP = 15
max_QP = 35
sequence_config = "redandblack_vox10.cfg"

subprocess.call("mkdir cache", shell=True)
for QP in range(min_QP, max_QP + 1):
    with open('cfg/rate/ctc-me.cfg', 'w') as qp_config_file:
        qp_config_file.write("geometryQP: " + str(QP) + "\n")
        qp_config_file.write("attributeQP: " + str(QP) + "\n")
        qp_config_file.write("occupancyPrecision: 4" + "\n")
    subprocess.call("./bin/PccAppEncoder       "
                    "--configurationFolder=cfg/      "
                    "--config=cfg/common/ctc-common.cfg      "
                    "--config=cfg/condition/ctc-all-intra.cfg        "
                    "--config=cfg/sequence/"+ sequence_config + "       "
                    "--config=cfg/rate/ctc-me.cfg    "
                    "--uncompressedDataFolder=./data/         "
                    "--frameCount=1  --reconstructedDataPath=S"+ str(QP) +".ply       "
                    "--compressedStreamPath=S"+ str(QP) + ".bin", shell=True)
    subprocess.call("mv S" + str(QP) + "* cache/", shell=True)
