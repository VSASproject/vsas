import matplotlib.pyplot as plt

import pandas as pd

def setup_plt():
    fs = (16, 9,)
    dpi = 300
    plt.rcParams['figure.figsize'] = [16, 9]
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['pdf.fonttype'] = 42
setup_plt()

data = pd.read_csv("output_vpcc.csv")
QoE = data['QoE'].values.tolist()
plt.tick_params(pad=18, labelsize=20)
plt.plot(list(range(len(QoE))), QoE, color="red", linestyle="dashdot",
        label="Poor 4G", linewidth=4)

plt.xlabel("Chunk Number", fontsize=20)
plt.ylabel("QoE Score", fontsize=20)
plt.title("Real-time QoE Score", fontsize=30)
plt.legend(loc='upper right', fontsize=20)


plt.show()