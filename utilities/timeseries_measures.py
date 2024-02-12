
import numpy as np
import matplotlib.pyplot as plt


def get_centered_moving_average(data_years, data_values, plus_minus_years, min_observations=5):
	"""
	
	"""

	data_years = np.array(data_years)
	data_values = np.array(data_values)

	all_years = range(int(min(data_years)), int(max(data_years)+1))
	smoothed_years = []
	smoothed_results = []
	standard_errors = []

	for year in all_years:
		window_positions = np.where(abs(data_years - year) <= plus_minus_years) 
		window_values = data_values[window_positions]
		mean = np.mean(window_values)

		n = len(window_values)

		if n >= min_observations:
			smoothed_years.append(year)
			smoothed_results.append(mean)
			standard_error = np.std(window_values) / np.sqrt(len(window_values))
			standard_errors.append(standard_error)

	return smoothed_years, smoothed_results, standard_errors


def test_moving_centered_average():

	years = [1920, 1920, 1911, 1918, 1919, 1923, 1925]
	values = [1,3,5,2,6,8,10]
	
	plt.scatter(years, values)

	smoothed_years, smoothed_results, sderrs = get_centered_moving_average(years, values, 3)

	plt.plot(smoothed_years, smoothed_results)

	fill_low = np.array(smoothed_results) - np.array(sderrs)
	fill_high = np.array(smoothed_results) + np.array(sderrs)

	ax=plt.gca()
	ax.fill_between(smoothed_years, fill_low, fill_high)

	plt.show()



if __name__=="__main__":

	test_moving_centered_average()