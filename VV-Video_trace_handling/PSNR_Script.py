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
        height = round(rect.get_height(), 1) + 1
        plt.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    fontsize=45,
                    rotation=90,
                    textcoords="offset points",
                    ha='center', va='bottom')

psnr = pd.read_csv("Output/simulate_4G.csv")
psnr_p = pd.read_csv("Output/simulate_5G.csv")
psnr_w = pd.read_csv("Output/simulate_wifi.csv")

vpcc = psnr['VPCC']
draco = psnr['Draco']
mesh = psnr['Mesh']

vpcc_p = psnr_p['VPCC']
draco_p = psnr_p['Draco']
mesh_p = psnr_p['Mesh']

vpcc_w = psnr_w['VPCC']
draco_w = psnr_w['Draco']
mesh_w = psnr_w['Mesh']

error_params = dict(elinewidth=3, ecolor='black', capsize=5)

name_list = ['FVV-Mesh', 'Vivo', 'VOXY']
psnr_mean = [mesh.mean(), draco.mean(), vpcc.mean()]
psnr_p_mean = [mesh_p.mean(), draco_p.mean(), vpcc_p.mean()]
psnr_w_mean = [mesh_w.mean(), draco_w.mean(), vpcc_w.mean()]

print("VPCC-Mesh: 4G", (psnr_mean[2] - psnr_mean[0])/psnr_mean[0], "5G",
      (psnr_p_mean[2] - psnr_p_mean[0])/psnr_p_mean[0], "WiFi", (psnr_w_mean[2] - psnr_w_mean[0])/psnr_w_mean[0])
print("VPCC-Draco: 4G", (psnr_mean[2] - psnr_mean[1])/psnr_mean[1], "5G",
      (psnr_p_mean[2] - psnr_p_mean[1])/psnr_p_mean[1], "WiFi", (psnr_w_mean[2] - psnr_w_mean[1])/psnr_w_mean[1])
print(((psnr_mean[2] - psnr_mean[0])/psnr_mean[0] + (psnr_p_mean[2] - psnr_p_mean[0])/psnr_p_mean[0] + (psnr_w_mean[2] - psnr_w_mean[0])/psnr_w_mean[0] +
      (psnr_mean[2] - psnr_mean[1])/psnr_mean[1] + (psnr_p_mean[2] - psnr_p_mean[1])/psnr_p_mean[1] + (psnr_w_mean[2] - psnr_w_mean[1])/psnr_w_mean[1])/6)
x = list(range(len(psnr_mean)))
total_width, n = 0.7, len(psnr_mean)
width = total_width/n
psnr_std = [mesh.std(), draco.std(), vpcc.std()]
psnr_p_std = [mesh_p.std(), draco_p.std(), vpcc_p.std()]
psnr_w_std = [mesh_w.std(), draco_w.std(), vpcc_w.std()]
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
                    hatch='x',yerr=psnr_w_std, error_kw=error_params)


