#This code is used to fit the R-D model
#On the Loot dataset
#This script train and save the up-to-date parameters
#When called from the rd_optim, it read the paraemter from cache.csv cache file
#While when running independantly, it trains on the given dataset, updating
#The model

import numpy as np
from cvxpy import exp
from pandas import read_csv
from scipy.optimize import curve_fit
import os

def aqp_psnr_model(qp):
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	def objective(x, a, b, c, d, a1, b1, c1):
		kappa = 1000
		if -((kappa * x - b1 / c1)) ** 2 <= 0:
			return 0
		else:
			return a * x + b * x + c * x ** 2 + d + a1 * exp(-((kappa * x - b1 / c1)) ** 2)

	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "AQP"+"15-35"+".csv"
	log_path = os.path.join(data_root,log_name)
	param_root = "param_cache"
	cache_path = os.path.join(param_root, "aqp_psnr" + ".txt")

	if os.path.exists(cache_path):
		popt = np.loadtxt(cache_path)
		a, b, c, d, a1, b1, c1 = popt
		y = objective(qp,a,b,c,d,a1,b1,c1)
		return y
	else:
		dataframe = read_csv(log_path)
		data = dataframe.values
		#print(data)

		x, y = data[:, 0], data[:, -1]

		popt, _ = curve_fit(objective, x, y)

		a,b,c,d,a1,b1,c1 = popt
		print(popt)
		popt_cache = np.array(popt)
		np.savetxt(cache_path,popt_cache,delimiter=',')
		y = objective(qp, a, b, c, d, a1, b1, c1)
		return y




def gqp_psnr_model(qp):
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	def objective(x, a, b, c, d, a1, b1, c1):
		kappa = 1000
		return a * x + b * x + c * x ** 2 + d + a1 * exp(-((kappa * x - b1 / c1)) ** 2)

	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "GQP"+"15-35"+".csv"
	log_path = os.path.join(data_root,log_name)

	param_root = "param_cache"
	cache_path = os.path.join(param_root, "gqp_psnr" + ".txt")

	if os.path.exists(cache_path):
		popt = np.loadtxt(cache_path)
		a,b,c,d,a1,b1,c1 = popt
		y = objective(qp, a, b, c, d, a1, b1, c1)
		return y
	else:
		dataframe = read_csv(log_path)
		data = dataframe.values
		#print(data)

		x, y = data[:, 0], data[:, -1]

		popt, _ = curve_fit(objective, x, y)

		a,b,c,d,a1,b1,c1 = popt
		print(popt)
		popt_cache = np.array(popt)
		np.savetxt(cache_path, popt_cache, delimiter=',')
		y = objective(qp, a, b, c, d, a1, b1, c1)
		return y







def aqp_br_model(qp):
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	def objective(x, a, b, c, d, a1, b1, c1):
		kappa = 1000
		return a * x + b * x + c * x ** 2 + d + a1 * exp(-((kappa * x - b1 / c1)) ** 2)

	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "AQP"+"15-35"+".csv"
	log_path = os.path.join(data_root,log_name)

	param_root = "param_cache"
	cache_path = os.path.join(param_root, "aqp_br" + ".txt")

	if os.path.exists(cache_path):
		popt = np.loadtxt(cache_path)
		a,b,c,d,a1,b1,c1 = popt
		y = objective(qp, a, b, c, d, a1, b1, c1)
		return y
	else:
		dataframe = read_csv(log_path)
		data = dataframe.values
		#print(data)

		x, y = data[:, 0], data[:, -2]

		popt, _ = curve_fit(objective, x, y)

		a,b,c,d,a1,b1,c1 = popt
		print(popt)
		popt_cache = np.array(popt)
		np.savetxt(cache_path, popt_cache, delimiter=',')
		y = objective(qp, a, b, c, d, a1, b1, c1)
		return y



def aqp_br_model_old(qp):
    def objective(x, a, b, c, d, a1, b1, c1):
        kappa = 1000
        a1 = 0
        ans = a * x + b * x + c * x ** 2 + d
        return ans
    data_root = "data"
    log_name = "AQP"+"15-35"+".csv"
    log_path = os.path.join(data_root,log_name)

    param_root = "param_cache"
    cache_path = os.path.join(param_root, "aqp_br" + ".txt")

    if os.path.exists(cache_path):
        popt = np.loadtxt(cache_path)
        a,b,c,d,a1,b1,c1 = popt
        y = objective(qp, a, b, c, d, a1, b1, c1)
        return y
    else:
        return -1


def gqp_br_model(qp):
	#def objective(x, a, b, c, d):
	#	return a * sin(b - x) + c * x ** 2 + d
	def objective(x, a, b, c, d, a1, b1, c1):
		kappa = 1000
		return a * x + b * x + c * x ** 2 + d + a1 * exp(-((kappa * x - b1 / c1)) ** 2)

	#url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
	data_root = "data"
	log_name = "GQP"+"15-35"+".csv"
	log_path = os.path.join(data_root,log_name)

	param_root = "param_cache"
	cache_path = os.path.join(param_root, "gqp_br" + ".txt")

	if os.path.exists(cache_path):
		popt = np.loadtxt(cache_path)
		a,b,c,d,a1,b1,c1 = popt
		y = objective(qp, a, b, c, d, a1, b1, c1)
		return y
	else:
		dataframe = read_csv(log_path)
		data = dataframe.values
		#print(data)

		x, y = data[:, 0], data[:, -2]

		popt, _ = curve_fit(objective, x, y)

		a,b,c,d,a1,b1,c1 = popt
		print(popt)
		popt_cache = np.array(popt)
		np.savetxt(cache_path, popt_cache, delimiter=',')
		y = objective(qp, a, b, c, d, a1, b1, c1)
		return y





if __name__=="__main__":
	y = aqp_psnr_model(20)
	print(y)
	y = gqp_psnr_model(20)
	print(y)
	y = aqp_br_model(20)
	print(y)
	y = gqp_br_model(20)
	print(y)