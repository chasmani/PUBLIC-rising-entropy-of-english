

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.stattools import acf
from statsmodels.distributions.empirical_distribution import ECDF


from scipy.stats import norm


import pymannkendall as mk
import piecewise_regression as pw

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utilities.general_utilities import append_to_csv


metadata_headers = [
		"source",
		"sample_id", 
		"category", 
		"year", 
		"author", 
		"title", 
		"measure_type",
		"length"]

word_measures_headers = [
	"word_count", 
	"avg_word_length", 
	"ttr",
	"zipf_cdf",
	"zipf_clauset", 
	"H_0",
	"H_1",
	"H_2"]



def kpss_coha(category="news", N=2000, min_year=1900, max_year=2010, measure="H_1"):

	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)
		
	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > min_year) & (df['year'] < max_year))]

	source = "COHA"

	df = df[(df['length'] == float(N)) & (df['source'] == source)]


	df = df[(df['category'] == category)]
	df = df[(~df[measure].isna())]

	df = df.groupby('year').median().reset_index()

	df = df.drop_duplicates()

	X = df[measure].values

	if len(X) > 14:

		result = kpss(X)
		kpss_stat = result[0]
		p_value = convert_kpss_to_p_value(kpss_stat)

		n = len(X)


		# Create a dictionary to store the results
		result_dict = {
			'kpss_stat': kpss_stat,
			'p_value': p_value,
			'sample_size': n
		}

		return result_dict
	


def convert_kpss_to_p_value(kpss_stat=0.7512, distribution_filename="../data/kpss_dist.npy"):

	squared_BB_dist = np.load(distribution_filename)

	quantiles = np.percentile(squared_BB_dist, [90, 95, 97.5, 99, 99.9])
	print(quantiles)

	# Assuming squared_BB_dist is already computed from the earlier code
	squared_BB_dist_ecdf = ECDF(squared_BB_dist)	
	p_value = 1 - squared_BB_dist_ecdf(kpss_stat)
	return p_value

def squared_BrownianBridge(n):
	W = np.cumsum(np.random.randn(n)) * n**(-0.5)
	r = np.linspace(0, 1, n)
	V = W - r * W[-1]
	return np.mean(V**2)

def generate_and_save_kpss_distribution(filename="../data/kpss_dist.npy"):
	n = 40000
	squared_BB_dist = []
	for _ in range(200000):
		if _ % 1000 == 0:
			print("Working on {}".format(_))
		squared_BB_dist.append(squared_BrownianBridge(n))
	np.save(filename, squared_BB_dist)
	return squared_BB_dist




def mann_kendall_coha(category="news", N=2000, min_year=1900, max_year=2000, measure="H_1"):

	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)
		
	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > min_year) & (df['year'] < max_year))]

	source = "COHA"

	df = df[(df['length'] == float(N)) & (df['source'] == source)]


	df = df[(df['category'] == category)]
	df = df[(~df[measure].isna())]

	df = df.drop_duplicates()

	df = df.groupby('year').median().reset_index()

	X = df[measure].values

	result = mk.original_test(X, alpha=0.01)

	
	# Extract the test statistic (S), Kendall's tau, and p-value from the test result
	S = result.s
	tau = result.Tau
	p_value = result.p

	# Calculate the confidence interval for Kendall's tau
	tau = result.Tau
	n = len(X)
	se = np.sqrt((2 * (2 * n + 5)) / (9 * n * (n - 1)))
	z = norm.ppf(0.975)  # 0.975 corresponds to 95% confidence level for a two-tailed test
	lower_bound = tau - z * se
	upper_bound = tau + z * se

	# Calculate the effective sample size (ESS)
	n = len(X)
	

	# Create a dictionary to store the results
	result_dict = {
		'S': S,
		'Tau': tau,
		'p': p_value,
		'CI_lower': lower_bound,
		'CI_upper': upper_bound,
		'sample_size': n
	}

	return result_dict

def analyse_coha_table():

	min_year = 1900
	max_year = 2010

	results_csv = "../data/results/timeseries_analysis_trends_{}_{}.csv".format(min_year, max_year)

	measures = {
		"H_1": "Word Entropy",
		"ttr": "Type Token Ratio",
		"zipf_clauset": "Zipf Exponent"
	}
	categories = {
		"news": "News",
		"mag": "Magazine",
		"fic": "Fiction",
		"nf": "Non-Fiction"
	}

	# Write the CSV header
	csv_header = ["Measure", "Category", "KPSS", "MK"]
	append_to_csv(csv_header, results_csv)

	p_values = []

	for category, category_name in categories.items():
		for measure, measure_name in measures.items():
			N = 2000
			kpss_result = kpss_coha(category=category, N=N, min_year=min_year, max_year=max_year, measure=measure)
			mk_result = mann_kendall_coha(category=category, N=N, min_year=min_year, max_year=max_year, measure=measure)

			if kpss_result is not None and mk_result is not None:

				p_values.append(kpss_result['p_value'])
				p_values.append(mk_result['p'])

	p_values_sorted = sorted(p_values)
	num_tests = len(p_values)
	adjusted_p_values = [p * (num_tests - i) for i, p in enumerate(p_values_sorted)]

	# Create a dictionary to map original p-values to adjusted p-values
	p_value_map = dict(zip(p_values, adjusted_p_values))

	for measure, measure_name in measures.items():
		for category, category_name in categories.items():
			N = 2000
			kpss_result = kpss_coha(category=category, N=N, min_year=min_year, max_year=max_year, measure=measure)
			mk_result = mann_kendall_coha(category=category, N=N, min_year=min_year, max_year=max_year, measure=measure)

			if kpss_result is not None and mk_result is not None:
				# Format the KPSS result string with adjusted p-value
				kpss_p_adjusted = p_value_map[kpss_result['p_value']]
				kpss_p_str = format_p_value(kpss_p_adjusted)
				kpss_str = "Statistic={:.3f}, {}".format(kpss_result['kpss_stat'], kpss_p_str)

				# Format the MK result string with adjusted p-value
				mk_p_adjusted = p_value_map[mk_result['p']]
				mk_p_str = format_p_value(mk_p_adjusted)
				mk_str = "Tau={:.3f}, {}, 95% CI [{:.3f}, {:.3f}], N={}".format(
					mk_result['Tau'],
					mk_p_str,
					mk_result['CI_lower'],
					mk_result['CI_upper'],
					mk_result['sample_size']
				)

				csv_row = [measure_name, category_name, kpss_str, mk_str]
				append_to_csv(csv_row, results_csv)
				print(csv_row)

def format_p_value(p_value):
	if p_value < 0.001:
		return "p < 0.001"
	else:
		return "p = {:.3f}".format(p_value)



if __name__=="__main__":
	analyse_coha_table()