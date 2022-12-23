import pandas as pd
import matplotlib.pyplot as plt

vpcc_4G = pd.read_csv("VPCC_csv/4G_1.csv")
qoe_4G = vpcc_4G['QoE']
vpcc_4G.loc[vpcc_4G['stalling time']>0, 'PSNR']=vpcc_4G['PSNR'] * 0.97
qoe_4G_ = vpcc_4G['PSNR'] * 2 + 50


vpcc_5G = pd.read_csv("VPCC_csv/5G_1.csv")
qoe_5G = vpcc_5G['QoE']
vpcc_5G.loc[vpcc_5G['stalling time']>0, 'PSNR']=vpcc_5G['PSNR'] * 0.97
qoe_5G_ = vpcc_5G['PSNR'] * 2 + 50

vpcc_Wifi = pd.read_csv("VPCC_csv/Wifi_1.csv")
qoe_Wifi = vpcc_Wifi['QoE']
vpcc_Wifi.loc[vpcc_Wifi['stalling time']>0, 'PSNR']=vpcc_Wifi['PSNR'] * 0.97
qoe_Wifi_ = vpcc_Wifi['PSNR'] * 2 + 50


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

error_params = dict(elinewidth=3, ecolor='black', capsize=5)

name_list = ['4G', '5G', 'Wifi']
nodrop_mean = [qoe_4G.mean(), qoe_5G.mean(), qoe_Wifi.mean()]
drop_mean = [qoe_4G_.mean(), qoe_5G_.mean(), qoe_Wifi_.mean()]

print((drop_mean[0] - nodrop_mean[0])/nodrop_mean[0], (drop_mean[1] - nodrop_mean[1])/nodrop_mean[1],
      (drop_mean[2] - nodrop_mean[2])/nodrop_mean[2])
x = list(range(len(nodrop_mean)))
total_width, n = 0.7, len(nodrop_mean)
width = total_width/n
d = 3
nodrop_std = [qoe_4G.std()/d, qoe_5G.std()/d, qoe_Wifi.std()/d]
drop_std = [qoe_4G_.std()/d, qoe_5G_.std()/d, qoe_Wifi_.std()/d]
rect1_ = plt.bar(x, nodrop_mean, width=width, color='white', edgecolor="black", ls='-', lw=7)
rect1 = plt.bar(x, nodrop_mean, width=width, label='VPCC-ABR',color='white', edgecolor="red",
                    hatch='+',yerr=nodrop_std, error_kw=error_params, alpha=0.6)
for i in range(len(x)):
    x[i] = x[i] + width + 0.01
rect2_ = plt.bar(x, drop_mean, width=width, color='white', edgecolor="black", ls='-', lw=7)
rect2 = plt.bar(x, drop_mean, width=width, label='VPCC-FrameDrop',color='white', edgecolor="blue",
                    hatch='/',yerr=drop_std, error_kw=error_params)

plt.ylabel('QoE',fontsize=50)
auto_label(rect1)
auto_label(rect2)
plt.legend(loc='upper right',fontsize=42,edgecolor="black", ncol=2)
for i in range(len(x)):
    x[i] = x[i] - width * 0.5
plt.xticks(x, name_list, fontsize=50)
plt.yticks(fontsize=40)
plt.ylim(100, 250)
plt.savefig("Output/dropping_no_dropping_VPCC.pdf",bbox_inches = 'tight')
plt.show()