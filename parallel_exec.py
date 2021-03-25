from concurrent.futures import ProcessPoolExecutor
from termcolor import colored
from Graph import Graph
from colored import attr
import multiprocessing
from tqdm import tqdm
import this_io as io
from Ant import Ant
import itertools
import util
import util
import sys
import pickle

def main(parameters):

	prmt = {"INITIAL_PHEROMONE": parameters[0],
				  "MAX_ITR": parameters[1],
				  "NUM_CITIES": num_cities,
				  "NUM_ANTS": parameters[2],
				  "P": parameters[3],
                  "ALPHA": parameters[4],
                  "BETA": parameters[5],
                  "Q": parameters[6]}     

	ants = [Ant() for _ in range(0, prmt['NUM_ANTS'])]
	graph = Graph(prmt)
	graph.create_graph(distance_matrix, prmt['INITIAL_PHEROMONE'])
	
	for itr in range(0, prmt['MAX_ITR']):
		graph.insert_ants(ants)
		graph.build_routes()
		graph.update_pheromone()
		graph.calculate_log()
		if itr < prmt['MAX_ITR']-1:
			graph.clear_routes()

	return graph, prmt

INITIAL_PHEROMONE = [10**(-16)]
MAX_ITR = [50, 100, 200]
NUM_ANTS = [52, 104]
P = [0.4, 0.5, 0.6]
ALPHA = [1]
BETA = [5]
Q = [100]

all_list = [INITIAL_PHEROMONE, MAX_ITR, NUM_ANTS, P, ALPHA, BETA, Q]
parameters = list(itertools.product(*all_list)) 
executor = ProcessPoolExecutor()
num_args = len(parameters)
chunksize = int(num_args/multiprocessing.cpu_count())

args = io.get_args()
distance_matrix, num_cities = io.get_matrix(args)

print("\033[1m"+"-> INITIAL_PHEROMONE: ", INITIAL_PHEROMONE)
print("\033[1m"+"-> MAX_ITR: ", MAX_ITR)
print("\033[1m"+"-> NUM_ANTS: ", NUM_ANTS)
print("\033[1m"+"-> P: ", P)
print("\033[1m"+"-> ALPHA: ", ALPHA)
print("\033[1m"+"-> BETA: ", BETA)
print("\033[1m"+"-> Q: ", Q, attr("reset"), "\n")

results = [i for i in tqdm(executor.map(main, parameters),total=num_args)]

file_name = args['f'].split("/")
file_name = file_name[-1]

pickle.dump(results, open("resultados/results_"+file_name+".pickle", "wb"))
print("\033[1m"+"\n-> Results saved in: ", "resultados/results_"+file_name+".pickle\n")