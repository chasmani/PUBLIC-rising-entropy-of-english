
import math

import matplotlib.pyplot as plt
import pandas as pd
import piecewise_regression as pw
import numpy as np

from design_scheme import COLOR_1, COLOR_2

LINEWIDTH = 1

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


def plot_timseries_piecewise_all():


	fig_width, fig_height = plt.gcf().get_size_inches()

	fig = plt.figure()

	N = 2000

	pd.set_option('display.max_columns', None)


	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)

	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > 1800) & (df['year'] < 2010))]
	
	source = "COHA"

	df = df[(df['length'] == float(N)) & (df['source'] == source)]

	measures = ["H_1", "zipf_clauset", "ttr"]
	categories = ["mag", "news", "fic", "nf"]

	plt.subplots(3,4,sharex="all", sharey="row", figsize=(fig_width*2, fig_height*2), constrained_layout=True)


	for category_number in range(4):
		for measure_number in range(3):
			category = categories[category_number]
			measure = measures[measure_number]

			plot_number = category_number + measure_number * 4 + 1
			print(plot_number)

			plt.subplot(3,4,plot_number)


			if plot_number <= 4:
				if category == "news":
					plt.title("News")
				if category == "mag":
					plt.title("Magazines")
				if category == "fic":
					plt.title("Fiction")
				if category == "nf":
					plt.title("Non-Fiction")
			if plot_number == 1:
				if measure == "H_1":
					plt.ylabel("Word Entropy")
			if plot_number == 5:
				if measure == "zipf_clauset":
					plt.ylabel("- Zipf Exponent")
			if plot_number == 9:
				if measure == "ttr":
					plt.ylabel("Type Token Ratio")
			if plot_number > 8:
				plt.xlabel("Year")



			this_df = df[(df['category'] == category)]
			this_df = this_df[(~this_df[measure].isna())]

			this_df = this_df.groupby('year').median().reset_index()

			Y = this_df[measure].values
			X = this_df["year"].values

			if measure == "zipf_clauset":
				Y = -1 * Y

			np.random.seed(1)

			pw_fit = pw.Fit(X,Y, n_breakpoints=1, min_distance_to_edge=0.02)
			
			pw_results = pw_fit.get_results()
			breakpoint_year = pw_results["estimates"]["breakpoint1"]["estimate"]
			breakpoint_interval = breakpoint_year - pw_results["estimates"]["breakpoint1"]["confidence_interval"][0]
			print(breakpoint_year, breakpoint_interval)

			pw_fit.plot_data(alpha=0.5, color=COLOR_1)
			pw_fit.plot_fit(color=COLOR_1)
			pw_fit.plot_breakpoints(color=COLOR_2, label=r"{} $\pm$ {} years".format(round(breakpoint_year), math.ceil(breakpoint_interval)))
			pw_fit.plot_breakpoint_confidence_intervals(color=COLOR_2)
			
			if plot_number in [1,5,9]:
				plt.legend(loc='lower right')
			elif plot_number in [2,3,6,7,11]:
				plt.legend(loc='lower left')
			else:
				plt.legend()

	plt.tight_layout()

	plt.savefig("images/timeseries_piecewise_all.tiff", dpi=300)

	plt.show()


def plot_timseries_piecewise_collated():

	N = 2000
	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)

	min_year = 1810
	max_year = 2010
	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > min_year) & (df['year'] < max_year))]	

	source = "COHA"
	df = df[(df['length'] == float(N)) & (df['source'] == source)]

	measure = "H_1"

	all_years = list(pd.Series(np.arange(1825,2010)))

	df = df.sort_values("year")

	categories = ["news", "mag", "nf", "fic"]

	all_results = []

	for category in categories:
		this_df = df[(df['category'] == category)]

		data_years = list(this_df["year"].values)
		data_values = list(this_df[measure].values)

		this_results = []

		for year in all_years:
			if year in data_years:
				year_index = data_years.index(year)
				result = data_values[year_index]
				this_results.append(result)
			else:
				this_results.append(np.nan)

		all_results.append(this_results)


	means = []

	# get means and sderrs
	for year in all_years:
		year_sum = 0
		year_count = 0
		year_index = list(all_years).index(year)
		for cat_index in range(4):
			cat_result = all_results[cat_index][year_index]
			if np.isnan(cat_result):
				pass
			else:
				year_sum += cat_result
				year_count += 1

		year_mean = year_sum/year_count
		means.append(year_mean)

	
	#cutoff_index = list(all_years).index(1900)
	Y = means
	X = all_years

	print(all_years)
	print(means)

	pw_fit = pw.Fit(X,Y, n_breakpoints=1, min_distance_to_edge=0.02)			

	pw_results = pw_fit.get_results()
	breakpoint_year = pw_results["estimates"]["breakpoint1"]["estimate"]
	breakpoint_interval = breakpoint_year - pw_results["estimates"]["breakpoint1"]["confidence_interval"][0]
	print(breakpoint_year, breakpoint_interval)

	pw_fit.plot_data(alpha=0.5, color=COLOR_1)
	pw_fit.plot_fit(color=COLOR_1)
	pw_fit.plot_breakpoints(color=COLOR_2, label=r"{} $\pm$ {} years".format(round(breakpoint_year), math.ceil(breakpoint_interval)))
	pw_fit.plot_breakpoint_confidence_intervals(color=COLOR_2)
	
	plt.legend()

	plt.xlabel("Year")
	plt.ylabel("Entropy")

	plt.tight_layout()

	plt.savefig("images/timeseries_piecewise_combined.tiff", dpi=300)

	plt.show()



if __name__=="__main__":
	plot_timseries_piecewise_all()