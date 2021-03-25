import matplotlib.pyplot as plt
from termcolor import colored
import matplotlib.transforms
import numpy as np
import pandas as pd

def plot_graphics(graph, MAX_ITR, name_save=""):

	log_itr = list(map(list, zip(*graph.log_itr)))
	best_ger, avg_ger, median_ger = log_itr[0], log_itr[1], log_itr[2]

	fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
	fig.set_size_inches(30, 9)
	title = fig.suptitle('Fitness - Colonia de Formigas', fontsize=40, x=0.45, y=0.97)

	plt.rcParams.update({'font.size': 20})
	plt.subplots_adjust(left=0.04, right=0.85, top=0.85)
	plt.gcf().text(0.86, 0.25, (graph.get_parameters() + 
					 '\n\n-----------------------------------------\n\n Melhor Fitness: ' + str (graph.best_solution.fitness) +
					 '\n\n Media Fitness: %.2f' % graph.avg_fitness +
					 '\n\n Mediana Fitness: %.2f' % graph.median_fitness), fontsize=16)

	if MAX_ITR >= 100: step = int(MAX_ITR / 100)
	else: step = 1
	avg_ger_step, median_ger_step, best_ger_step = [], [], []
	for i in range(0, MAX_ITR, step):
		avg_ger_step.append(avg_ger[i])
		median_ger_step.append(median_ger[i])
		best_ger_step.append(best_ger[i])

	ax1.set_title("Melhores fitness")
	ax1.set_xlabel("Gerações", fontsize='medium')
	ax1.set_ylabel("Fitness", fontsize='medium')
	ax1.plot(list(range(0, MAX_ITR, step)), best_ger_step, 'g--', label='Melhor Fitness: ' + str (graph.best_solution.fitness))
	ax1.legend(ncol=3)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Media e Mediana da fitness")
	ax2.set_xlabel("Gerações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')
	ax2.plot(list(range(0, MAX_ITR, step)), avg_ger_step, 'r--', label='Media Fitness: %.4f' % graph.avg_fitness)
	ax2.plot(list(range(0, MAX_ITR, step)), median_ger_step, 'b--', label='Mediana Fitness: %.4f' % graph.median_fitness)
	ax2.legend(ncol=1)
	ax2.tick_params(labelsize=18)

	ax3.set_title("Comparação entre as fitness")
	ax3.set_xlabel("Gerações", fontsize='medium')
	ax3.set_ylabel("Fitness", fontsize='medium')
	ax3.plot(list(range(0, MAX_ITR, step)), best_ger_step, 'g--', label='Melhor Fitness: %.4f' % graph.best_solution.fitness)
	ax3.plot(list(range(0, MAX_ITR, step)), avg_ger_step, 'r--', label='Media Fitness: %.4f' % graph.avg_fitness)
	ax3.plot(list(range(0, MAX_ITR, step)), median_ger_step, 'b--', label='Mediana Fitness: %.4f' % graph.median_fitness)
	ax3.legend(ncol=1)
	ax3.tick_params(labelsize=18)

	print(colored("\033[1m"+"\n-> Graphic saved in: " + 'graficos/'+name_save+graph.get_parameters()+
				  '_fitness='+str(graph.best_solution.fitness)+'.png', "green"))
	
	fig.savefig('graficos/'+name_save+graph.get_parameters()+'_fitness='+str(graph.best_solution.fitness)+'.png')

def plot_table(results, results_ord, file):
	table = {"NPOP": [], "NGER": [], "TX_M": [], "TX_C": [], "Elitism": [],
			 "Fitness": [], "Avg Fit": [], "Median Fit": [], "STD": []}
	
	for i in results_ord:
		table["NPOP"].append(results[i[0]].nindiv)
		table["NGER"].append(results[i[0]].nger)
		table["TX_M"].append(results[i[0]].mutation_rate)
		table["TX_C"].append(results[i[0]].crossing_rate)
		table["Elitism"].append(results[i[0]].elitism)
		table["Fitness"].append(results[i[0]].best_solution.fitness)
		table["Avg Fit"].append("%.2f" % results[i[0]].avg_fitness)
		table["Median Fit"].append("%.2f" % results[i[0]].median_fitness)
		table["STD"].append("%.2f" % results[i[0]].std_fitness)

	df = pd.DataFrame(data=table)
	print("\nTable results: \n", df)

	fig, ax = plt.subplots()

	fig.patch.set_visible(False)
	plt.axis('off')
	plt.grid('off')
	fig.set_size_inches(12, 11)

	the_table = ax.table(cellText=df.values,colLabels=df.columns, cellLoc='center', loc='center')
	the_table.auto_set_font_size(False)
	the_table.set_fontsize(12)

	plt.gcf().canvas.draw()
	points = the_table.get_window_extent(plt.gcf()._cachedRenderer).get_points()
	points[0,:] -= 120; points[1,:] += 120
	nbbox = matplotlib.transforms.Bbox.from_extents(points/plt.gcf().dpi)

	fig.tight_layout()
	print(colored("\033[1m"+"\n => Table saved in: " + 'tabelas/'+file[len(file)-1]+'.png', "green"))
	fig.savefig('tabelas/'+file[len(file)-1]+'.png', dpi=500, bbox_inches=nbbox)