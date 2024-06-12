

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as ss
import numpy as np

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


def snapshot_analysis_bnc(measure="H_1"):

	input_filename = "../data/results/results_word_measures_bnc.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)	
	N = 2000

	source = "BNC"
	df = df[(df['length'] == float(N)) & (df['source'] == source)]
	bnc_categories = ["FICTION", "NEWS", "ACPROSE"]

	samples = []
	for category in bnc_categories:
		this_df = df[(df['category'] == category)]
		this_df = this_df[(~this_df[measure].isna())]

		X = this_df[measure].values
		samples.append(X)

	result = ss.f_oneway(*samples)
	
	dof = get_dof(samples)

	eta_squared_value = eta_squared(samples)

	bootstrapped_ci = bootstrap_ci_eta_squared(result, samples)

	return result, dof, eta_squared_value, bootstrapped_ci


def snapshot_analysis_coca(measure="zipf_clauset"):


	input_filename = "../data/results/results_word_measures_coca.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)	
	N = 2000

	source = "COCA"
	df = df[(df['length'] == float(N)) & (df['source'] == source)]
	coca_categories = ["mag", "news", "acad", "fic"]

	samples = []
	for category in coca_categories:
		this_df = df[(df['category'] == category)]
		this_df = this_df[(~this_df[measure].isna())]

		X = this_df[measure].values
		samples.append(X)

	result = ss.f_oneway(*samples)
	
	dof = get_dof(samples)

	eta_squared_value = eta_squared(samples)

	bootstrapped_ci = bootstrap_ci_eta_squared(result, samples)

	return result, dof, eta_squared_value, bootstrapped_ci




def snapshot_analysis_coha(measure="zipf_clauset"):

	input_filename = "../data/results/results_word_measures_coha.csv"

	headers = metadata_headers + word_measures_headers

	df = pd.read_csv(input_filename, delimiter=";", names=headers)	
	N = 2000

	source = "COHA"
	df = df[(df['length'] == float(N)) & (df['source'] == source)]
	coha_categories = ["mag", "news", "fic", "nf"]

	# For the snapshot, just 2000-2007 (data ends at 2007)
	df = df[(df['year'] > 1999)]

	samples = []
	for category in coha_categories:
		this_df = df[(df['category'] == category)]
		this_df = this_df[(~this_df[measure].isna())]

		X = this_df[measure].values
		samples.append(X)

	result = ss.f_oneway(*samples)

	dof = get_dof(samples)

	eta_squared_value = eta_squared(samples)

	bootstrapped_ci = bootstrap_ci_eta_squared(result, samples)

	return result, dof, eta_squared_value, bootstrapped_ci

def get_dof(samples):
	n_groups = len(samples)
	n_total = sum(len(group) for group in samples)
	dof_between = n_groups - 1
	dof_within = n_total - n_groups
	return dof_between, dof_within


def eta_squared(samples):

	all_values = np.concatenate(samples)
	grand_mean = np.mean(all_values)
	n_total = len(all_values)

	# Between-group sum of squares
	SS_between = sum(len(group) * (np.mean(group) - grand_mean) ** 2 for group in samples)

	# Total sum of squares
	SS_total = sum((value - grand_mean) ** 2 for value in all_values)

	# Calculate eta squared
	eta_squared = SS_between / SS_total

	return eta_squared

def bootstrap_ci_eta_squared(ANOVA_result, samples, n_bootstraps=1000):

	bootstrapped_eta_squared = []

	for i in range(n_bootstraps):
		boot_samples = [np.random.choice(sample, len(sample), replace=True) for sample in samples]
		boot_eta_squared = eta_squared(boot_samples)
		bootstrapped_eta_squared.append(boot_eta_squared)

	bootstrapped_eta_squared = np.array(bootstrapped_eta_squared)
	bootstrapped_eta_squared = np.sort(bootstrapped_eta_squared)

	# Calculate the 95% confidence interval
	lower_bound = bootstrapped_eta_squared[int(n_bootstraps * 0.025)]
	upper_bound = bootstrapped_eta_squared[int(n_bootstraps * 0.975)]

	print(lower_bound, upper_bound)

	return lower_bound, upper_bound



def snapshot_analysis():

	results_csv = "../data/results/snapshot_analysis.csv"

	csv_headers = ["Lexical Measure", "Source", "ANOVA Result"]
	append_to_csv(csv_headers, results_csv)

	for measure in ["H_1", "ttr", "zipf_clauset"]:
		if measure == "H_1":
			measure_name = "Word Entropy"
		elif measure == "ttr":
			measure_name = "Type Token Ratio"
		elif measure == "zipf_clauset":
			measure_name = "Zipf Exponent"

		for corpus in ["COHA", "COCA", "BNC"]:

			csv_row = [measure_name, corpus]

			if corpus == "COHA":
				result, dof, eta_squared_value, bootstrapped_ci = snapshot_analysis_coha(measure)
			elif corpus == "COCA":
				result, dof, eta_squared_value, bootstrapped_ci = snapshot_analysis_coca(measure)
			elif corpus == "BNC":
				result, dof, eta_squared_value, bootstrapped_ci = snapshot_analysis_bnc(measure)

			if result[1] < 0.001:
				p_value = "< 0.001"
			else:
				p_value = "{:.2e}".format(result[1])
			result_string = "F({}, {}) = {}, p = {}, eta^2 = {:.3f}, 95% CI = [{:.3f}, {:.3f}]".format(dof[0], dof[1], int(result[0]), p_value, eta_squared_value, bootstrapped_ci[0], bootstrapped_ci[1])
			print(result_string)
			csv_row.append(result_string)
		
			append_to_csv(csv_row, results_csv)




		

if __name__=="__main__":
	snapshot_analysis()