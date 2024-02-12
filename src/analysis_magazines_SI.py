
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utilities.timeseries_measures import get_centered_moving_average

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


def analysis_circulation_and_word_entropy():

	plus_minus_years = 5

	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)

	min_year = 1810
	max_year = 2010
	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > min_year) & (df['year'] < max_year))]	

	source = "COHA"
	N = 2000
	df = df[(df['length'] == float(N)) & (df['source'] == source)]

	smoothing_factor = 0.5

	j = 0


	df["date"] = pd.to_datetime(df["year"], format='%Y')

	df = df.sort_values("year")

	df = df[(df['category'] == "mag")]

	data_years = df["year"]
	data_values = df["H_1"]

	smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)
	print(smoothed_years, smoothed_results)

	
	# List of existing years
	# List of smoothed results

	df_circ = pd.read_csv("../data/markets/magazine_readership.csv", delimiter=";", header=0)
	
	# Match smoothed years to circulation years
	print(df_circ)

	df_combined = pd.DataFrame({'Year': smoothed_years, 'H': smoothed_results}).merge(df_circ, on='Year')
	pearson_r = df_combined.corr().loc['H', 'Monthly Circulation']
	print(pearson_r)


	print(df_combined)

	# Run with AR1 model
	import statsmodels.api as sm

	X = sm.add_constant(df_combined["Monthly Circulation"])
	Y = df_combined["H"]

	model = sm.GLSAR(Y, X, rho=1)  # Set rho=1 for AR1 correlation
	result = model.fit()	
	print(result.summary())
	print(model.rho)

	# Detrended data
	X = df_combined["Monthly Circulation"]
	diff_X = X.diff().dropna()
	diff_Y = Y.diff().dropna()

	from scipy.stats import pearsonr
	correlation, p_value = pearsonr(diff_X, diff_Y)
	print("Correlation: ", correlation)
	print("P-value: ", p_value)


if __name__=="__main__":
	analysis_circulation_and_word_entropy()