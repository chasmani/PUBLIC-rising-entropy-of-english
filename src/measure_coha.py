

import os
import csv
from datetime import date


import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


from utilities.text_measures import measure_text_word_measures
from utilities.general_utilities import append_to_csv


def measure_coha_word_measures():

	file_directory = "../data/corpora/coha/clean_text/"
	results_filename = "../data/results/results_word_measures_coha.csv"

	# Get text sample files
	files = os.listdir(file_directory)
	text_sample_files = [f for f in files if ".txt" in f]	
	total_file_count = len(text_sample_files)
	counter = 0

	for text_sample_file in text_sample_files:
		counter += 1
		print("Working COHA word measures file {} of {}".format(counter, total_file_count))
		file_path = file_directory + text_sample_file
		category = text_sample_file.split("_")[0]
		year = text_sample_file.split("_")[1]
		ref_id = text_sample_file.split("_")[2].replace(".txt","")
		
		for N in [2000]: 
			metadata = ["COHA", ref_id, category, year, None, None, "word_measures", N]
			try:
				with open (file_path, 'r', errors="ignore") as f:
					text = f.read()
					word_measures = measure_text_word_measures(text, N+100)
					if word_measures:
						csv_list = metadata + word_measures
						append_to_csv(csv_list, results_filename)
				
			except Exception as e:
				print(e)

if __name__=="__main__":
	measure_coha_word_measures()