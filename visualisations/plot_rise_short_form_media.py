
import math


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

from design_scheme import COLOR_NF, COLOR_FIC, COLOR_NEWS, COLOR_MAG, COLOR_SOCIAL, LINEWIDTH, FONT_PROP, BOLD_FONT_PROP, COLOR_3


def get_min_u(lamb, r, R):

	return 1 / (lamb*(1/R - 1/r))



def plot_min_u_as_lambda(r, linestyle="solid", color="black", label=None):
	
	R = 1


	lambs = np.linspace(0.5,1, 100)
	min_us = [get_min_u(lamb, r, R) for lamb in lambs]

	if r == float("inf"):
		r = "Infinite"


	if label:
		plt.plot(lambs, min_us, linewidth=LINEWIDTH*2, color=color, linestyle=linestyle, label=label)
	else:
		plt.plot(lambs, min_us, linewidth=LINEWIDTH*2, color=color, linestyle=linestyle, label=r"$\bar{r}_m=$" + str(r))
	

	
def plot_min_u_as_lambda_rs():

	plot_min_u_as_lambda(r=float("inf"), linestyle="solid", color="#404040")
	plot_min_u_as_lambda(r=10, linestyle=(0, (5, 1)), color=COLOR_MAG)
	plot_min_u_as_lambda(r=5, linestyle=(0, (5, 3)), color=COLOR_NEWS)
	plot_min_u_as_lambda(r=3, linestyle=(0, (5, 5)), color=COLOR_FIC)

	plt.xlabel(r"Information Prevalence, $\lambda_m$")
	plt.ylabel(r"Minimum Size of Information per Media Item, $u_{min}$")

	plt.xlim(0.4,1.1)

	plt.axhline(1.3, label="E.g. Social Media", linestyle="dotted", linewidth=LINEWIDTH*2, color=COLOR_SOCIAL)

	#plt.arrow(1, 1, 0.01, 0.02, head_width=0.05, head_length=0.03, linewidth=4, color='r', length_includes_head=True)

	plt.xticks([])
	plt.yticks([])

	ax=plt.gca()
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	plt.legend()

	plt.savefig("images/min_u_with_increasing_prevalence_one_r.tiff", dpi=300)
	plt.show()

def plot_one_line():

	plot_min_u_as_lambda(r=float("inf"), linestyle="solid", color="#404040", label="Minimum Viable Size")
	
	plt.xlabel(r"Information Prevalence")
	plt.ylabel(r"Information Item Size")

	plt.xlim(0.4,1.1)

	plt.axhline(1.3, label="E.g. Social Media", linestyle="dotted", linewidth=LINEWIDTH*2, color=COLOR_SOCIAL)

	#plt.arrow(1, 1, 0.01, 0.02, head_width=0.05, head_length=0.03, linewidth=4, color='r', length_includes_head=True)

	plt.xticks([])
	plt.yticks([])

	ax=plt.gca()
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	plt.legend()

	plt.savefig("images/min_u_with_increasing_prevalence_inf_r.png", dpi=300)
	plt.show()



if __name__=="__main__":
	plot_min_u_as_lambda_rs()

