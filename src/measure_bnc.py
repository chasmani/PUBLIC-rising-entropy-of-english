import os
import csv

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


from utilities.text_measures import measure_text_word_measures
from utilities.general_utilities import append_to_csv


def measure_bnc_word_measures():

	metadata_filename = "../data/results/bnc_metadata.csv"
	input_text_folder = "../data/corpora/bnc/clean_text/"
	results_filename = "../data/results/results_word_measures_bnc.csv"
	with open(metadata_filename, 'r', encoding="utf-8") as read_obj:
		csv_reader = csv.reader(read_obj, delimiter=";")
		for row in csv_reader:
			print(row)
			sample_id = row[1]

			file_path = input_text_folder + sample_id + ".txt"

			for N in [2000]: 
				metadata = row + ["word_measures", N]
				try:
					with open (file_path, 'r', errors="ignore") as f:
						text = f.read()
						word_measures = measure_text_word_measures(text, N+100)
						if word_measures:
							csv_list = metadata + word_measures
							append_to_csv(csv_list, results_filename)
					
				except Exception as e:
					print(e)
					raise


if __name__=="__main__":
	measure_bnc_word_measures()
