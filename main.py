from termcolor import colored
from tqdm import tqdm
import this_io as io
from Graph import Graph
from Ant import Ant
from tqdm import tqdm
import plot_charts as pc


if __name__ == "__main__":

	args = io.get_args()
	distance_matrix, num_cities = io.get_matrix(args)

	#default
	parameters = {"INITIAL_PHEROMONE": 10**(-16),
				  "MAX_ITR": 50,
				  "NUM_CITIES": num_cities,
				  "NUM_ANTS": num_cities * 2,
				  "ALPHA": 1,
				  "BETA": 5,
				  "P": 0.5,
				  "Q": 100}

	ants = [Ant() for _ in range(0, parameters['NUM_ANTS'])]
	graph = Graph(parameters)
	graph.create_graph(distance_matrix, parameters['INITIAL_PHEROMONE'])
	
	for itr in tqdm(range(0, parameters['MAX_ITR']), position=0, leave=True):
		graph.insert_ants(ants)
		graph.build_routes()
		graph.update_pheromone()
		graph.calculate_log()
		if itr < parameters['MAX_ITR']-1:
			graph.clear_routes()

	print(graph.get_parameters())
	print("\nBest Solution: ", graph.best_solution)
	pc.plot_graphics(graph, parameters)