import matplotlib.pyplot as plt
import numpy as np

throughput_list = np.loadtxt("throughputs/throughput.csv", delimiter=",")
true_bandwidth = []
choosen_bitrate = []
dropping_bitrate = []
for throughput in throughput_list:
    true_bandwidth.append(throughput * 0.8)
    if throughput < 12:
        choosen_bitrate.append(7)
        dropping_bitrate.append(min(throughput * 0.8 - 1, 7))
    elif throughput < 25:
        choosen_bitrate.append(12)
        dropping_bitrate.append(min(throughput * 0.8 - 1, 12))
    elif throughput < 50:
        choosen_bitrate.append(25)
        dropping_bitrate.append(min(throughput * 0.8 - 1, 25))
    else:
        choosen_bitrate.append(50)
        dropping_bitrate.append(min(throughput * 0.8 - 1, 50))



def setup_plt():
    fs = (16, 9,)
    dpi = 300
    plt.rcParams['figure.figsize'] = [40, 12]
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['pdf.fonttype'] = 42
setup_plt()

for i in range(0, len(choosen_bitrate)-5, 5):
    choosen_bitrate[i + 1] = choosen_bitrate[i]
    choosen_bitrate[i + 2] = choosen_bitrate[i]
    choosen_bitrate[i + 3] = choosen_bitrate[i]
    choosen_bitrate[i + 4] = choosen_bitrate[i]

for i in range(0, len(dropping_bitrate)):
    if dropping_bitrate[i] > choosen_bitrate[i]:
        dropping_bitrate[i] = choosen_bitrate[i]


plt.tick_params(pad=18, labelsize=32)
plt.plot(list(range(len(true_bandwidth))), true_bandwidth, color="black", #linestyle="dashdot",
        label="True Bandwidth", linewidth=6, marker='o', ms=25)
plt.plot(list(range(len(choosen_bitrate))), choosen_bitrate, color="red", linestyle="dashdot",
        label="VPCC ABR", linewidth=6, marker='*', ms=25)
plt.plot(list(range(len(dropping_bitrate))), dropping_bitrate, color="blue", linestyle="dotted",
        label="VPCC ABR + FrameDrop", linewidth=6, marker='p', ms=25)

plt.xlim(0, 100)
plt.ylim(10, 65)

plt.xlabel("Time (Sec)", fontsize=70)
plt.ylabel("Bandwidth (Mbps)", fontsize=70)
#plt.title("Real-time Bitrate and True Bandwidth", fontsize=30)
plt.legend(loc='upper right', fontsize=50, ncol=3)
plt.savefig("Output/real_time_0s-75s.pdf",bbox_inches = 'tight')

plt.show()