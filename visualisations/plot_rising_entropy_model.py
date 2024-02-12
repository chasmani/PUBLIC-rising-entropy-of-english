

import math


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

from design_scheme import COLOR_NF, COLOR_FIC, COLOR_NEWS, COLOR_MAG, COLOR_SOCIAL, LINEWIDTH, COLOR_3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def entropy_rising_normal_example():

	# Initialize the figure
	f, ax = plt.subplots()
	#sns.despine(bottom=True, left=True)


	prevalences = []

	lambdas = []
	rs = []
	consumeds = []

	np.random.seed(0)

	lamb_count = 0
	for mean, variance, threshold in [(4,2.6,1), (5,2.4,3), (7,2.2,4), (8,2,5), (8.5,2,6), (9,2,7)]:
		prevalence = [r"$\lambda_{}$".format(lamb_count)] * 100
		lamb_count += 1
		prevalences += prevalence

		lamb_rs = list(np.random.normal(loc=mean, scale=variance, size=100))
		consumed = [1 if r>threshold else 0 for r in lamb_rs]
		rs += lamb_rs
		consumeds += consumed

	print(len(prevalences))
	print(len(rs))
	print(len(consumeds))


	df = pd.DataFrame({'Prevalence':prevalences, 'Utility Rate':rs, 'consumed':consumeds})

	palette = ["silver", COLOR_FIC]

	sns.stripplot(y="Utility Rate", x="Prevalence", hue="consumed",
	              data=df, dodge=False, alpha=1, edgecolor="white", linewidth=1, size=6, zorder=1, orient="v", palette=palette)

	plt.xlabel(r"Increasing Prevalence, $\lambda$")
	plt.ylabel(r"Utility rate, $r_p$")


	# Show each observation with a scatterplot


	# Show the conditional means, aligning each pointplot in the
	# center of the strips by adjusting the width allotted to each
	# category (.8 by default) by the number of hue levels
	#sns.pointplot(x="value", y="measurement", hue="species", data=iris, dodge=.8 - .8 / 3,join=False, palette="dark",markers="d", scale=.75, ci=None)

	# Improve the legend
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles[:], ["Ignored", "Consumed"], title="Information", frameon=True)

	plt.savefig("images/entropy_rising_with_prevalence.png", dpi=300)

	plt.show()



def get_optimal_diet(rs, lamb, t):
	"""
	Get the optimal diet for a forager given some prey
	lamb and t are the same for each prey
	"""

	rs.sort(reverse=True)
	rs_diet = []
	rs_ignored = []
	R = 0
	for r in rs:
		if r > R:
			rs_diet.append(r)
			R = lamb*t*np.sum(rs_diet)/(1+lamb*t*len(rs_diet))
			print(R)
		else:
			if np.random.random()<0.2:
				rs_ignored.append(r)

	return rs_diet, rs_ignored


def entropy_rising_simulation():

	np.random.seed(2)

	# Initialize the figure
	#f, ax = plt.subplots()
	#sns.despine(bottom=True, left=True)

	fig_width, fig_height = plt.gcf().get_size_inches()

	fig = plt.figure(figsize=(fig_width*1, fig_height), constrained_layout=True)
	

	prevalences = np.array(range(10,40,3))/100
	print(prevalences)

	prevalences_df = []
	rs_df = []
	diet_df = []
	t = 1

	for prevalence in prevalences:
		n = int(500*prevalence)
		

		n_rs = list(np.random.uniform(low=20, high=30, size=n))

		rs_consumed, rs_ignored = get_optimal_diet(n_rs, prevalence, t)

		prevalences_df += [prevalence]*(len(rs_consumed)+len(rs_ignored))

		rs_df += rs_consumed
		rs_df += rs_ignored

		print(rs_consumed, rs_ignored)



		diet_df += ["Consumed"]*len(rs_consumed) 
		diet_df += ["Ignored"]*len(rs_ignored)

	df = pd.DataFrame({'Prevalence':prevalences_df, 'Utility Rate':rs_df, 'consumed':diet_df})

	palette = [COLOR_FIC, "silver"]

	sns.stripplot(y="Utility Rate", x="Prevalence", hue="consumed",
	              data=df, dodge=False, alpha=1, edgecolor="white", linewidth=0.3, size=6, zorder=1, orient="v", palette=palette)

	plt.xlabel(r"Information Prevalence, $\lambda$")
	plt.ylabel(r"Information Utility Rate, $r_i$")


	ax = plt.gca()
	handles, labels = ax.get_legend_handles_labels()

	#ax.legend(handles[:], ["Consumed", "Ignored"], title="Information", frameon=True, loc='center left', bbox_to_anchor=(1, 0.5))
	ax.legend(handles[:], ["Consumed", "Ignored"], title="Information", frameon=True)

	ax.set_xlim(right=12.5)

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)



	plt.savefig("images/entropy_rising_simulation_with_survival.tiff", dpi=300)

	plt.show()

if __name__=="__main__":
	entropy_rising_simulation()