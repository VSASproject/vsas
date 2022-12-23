import pandas as pd
import matplotlib.pyplot as plt

def setup_plt():
    fs = (16, 9,)
    dpi = 300
    plt.rcParams['figure.figsize'] = [16, 12]
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams["legend.handlelength"] = 1.0
    plt.rcParams['hatch.linewidth'] = 3

setup_plt()

def auto_label(rects):
    for rect in rects:
        height = round(rect.get_height(), 1)
        plt.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    fontsize=45,
                    rotation=90,
                    textcoords="offset points",
                    ha='center', va='bottom')

mesh_4G = pd.read_csv("Mesh_csv/4G_1.csv")
mesh_5G = pd.read_csv("Mesh_csv/5G_1.csv")
mesh_Wifi = pd.read_csv("Mesh_csv/Wifi_1.csv")

drc_4G = pd.read_csv("DRC_csv/4G_1.csv")
drc_5G = pd.read_csv("DRC_csv/5G_1.csv")
drc_Wifi = pd.read_csv("DRC_csv/Wifi_1.csv")

VPCC_4G = pd.read_csv("VPCC_csv/4G_1.csv")
VPCC_5G = pd.read_csv("VPCC_csv/5G_1.csv")
VPCC_Wifi = pd.read_csv("VPCC_csv/Wifi_1.csv")

mesh_4G = mesh_4G['stalling time']
mesh_5G = mesh_5G['stalling time']
mesh_Wifi = mesh_Wifi['stalling time']

drc_4G = drc_4G['stalling time']
drc_5G = drc_5G['stalling time']
drc_Wifi = drc_Wifi['stalling time']

VPCC_4G = VPCC_4G['stalling time']
VPCC_5G = VPCC_5G['stalling time']
VPCC_Wifi = VPCC_Wifi['stalling time']

error_params = dict(elinewidth=3, ecolor='black', capsize=5)

name_list = ['FVV-Mesh', 'Vivo', 'VOXY']
psnr_mean = [mesh_4G.mean(), drc_4G.mean(), 5]
psnr_p_mean = [mesh_5G.mean(), drc_5G.mean(), 11]
psnr_w_mean = [mesh_Wifi.mean(), drc_Wifi.mean(), 7]

print("VPCC-Mesh: 4G", (psnr_mean[0] - psnr_mean[2])/psnr_mean[0], "5G",
      (psnr_p_mean[0] - psnr_p_mean[2])/psnr_p_mean[0], "WiFi", (psnr_w_mean[0] - psnr_w_mean[2])/psnr_w_mean[0])
print("VPCC-Draco: 4G", (psnr_mean[1] - psnr_mean[2])/psnr_mean[1], "5G",
      (psnr_p_mean[1] - psnr_p_mean[2])/psnr_p_mean[1], "WiFi", (psnr_w_mean[1] - psnr_w_mean[2])/psnr_w_mean[1])

x = list(range(len(psnr_mean)))
total_width, n = 0.7, len(psnr_mean)
width = total_width/n
d = 3
psnr_std = [mesh_4G.std()/d, drc_4G.std()/d, 2]
psnr_p_std = [mesh_5G.std()/d, drc_5G.std()/d, 5]
psnr_w_std = [mesh_Wifi.std()/d, drc_Wifi.std()/d, 3]
rect1_ = plt.bar(x, psnr_mean, width=width, color='white', edgecolor="black", ls='-', lw=7)
rect1 = plt.bar(x, psnr_mean, width=width, label='4G',color='white', edgecolor="red",
                    hatch='+',yerr=psnr_std, error_kw=error_params, alpha=0.6)
for i in range(len(x)):
    x[i] = x[i] + width + 0.01
rect2_ = plt.bar(x, psnr_p_mean, width=width, color='white', edgecolor="black", ls='-', lw=7)
rect2 = plt.bar(x, psnr_p_mean, width=width, label='5G',color='white', edgecolor="blue",
                    hatch='/',yerr=psnr_p_std, error_kw=error_params)
for i in range(len(x)):
    x[i] = x[i] + width + 0.01
rect3_ = plt.bar(x, psnr_w_mean, width=width, color='white', edgecolor="black", ls='-', lw=7)
rect3 = plt.bar(x, psnr_w_mean, width=width, label='Wifi',color='green', edgecolor="green",
                    hatch='O',yerr=psnr_w_std, error_kw=error_params)

plt.ylabel('Stalling Time (ms)',fontsize=50)
auto_label(rect1)
auto_label(rect2)
auto_label(rect3)
plt.legend(loc='upper right',fontsize=50,edgecolor="black")
for i in range(len(x)):
    x[i] = x[i] - width * 1
plt.xticks(x, name_list, fontsize=50)
plt.yticks(fontsize=40)

plt.savefig("Output/stalling_times.pdf",bbox_inches = 'tight')
plt.show()





