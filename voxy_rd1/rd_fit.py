#This code is used to fit the R-D model
#On the Loot dataset
#This script train and save the up-to-date parameters
#When called from the rd_optim, it read the paraemter from cache.csv cache file
#While when running independantly, it trains on the given dataset, updating
#The model

from numpy import sin
from numpy import arange
from pandas import read_csv
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
fsize = 30

def setup_plt():
    fs = (16, 9,)
    dpi = 300
    plt.rcParams['figure.figsize'] = [16, 9]
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['pdf.fonttype'] = 42


def aqp_psnr_model():
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	def objective(x, a, b, c, d):
		return a*x + b*x + c * x ** 2 + d

	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "AQP"+"15-35"+".csv"
	log_path = os.path.join(data_root,log_name)

	dataframe = read_csv(log_path)
	data = dataframe.values
	print(data)

	x, y = data[:, 0], data[:, -1]

	popt, _ = curve_fit(objective, x, y)

	a, b, c, d = popt
	print(popt)

	setup_plt()
	plt.scatter(x, y, linewidths=10)

	x_line = arange(min(x), max(x), 1)
	y_line = objective(x_line, a, b, c, d)

	plt.tick_params(pad=18,labelsize=fsize-2)
	plt.xlabel("Attribute QP", fontsize=fsize)
	plt.ylabel("Attribute PSNR", fontsize=fsize)
	plt.plot(x_line, y_line, '--', label="Loot sequence", color='red',linewidth=5)
	plt.legend(fontsize=fsize)
	plt.savefig("figures/QPA_PSNR.png")
	plt.show()

def gqp_psnr_model():
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	def objective(x, a, b, c, d):
		return a*x + b*x + c * x ** 2 + d

	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "GQP"+"15-35"+".csv"
	log_path = os.path.join(data_root,log_name)

	dataframe = read_csv(log_path)
	data = dataframe.values
	print(data)

	x, y = data[:, 0], data[:, -1]

	popt, _ = curve_fit(objective, x, y)

	a, b, c, d = popt
	print(popt)

	setup_plt()
	plt.scatter(x, y, linewidths=10)

	x_line = arange(min(x), max(x), 1)
	y_line = objective(x_line, a, b, c, d)

	plt.tick_params(pad=18,labelsize=fsize-2)
	plt.xlabel("Geometry QP", fontsize=fsize)
	plt.ylabel("Geometry PSNR", fontsize=fsize)
	plt.plot(x_line, y_line, '--', label="Loot sequence", color='red',linewidth=5)
	plt.legend(fontsize=fsize)
	plt.savefig("figures/QPG_PSNR.png")
	plt.show()


def aqp_br_model():
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	def objective(x, a, b, c, d):
		return a*x + b*x + c * x ** 2 + d

	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "AQP"+"15-35"+".csv"
	log_path = os.path.join(data_root,log_name)

	dataframe = read_csv(log_path)
	data = dataframe.values
	print(data)

	x, y = data[:, 0], data[:, -2]

	popt, _ = curve_fit(objective, x, y)

	a, b, c, d = popt
	print(popt)

	setup_plt()
	plt.scatter(x, y, linewidths=10)

	x_line = arange(min(x), max(x), 1)
	y_line = objective(x_line, a, b, c, d)

	plt.tick_params(pad=18,labelsize=fsize-2)
	plt.xlabel("Attribute QP", fontsize=fsize)
	plt.ylabel("BR", fontsize=fsize)
	plt.plot(x_line, y_line, '--', label="Loot sequence", color='red',linewidth=5)
	plt.legend(fontsize=fsize)
	plt.savefig("figures/QPA_BR.png")
	plt.show()

def gqp_br_model():
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	def objective(x, a, b, c, d):
		return a*x + b*x + c * x ** 2 + d

	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "GQP"+"15-35"+".csv"
	log_path = os.path.join(data_root,log_name)

	dataframe = read_csv(log_path)
	data = dataframe.values
	print(data)

	x, y = data[:, 0], data[:, -2]

	popt, _ = curve_fit(objective, x, y)

	a, b, c, d = popt
	print(popt)

	setup_plt()
	plt.scatter(x, y, linewidths=10)

	x_line = arange(min(x), max(x), 1)
	y_line = objective(x_line, a, b, c, d)

	plt.tick_params(pad=18,labelsize=fsize-2)
	plt.xlabel("Geometry QP", fontsize=fsize)
	plt.ylabel("BR", fontsize=fsize)
	plt.plot(x_line, y_line, '--', label="Loot sequence", color='red',linewidth=5)
	plt.legend(fontsize=fsize)
	plt.savefig("figures/QPG_BR.png")
	plt.show()


if __name__=="__main__":
	aqp_psnr_model()
	gqp_psnr_model()
	aqp_br_model()
	gqp_br_model()