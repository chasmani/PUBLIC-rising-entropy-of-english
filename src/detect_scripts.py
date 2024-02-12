

import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utilities.general_utilities import append_to_csv


def detect_plays():

	file_directory = "../data/corpora/coha/raw/"
	results_filename = "../data/results/plays.csv"

	# Get text sample files
	files = os.listdir(file_directory)
	text_sample_files = [f for f in files if ".txt" in f]	
	total_file_count = len(text_sample_files)
	counter = 0

	for text_sample_file in text_sample_files:
		counter += 1
		file_path = file_directory + text_sample_file
		category = text_sample_file.split("_")[0]
		year = text_sample_file.split("_")[1]
		ref_id = text_sample_file.split("_")[2].replace(".txt","")
		
		if category == "fic":
			
			metadata = ["COHA", ref_id, category, year]
			try:
				with open (file_path, 'r', errors="ignore") as f:
					text = f.read()
				
					script = is_text_a_script(text)

											

					csv_list = metadata + [len(text), script]
						
					append_to_csv(csv_list, results_filename)
					
			except Exception as e:
				print(e)


def is_text_a_script(text="This is a text bit of text ACt 1 Scene I"):


	for flag in ["ACT", "SCENE", "BALLAD", "SONNET", "POET", "POEM", "Scene", "Act"]:
		if flag in text:
			return True
	return False


if __name__=="__main__":
	detect_plays()