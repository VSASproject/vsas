#This code is used to fit the R-D model
#On the Loot dataset
#This script train and save the up-to-date parameters
#When called from the rd_optim, it read the paraemter from cache.csv cache file
#While when running independantly, it trains on the given dataset, updating
#The model

from numpy import exp
from numpy import abs
from numpy import arange
from pandas import read_csv
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
fsize = 30


def setup_plt():
    plt.rcParams['pdf.fonttype'] = 42


def objective(x, a, b, c, d, a1, b1, c1):
	kappa = 1000
	return a * x + b * x + c * x ** 2 + d + a1 * exp(-((kappa * x - b1 / c1)) ** 2)

def draw_line(ax,log_path,line_label, s_color, line_color):
	dataframe = read_csv(log_path)
	data = dataframe.values
	#print(data)

	br = data[:, -1] * 30 / 1000
	print(br)
	x, y = data[:, 2], data[:, -2]

	popt, _ = curve_fit(objective, x, y)

	a, b, c, d, a1, b1, c1 = popt
	print(popt)

	ax.scatter(x, y, color=s_color, linewidths=10)
	x_line = arange(min(x), max(x)+1, 1)
	y_line = objective(x_line, a, b, c, d, a1, b1, c1)
	ax.plot(x_line, y_line, 'x-', label=line_label,
			markersize=12,markeredgewidth=4,
			color=line_color,linewidth=2)

def aqp_psnr_model():
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	# def objective(x, a, b, c, d):
	# 	kappa=1000
	# 	ans = a*x+ c * x ** 2 + d*exp(-(x-b)**2)
	# 	return ans


	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "aqp"+"100"+".csv"
	log_path = os.path.join(data_root,log_name)

	dataframe = read_csv(log_path)
	data = dataframe.values
	#print(data)

	br = data[:, -1] * 30 / 1000
	print(br)
	x, y = data[:, 2], data[:, -2]

	popt, _ = curve_fit(objective, x, y)

	a, b, c, d, a1, b1, c1 = popt
	print(popt)

	setup_plt()

	# set up the figure canvas
	figure = plt.figure(figsize=(16, 9), dpi=80)
	# set up the margin
	ax = figure.add_axes([0.115, 0.15, 0.8, 0.8])
	# set up the tick size
	ax.tick_params(pad=18, labelsize=fsize - 2)

	ax.scatter(x, y,  label="psnr(qp)",linewidths=10)
	x_line = arange(min(x), max(x)+1, 1)
	y_line = objective(x_line, a, b, c, d, a1, b1, c1)
	ax.plot(x_line, y_line, 'x-', label="f_psnr(qp)",
			markersize=12,markeredgewidth=4,
			color='red',linewidth=2)
	draw_line(ax,'data/aqp33.csv','Dr=0.33','blue','blue')
	draw_line(ax, 'data/aqp10.csv', 'Dr=0.1', 'yellow', 'yellow')

	#annotation
	xi = 5

	err=round(abs(y[xi] - y_line[xi]),2)
	ax.annotate('BR='+str(int(br[xi]))+'Kbps, E='+str(err), xy=(x_line[xi], y[xi]), xytext=(x_line[xi] + 1, y_line[xi] + 1),
				 xycoords='data',fontsize=fsize,
				 arrowprops=dict(facecolor='red', shrink=0.05)
				 )
	ax.plot([15, x_line[xi]], [y[xi], y[xi]], color='red', linestyle='--', linewidth=2)

	xi = 9
	err = round(abs(y[xi] - y_line[xi]), 2)
	ax.annotate('BR='+str(int(br[xi]))+'Kbps, \nE='+str(err), xy=(x_line[xi], y[xi]), xytext=(x_line[xi] + 1, y_line[xi] ),
				 xycoords='data', fontsize=fsize,
				 arrowprops=dict(facecolor='red', shrink=0.05)
				 )
	ax.plot([15, x_line[xi]], [y[xi], y[xi]], color='red', linestyle='--', linewidth=2)

	xi = 15
	err = round(abs(y[xi] - y_line[xi]), 2)
	ax.annotate('BR='+str(int(br[xi]))+'Kbps, \nE='+str(err), xy=(x_line[xi], y[xi]), xytext=(x_line[xi] + 1, y_line[xi] - 1),
				 xycoords='data', fontsize=fsize,
				 arrowprops=dict(facecolor='red', shrink=0.05)
				 )
	ax.plot([15, x_line[xi]], [y[xi], y[xi]], color='red', linestyle='--', linewidth=2)
	#plt.plot((15,y_line[xi]),(x_line[xi], y[xi]))
	#plt.axhline(y[xi],15,30)
	#

	ax.set_xlim(15,35)
	ax.set_xlabel("Attribute QP", fontsize=fsize)
	ax.set_ylabel("Attribute PSNR", fontsize=fsize)
	plt.legend(fontsize=fsize)
	plt.savefig("figures/fig_1.eps")
	plt.show()


if __name__=="__main__":
	aqp_psnr_model()