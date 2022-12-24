#This code is used to fit the R-D model
#On the Loot dataset
#This script train and save the up-to-date parameters
#When called from the rd_optim, it read the paraemter from cache.csv cache file
#While when running independantly, it trains on the given dataset, updating
#The model
from numpy import exp
from numpy import sin
from numpy import arange
from pandas import read_csv
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
fsize = 30

def setup_plt():
    fs = (16, 9,)
    #dpi = 300
    plt.rcParams['figure.figsize'] = [16, 9]
    #plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['pdf.fonttype'] = 42


def aqp_psnr_model():
	def objective(x, a, b, c, d, a1, b1, c1):
		kappa = 1
		return a * exp(-((kappa * x - b) / c) ** 2) + d * exp(-((kappa * x - a1) / b1) ** 2) + c1
	x_line = []
	y_line = []
	setup_plt()
	file_name_list = ["longdress_1.csv", "loot.csv", "redandblack.csv", "soldier.csv"]
	colors = ["red", "green", "blue", "black"]
	ticks = ['o', 'x', '+', '.']
	counter = 0

	for log_name in file_name_list:
		data_root = "data"
		log_path = os.path.join(data_root,log_name)
		dataframe = read_csv(log_path)
		data = dataframe.values
		x, y = data[:, 0], data[:, -1]
		p0 = (30, -5.699, 14.54, 41.71, 3.612, 80.83, 0)
		popt, _ = curve_fit(objective, x, y, p0, maxfev=500000)
		a, b, c, d, a1, b1, c1 = popt
		plt.scatter(x, y, linewidths=10, color=colors[counter],
					#marker=ticks[counter]
					)
		x_line.append(arange(min(x), max(x), 1))
		y_line.append(objective(x_line[-1], a, b, c, d, a1, b1, c1))
		counter += 1

	plt.tick_params(pad=18,labelsize=fsize-2)
	plt.xlabel("Attribute QP", fontsize=fsize)
	plt.ylabel("Attribute PSNR", fontsize=fsize)
	plt.plot(x_line[0], y_line[0], '--', label="Longdress sequence", color='blue',linewidth=5, alpha=0.6)
	plt.plot(x_line[1], y_line[1], '-', label="Loot sequence", color='green', linewidth=5, alpha=0.6)
	plt.plot(x_line[2], y_line[2], '.-', label="Red and Black sequence", color='red', linewidth=5, alpha=0.6)
	plt.plot(x_line[3], y_line[3], '-', label="Soldier sequence", color='black', linewidth=5, alpha=0.6)
	plt.legend(fontsize=fsize)
	plt.savefig("figures/QPA_PSNR.png")
	plt.show()

def gqp_psnr_model():
	def objective(x, a, b, c, d, a1, b1, c1):
		kappa = 1
		return a * exp(-((kappa * x - b) / c) ** 2) + d * exp(-((kappa * x - a1) / b1) ** 2) + c1
	x_line = []
	y_line = []
	setup_plt()
	file_name_list = ["GP_longdress_1.csv", "GP_loot.csv", "GP_redandblack.csv", "GP_soldier.csv"]
	colors = ["red", "green", "blue", "black"]
	ticks = ['o', 'x', '+', '-']
	counter = 0

	for log_name in file_name_list:
		data_root = "data"
		log_path = os.path.join(data_root,log_name)
		dataframe = read_csv(log_path)
		data = dataframe.values
		x, y = data[:, 0], data[:, -1]
		p0 = (30, -5.699, 14.54, 41.71, 3.612, 80.83, 0)
		popt, _ = curve_fit(objective, x, y, p0, maxfev=500000)
		a, b, c, d, a1, b1, c1 = popt
		plt.scatter(x, y, linewidths=10, color=colors[counter])
		x_line.append(arange(min(x), max(x), 1))
		y_line.append(objective(x_line[-1], a, b, c, d, a1, b1, c1))
		counter += 1

	plt.tick_params(pad=18,labelsize=fsize-2)
	plt.xlabel("Geometry QP", fontsize=fsize)
	plt.ylabel("Geometry PSNR", fontsize=fsize)
	plt.plot(x_line[0], y_line[0], '--', label="Longdress sequence", color='blue',linewidth=5, alpha=0.6)
	plt.plot(x_line[1], y_line[1], '-', label="Loot sequence", color='green', linewidth=5, alpha=0.6)
	plt.plot(x_line[2], y_line[2], '.-', label="Red and Black sequence", color='red', linewidth=5, alpha=0.6)
	plt.plot(x_line[3], y_line[3], '-', label="Soldier sequence", color='black', linewidth=5, alpha=0.6)
	plt.legend(fontsize=fsize)
	plt.savefig("figures/QPG_PSNR.png")
	plt.show()


def aqp_br_model():
	def objective(x, a, b, c, d, a1, b1, c1):
		kappa = 1
		return a * exp(-((kappa * x - b) / c) ** 2) + d * exp(-((kappa * x - a1) / b1) ** 2) + c1
	x_line = []
	y_line = []
	setup_plt()
	file_name_list = ["longdress_1.csv", "loot.csv", "redandblack.csv", "soldier.csv"]
	colors = ["red", "green", "blue", "black"]
	ticks = ['o', 'x', '+', '.']
	counter = 0

	for log_name in file_name_list:
		data_root = "data"
		log_path = os.path.join(data_root,log_name)
		dataframe = read_csv(log_path)
		data = dataframe.values
		x, y = data[:, 0], data[:, -1]
		p0 = (30, -5.699, 14.54, 41.71, 3.612, 80.83, 0)
		popt, _ = curve_fit(objective, x, y, p0, maxfev=500000)
		a, b, c, d, a1, b1, c1 = popt
		plt.scatter(x, y, linewidths=10, color=colors[counter],
					#marker=ticks[counter]
					)
		x_line.append(arange(min(x), max(x), 1))
		y_line.append(objective(x_line[-1], a, b, c, d, a1, b1, c1))
		counter += 1

	plt.tick_params(pad=18,labelsize=fsize-2)
	plt.xlabel("Attribute QP", fontsize=fsize)
	plt.ylabel("BR", fontsize=fsize)
	plt.plot(x_line[0], y_line[0], '--', label="Longdress sequence", color='blue', linewidth=5, alpha=0.6)
	plt.plot(x_line[1], y_line[1], '-', label="Loot sequence", color='green', linewidth=5, alpha=0.6)
	plt.plot(x_line[2], y_line[2], '.-', label="Red and Black sequence", color='red', linewidth=5, alpha=0.6)
	plt.plot(x_line[3], y_line[3], '-', label="Soldier sequence", color='black', linewidth=5, alpha=0.6)
	plt.legend(fontsize=fsize)
	plt.savefig("figures/QPA_BR.png")
	plt.show()


if __name__=="__main__":
	aqp_psnr_model()
	gqp_psnr_model()
	aqp_br_model()