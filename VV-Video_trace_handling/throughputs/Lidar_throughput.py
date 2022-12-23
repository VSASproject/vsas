import numpy as np
import matplotlib.pyplot as plt

_4G_throughput = np.loadtxt("throughput.csv", delimiter=",")
_5G_throughput = np.loadtxt("throughput_5G_1.csv", delimiter=",")
_wifi_throughput = np.loadtxt("throughput_wifi_1.csv", delimiter=",")

_001_bits = 30 * 30 * 8/1000  #Mb
_002_bits = 30 * 60 * 8/1000
_005_bits = 30 * 150 * 8/1000
_01_bits = 30 * 280 * 8/1000
_02_bits = 30 * 560 * 8/1000

GENERAL = []

for i in range(5):
    GENERAL.append([])
    for j in range(3):
        GENERAL[i].append([])

if_ms = 1000

for row_index in range(400):
    _4G = _4G_throughput[row_index]
    if _4G < 5:
        _4G = 5
    _5G = _5G_throughput[row_index]
    if _5G < 5:
        _5G = 5
    _wifi = _wifi_throughput[row_index]
    if _wifi < 5:
        _wifi = 5
    GENERAL[0][0].append(_001_bits/_4G * if_ms)
    GENERAL[0][1].append(_001_bits / _wifi * if_ms)
    GENERAL[0][2].append(_001_bits / _5G * if_ms)
    GENERAL[1][0].append(_002_bits / _4G * if_ms)
    GENERAL[1][1].append(_002_bits / _wifi * if_ms)
    GENERAL[1][2].append(_002_bits / _5G * if_ms)
    GENERAL[2][0].append(_005_bits / _4G * if_ms)
    GENERAL[2][1].append(_005_bits / _wifi * if_ms)
    GENERAL[2][2].append(_005_bits / _5G * if_ms)
    GENERAL[3][0].append(_01_bits / _4G * if_ms)
    GENERAL[3][1].append(_01_bits / _wifi * if_ms)
    GENERAL[3][2].append(_01_bits / _5G * if_ms)
    GENERAL[4][0].append(_02_bits / _4G * if_ms)
    GENERAL[4][1].append(_02_bits / _wifi * if_ms)
    GENERAL[4][2].append(_02_bits / _5G * if_ms)

def setup_plt():
    fs = (16, 9,)
    dpi = 300
    plt.rcParams['figure.figsize'] = [16, 12]
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams["legend.handlelength"] = 1.0
    plt.rcParams['hatch.linewidth'] = 3


def auto_label(rects):
    for rect in rects:
        height = round(rect.get_height(), 1) + 1
        plt.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    fontsize=45,
                    rotation=90,
                    textcoords="offset points",
                    ha='center', va='bottom')


setup_plt()
FULL = [int(np.mean(GENERAL[4][0])), int(np.mean(GENERAL[4][1])), int(np.mean(GENERAL[4][2]))]
PART = [int(np.mean(GENERAL[0][0]) + 0.1 * np.mean(GENERAL[4][0])),
        int(np.mean(GENERAL[0][1]) + 0.1 * np.mean(GENERAL[4][1])),
        int(np.mean(GENERAL[0][2]) + 0.1 * np.mean(GENERAL[4][2]))]

x = list(range(len(FULL)))
total_width, n = 0.7, len(FULL)
width = total_width/n
rect1_ = plt.bar(x, FULL, width=width, color='white', edgecolor="black", ls='-', lw=7)
rect1 = plt.bar(x, FULL, width=width, label='full size',color='white', edgecolor="red",
                    hatch='+', alpha=0.6)
for i in range(len(x)):
    x[i] = x[i] + width + 0.01
rect2_ = plt.bar(x, PART, width=width, color='white', edgecolor="black", ls='-', lw=7)
rect2 = plt.bar(x, PART, width=width, label='optimization',color='white', edgecolor="blue",
                    hatch='/')
name_list = ["4G", "WiFi", "5G"]
plt.ylabel('Transmission Delay (ms)',fontsize=50)
auto_label(rect1)
auto_label(rect2)
plt.legend(loc='upper right',fontsize=40,edgecolor="black")
for i in range(len(x)):
    x[i] = x[i] - width * 0.5
plt.xticks(x, name_list, fontsize=50)
plt.ylim(0, 6000)
plt.yticks(fontsize=40)
plt.savefig("lidar_delay.pdf",bbox_inches = 'tight')
plt.show()
