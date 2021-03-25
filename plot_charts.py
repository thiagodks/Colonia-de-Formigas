import matplotlib.pyplot as plt
from termcolor import colored
import matplotlib.transforms
import numpy as np
import pandas as pd
import pickle
import argparse
import sys

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', required=True, help='file input: -f results.pickle')
	args = vars(parser.parse_args())
	print("\033[1m"+"\n-> File: ", args['f'], "\n")
	return args

def plot_results(results, args):
	results.sort(key=lambda x: x[0].best_global.fitness)
	plot_graphics(results[0][0], results[0][1], name_save='best_solution_')
	plot_graphics(results[-1][0], results[-1][1], name_save='worst_solution_')
	file_name = args['f'].split("/")
	file_name = file_name[-1]
	plot_table(results, name_save=file_name)

def plot_graphics(graph, parameters, name_save=""):

	log_itr = list(map(list, zip(*graph.log_itr)))
	best_ger, avg_ger, median_ger = log_itr[0], log_itr[1], log_itr[2]

	fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
	fig.set_size_inches(30, 9)
	title = fig.suptitle('Fitness - Colonia de Formigas', fontsize=40, x=0.45, y=0.97)

	plt.rcParams.update({'font.size': 20})
	plt.subplots_adjust(left=0.04, right=0.85, top=0.85)
	plt.gcf().text(0.86, 0.25, (graph.get_parameters() + 
					 '\n\n-----------------------------------------\n\n Melhor Fitness: ' + str (graph.best_global.fitness) +
					 '\n\n Media Fitness: %.2f' % graph.avg_fitness +
					 '\n\n Mediana Fitness: %.2f' % graph.median_fitness), fontsize=16)

	if parameters['MAX_ITR'] >= 100: step = int(parameters['MAX_ITR'] / 100)
	else: step = 1
	avg_ger_step, median_ger_step, best_ger_step = [], [], []
	for i in range(0, parameters['MAX_ITR'], step):
		avg_ger_step.append(avg_ger[i])
		median_ger_step.append(median_ger[i])
		best_ger_step.append(best_ger[i])

	ax1.set_title("Melhores fitness")
	ax1.set_xlabel("Iterações", fontsize='medium')
	ax1.set_ylabel("Fitness", fontsize='medium')
	ax1.plot(list(range(0, parameters['MAX_ITR'], step)), best_ger_step, 'g--', label='Melhor Fitness: ' + str (graph.best_global.fitness))
	ax1.legend(ncol=3)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Media e Mediana da fitness")
	ax2.set_xlabel("Iterações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')
	ax2.plot(list(range(0, parameters['MAX_ITR'], step)), avg_ger_step, 'r--', label='Media Fitness: %.4f' % graph.avg_fitness)
	ax2.plot(list(range(0, parameters['MAX_ITR'], step)), median_ger_step, 'b--', label='Mediana Fitness: %.4f' % graph.median_fitness)
	ax2.legend(ncol=1)
	ax2.tick_params(labelsize=18)

	ax3.set_title("Comparação entre as fitness")
	ax3.set_xlabel("Iterações", fontsize='medium')
	ax3.set_ylabel("Fitness", fontsize='medium')
	ax3.plot(list(range(0, parameters['MAX_ITR'], step)), best_ger_step, 'g--', label='Melhor Fitness: %.4f' % graph.best_global.fitness)
	ax3.plot(list(range(0, parameters['MAX_ITR'], step)), avg_ger_step, 'r--', label='Media Fitness: %.4f' % graph.avg_fitness)
	ax3.plot(list(range(0, parameters['MAX_ITR'], step)), median_ger_step, 'b--', label='Mediana Fitness: %.4f' % graph.median_fitness)
	ax3.legend(ncol=1)
	ax3.tick_params(labelsize=18)

	parameters = "_".join([str(arg) for arg in parameters.values()])

	print(colored("\033[1m"+"-> Graphic saved in: " + 'graficos/'+name_save+parameters+
				  '_fitness='+str(graph.best_global.fitness)+'.pdf\n', "green"))

	fig.savefig('graficos/'+name_save+parameters+'_fitness='+str(graph.best_global.fitness)+'.pdf')

def plot_table(results, name_save=""):

	table = {"MAX_ITR": [],
			"NUM_CITIES": [],
			"NUM_ANTS": [],
			"ALPHA": [],
			"BETA": [],
			"FITNESS": [],
			"P": [],
			"Q": []}  

	for i in results:
		table["MAX_ITR"].append(i[1]["MAX_ITR"])
		table["NUM_CITIES"].append(i[1]["NUM_CITIES"])
		table["NUM_ANTS"].append(i[1]["NUM_ANTS"])
		table["ALPHA"].append(i[1]["ALPHA"])
		table["BETA"].append(i[1]["BETA"])
		table["FITNESS"].append("%.2f" % i[0].best_global.fitness)
		table["P"].append(i[1]["P"])
		table["Q"].append(i[1]["Q"])

	df = pd.DataFrame(data=table)

	fig, ax = plt.subplots()

	fig.patch.set_visible(False)
	plt.axis("off")
	plt.grid("off")
	fig.set_size_inches(6, 3)
	ax.set_title("Execuções", y=1.2, fontdict={"fontsize": 12})

	the_table = ax.table(cellText=df.values,colLabels=df.columns, cellLoc="center", loc="center")
	the_table.auto_set_font_size(False)
	the_table.set_fontsize(6)

	fig.tight_layout()
	fig.savefig("tabelas/table_"+name_save+".pdf", dpi=500)
	print(colored("\033[1m"+"\n-> Tabela salva em: " + "tabelas/table_"+name_save+".pdf", "green"))
	print("\nTabela: \n", df)

if __name__ == "__main__":

	args = get_args()
	results = pickle.load(open(args['f'], 'rb'))
	plot_results(results, args)