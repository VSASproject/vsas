import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("output_vpcc.csv")
QoE = data.loc[:, ["QoE"]]

QoE['cdf'] = QoE['QoE'].rank(method = 'average', pct = True)
QoE = QoE.sort_values("QoE")

def setup_plt():
    fs = (16, 9,)
    dpi = 300
    plt.rcParams['figure.figsize'] = [16, 9]
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['pdf.fonttype'] = 42
setup_plt()

figure = plt.figure()
ax = figure.add_axes([0.115, 0.15, 0.8, 0.8])
ax.tick_params(pad=18, labelsize=36)
ax.plot(QoE["QoE"], QoE['cdf'], label="VPCC",
            linestyle="dashdot",
            color="b", linewidth=5)

data = pd.read_csv("output_drc.csv")
QoE = data.loc[:, ["QoE"]]

QoE['cdf'] = QoE['QoE'].rank(method = 'average', pct = True)
QoE = QoE.sort_values("QoE")
ax.plot(QoE["QoE"], QoE['cdf'], label="DRC",
            linestyle="--",
            color="r", linewidth=5)

plt.legend(loc='upper left', fontsize=20)
ax.set_xlabel("QoE Comparison", fontsize=40)
ax.set_ylim(0, 1)
ax.set_ylabel('CDF', fontsize=40)
#plt.savefig("Output_CDFs_Oculus_InGeneral/general_" + feature + ".pdf", bbox_inches='tight')
plt.show()
figure.clf()