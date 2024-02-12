

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from design_scheme import COLOR_FIC


def plot_prey_diet_choice_distribution(y=[0,1,1,0,2,1,0,1,0,0,1,2,1,0,0,0,1,1,0,2], diet_condition=5):

	x = list(range(len(y)))

	plt.ylim(0,7)


	plt.xlabel(r"Information Utility Rate, $r_i$")
	plt.ylabel(r"Information Prevalence, $\lambda_i$")

	palette = ["lightgrey", COLOR_FIC]

	hue = ["Ignored Media"]*diet_condition + ["Consumed Media"]*(20-diet_condition)

	plt.axvline(diet_condition, linestyle="dashed", linewidth=3, label="Diet Condition")

	
	colors = ["lightgrey"]*diet_condition + [COLOR_FIC]*(20-diet_condition)

	plt.bar(x=x, height=y, width=0.6, color=colors, label="Ignored Media")
	plt.bar(x=[], height=[], width=0.6, color=COLOR_FIC, label="Consumed Media")


	plt.xticks([])
	plt.yticks([])





if __name__=="__main__":


	y_low = [0,1,1,0,2,1,0,1,0,0,1,2,1,0,0,0,1,1,0,2]
	diet_condition_low = 5

	y_high = [1,1,1,1,2,1,1,1,3,4,1,2,1,2,3,6,2,3,5,4]
	diet_condition_high = 13


	plot_prey_diet_choice_distribution(y_high, diet_condition_high)
	plt.show()