
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



def get_timeseries_combined_plot_with_conf_intervals(measure="H_1", N=2000):

	plus_minus_years = 5

	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)

	min_year = 1810
	max_year = 2010
	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > min_year) & (df['year'] < max_year))]	


	source = "COHA"
	df = df[(df['length'] == float(N)) & (df['source'] == source)]

	all_years = pd.Series(np.arange(1825,2010))

	df = df.sort_values("year")


	categories = ["news", "mag", "nf", "fic"]

	all_results = []
	all_sderrs = []

	print(len(df))

	for category in categories:
		this_df = df[(df['category'] == category)]
		print(category, len(this_df))

		this_results = []
		this_sderrs = []

		data_years = this_df["year"]
		data_values = this_df[measure]

		smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)

		for year in all_years:
			if year in smoothed_years:
				year_index = smoothed_years.index(year)
				result = smoothed_results[year_index]
				this_results.append(result)
				sderr = sderrs[year_index]
				this_sderrs.append(sderr)
			else:
				this_results.append(np.nan)
				this_sderrs.append(np.nan)


		all_results.append(this_results)
		all_sderrs.append(this_sderrs)

	means = []
	mean_sderrs = []

	# get means and sderrs
	for year in all_years:
		year_sum = 0
		year_count = 0
		var_sum = 0
		year_index = list(all_years).index(year)
		for cat_index in range(4):
			cat_result = all_results[cat_index][year_index]
			if np.isnan(cat_result):
				pass
			else:
				year_sum += cat_result
				year_count += 1
				var_sum += all_sderrs[cat_index][year_index]**2
		year_mean = year_sum/year_count
		year_sderr = (1/year_count) * np.sqrt(var_sum)
		means.append(year_mean)
		mean_sderrs.append(year_sderr)

	cutoff_index = list(all_years).index(1900)



	plt.plot(all_years[:cutoff_index], means[:cutoff_index], alpha=1, label=category, linewidth=LINEWIDTH, color="#040404")

	plt.plot(all_years[cutoff_index:], means[cutoff_index:], label=category, linewidth=LINEWIDTH, color="#040404")



	fill_low = np.array(means) - 1.96*np.array(mean_sderrs)
	fill_high = np.array(means) + 1.96*np.array(mean_sderrs)

	ax=plt.gca()
	ax.fill_between(all_years, fill_low, fill_high, alpha=0.1)





def plot_timeseries_with_media_categories(measure="H_1", measure_name="Word Entropy", annotate=True, categories = ["nf", "fic", "news", "mag"], N=2000):

	plus_minus_years = 5

	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)

	df['H_1_neg'] = 0 - df['H_1']

	min_year = 1810
	max_year = 2010
	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > min_year) & (df['year'] < max_year))]	


	source = "COHA"
	N = N
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
			if measure == "H_2" and annotation == "Fiction":
				ax.annotate(annotation, xy=(1, y[-1][-1]-0.01), xycoords=('axes fraction', 'data'), 
				ha='left', va='center', color=l.get_color())
			else:
				ax.annotate(annotation, xy=(1, y[-1][-1]), xycoords=('axes fraction', 'data'), 
				ha='left', va='center', color=l.get_color())

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)

	plt.xlabel("Year")
	plt.ylabel(measure_name)

	if measure == "zipf_clauset":
		plt.gca().invert_yaxis()

	#plt.grid(axis="y")


	plt.tight_layout()

	plt.savefig("images/coha_categories_timeseries_{}.tiff".format(measure), dpi=300)
	plt.savefig("images/coha_categories_timeseries_{}.png".format(measure), dpi=300)
	plt.savefig("images/Figure2.png".format(measure), dpi=600)

	print("Done")
	

	plt.show()


if __name__=="__main__":
	#get_timeseries_combined_plot_with_conf_intervals()
	#plt.show()
	plot_timeseries_with_media_categories(measure="H_1", measure_name="Word Entropy")
	