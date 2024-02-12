

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as ss

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
	
	return result[1]

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
	print(result)
	return result[1]


def snapshot_analysis():

	results_csv = "../data/results/snapshot_analysis.csv"

	csv_headers = ["measure", "BNC ANOVA p-value", "COCA ANOVA p-value"]

	append_to_csv(csv_headers, results_csv)

	for measure in ["H_1", "ttr", "zipf_clauset"]:
		bnc_result = snapshot_analysis_bnc(measure)
		coca_result = snapshot_analysis_coca(measure)

		csv_row = [measure, bnc_result, coca_result]
		print(csv_row)
		append_to_csv(csv_row, results_csv)

if __name__=="__main__":
	snapshot_analysis()