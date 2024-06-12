
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from design_scheme import COLOR_NF, COLOR_FIC, COLOR_NEWS, COLOR_MAG, LINEWIDTH, COLOR_3

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





def get_timeseries_with_window_and_ci(measure="H_1", annotate=True, categories = ["nf", "fic", "news", "mag"]):


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

	COHA_CATEGORY_LABELS = {
		"nf":"Non-Fiction",
		"fic":"Fiction",
		"news":"News",
		"mag":"Magazines"
	}

	COHA_CATEGORY_STYLES = {
		"nf":{"color":COLOR_NF},
		"fic":{"color":COLOR_FIC, "linestyle":":"},
		"news":{"color":COLOR_NEWS},
		"mag":{"color":COLOR_MAG, "linestyle":"-."}
	}

	all_years = pd.Series(np.arange(1800,2010))

	df["date"] = pd.to_datetime(df["year"], format='%Y')

	df = df.sort_values("year")

	for category in categories:

		this_style = COHA_CATEGORY_STYLES[category]

		this_df = df[(df['category'] == category)]
			

		data_years = this_df["year"]
		data_values = this_df[measure]

		smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)

		plt.plot(smoothed_years, smoothed_results, label=category, linewidth=LINEWIDTH, **this_style)

		fill_low = np.array(smoothed_results) - 1.96*np.array(sderrs)
		fill_high = np.array(smoothed_results) + 1.96*np.array(sderrs)

		ax=plt.gca()
		ax.fill_between(smoothed_years, fill_low, fill_high, **this_style, alpha=0.1)


	for j in range(len(ax.lines)):
		l = ax.lines[j]
		y = l.get_data()	
		if annotate:
			annotation = COHA_CATEGORY_LABELS[categories[j]]
			ax.annotate(annotation, xy=(1, y[-1][-1]), xycoords=('axes fraction', 'data'), 
			ha='left', va='center', color=l.get_color())

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)



def plot_timeseries_with_magazine_circulation():


	default_x_size = plt.rcParamsDefault["figure.figsize"][0]
	default_y_size = plt.rcParamsDefault["figure.figsize"][1]

	size_ratio = 1.5

	plt.rcParams["figure.figsize"] = default_x_size, default_y_size

	measure = "H_1"

	get_timeseries_with_window_and_ci(measure, annotate=False, categories=["mag"])	

	plt.ylabel("Word Entropy")
	plt.xlabel("Year")


	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

	# Depression
	neg_growth_years = [
		1929, 1930, 1931, 1932, 1933]

	for year in neg_growth_years:
		plt.axvspan(year, year+1, ymin=0, ymax=0.9, color=COLOR_NEWS, alpha=0.3, lw=0)



	ax.annotate("The Great Depression", xy=(1933, 0.92), xycoords=('data', 'axes fraction'), 
		ha='right', va='center', color=COLOR_NEWS)

	
	# Ten cent magazine
	plt.axvspan(1893, 1894, ymin=0, ymax=0.7, color=COLOR_NEWS, alpha=0.3, lw=0)
	ax.annotate("10 cent magazines", xy=(1894, 0.72), xycoords=('data', 'axes fraction'), 
		ha='right', va='center', color=COLOR_NEWS)


	# Audit Bureau of Circulations
	plt.axvspan(1914, 1915, ymin=0, ymax=0.8, color=COLOR_NEWS, alpha=0.3, lw=0)
	ax.annotate("Audit Bureau of Circulations", xy=(1915, 0.82), xycoords=('data', 'axes fraction'), 
		ha='right', va='center', color=COLOR_NEWS)


	df = pd.read_csv("../data/markets/magazine_readership.csv", delimiter=";", header=0)
	
	ax1 = plt.gca()
	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


	monthly_circ_2005_index = 362
	df["Monthly Circulation Index"] = df["Monthly Circulation"]/monthly_circ_2005_index*100
	ax2.plot(df["Year"], df["Monthly Circulation Index"], label="US Magazine Circulation")

	ax2.set_ylim([9, 400])
	ax2.set_yscale('log')

	ax2.set_ylabel('US Monthly Circulation (Millions)')

	ax1.set_ylim([7.94, 8.41])


	ax1.spines['top'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	ax1.spines['bottom'].set_visible(False)
	ax2.spines['bottom'].set_visible(False)
	


	plt.tight_layout()

	plt.savefig("images/magazine_history.tiff", dpi=300)
	plt.savefig("images/magazine_history.png", dpi=300)


	plt.show()

if __name__=="__main__":
	plot_timeseries_with_magazine_circulation()