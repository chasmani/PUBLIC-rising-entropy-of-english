

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss

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


def adf_coha(category="news", N=2000, min_year=1900, max_year=2010, measure="H_1"):

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

	X = df[measure].values

	if len(X) > 14:

		result = adfuller(X)
		p_value = result[1]
		return p_value


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
		p_value = result[1]
		return (kpss_stat, p_value)



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
	return result

def analyse_coha_timeseries():

	min_year = 1900
	max_year = 2010

	results_csv = "../data/results/timeseries_analysis_trends_{}_{}.csv".format(min_year, max_year)

	measures = ["H_1", "ttr", "zipf_clauset"]

	csv_row = [""] + measures
	append_to_csv(csv_row, results_csv)	

	for min_year, max_year in [(min_year,max_year)]:
		
		for category in ["news", "mag", "fic", "nf"]:
			csv_row = [category]
			for measure in measures:
				N = 2000
				kpss = kpss_coha(category=category, N=N, min_year=min_year, max_year=max_year, measure=measure)	
				#print("{}-{}\t{}\t{}\tADF:{}".format(min_year, max_year, category, measure, adf))
				mk = mann_kendall_coha(category=category, N=N, min_year=min_year, max_year=max_year, measure=measure)
				#print("{}-{}\t{}\t{}\tMK:{}".format(min_year, max_year, category, measure, mk))

				if kpss == None:
					kpss = "-"
					csv_row.append("({}, {:.3f})".format(kpss, mk.p,))
				else:
					csv_row.append("({:.4f}, {:.3f})".format(kpss, mk.p,))
			print(csv_row)
			append_to_csv(csv_row, results_csv)



	

if __name__=="__main__":
	analyse_coha_timeseries()