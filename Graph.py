import random
import numpy as np
from Ant import Ant

class Edge:

	def __init__(self, distance=0, pheromone=0):
		self.distance = distance
		self.pheromone = pheromone

	def __str__(self):
		return "(D: {dist}, P: {pher})".format(dist=self.distance, pher=self.pheromone)

class Graph:

	def __init__(self, parameters):
		self.num_vertices = parameters['NUM_CITIES']
		self.num_ants = parameters['NUM_ANTS']
		self.alpha = parameters['ALPHA']
		self.beta = parameters['BETA']
		self.p = parameters['P']
		self.q = parameters['Q']
		self.adj_matrix = []
		self.log_itr = []
		self.ants = []
		self.best_global = None

	def get_parameters(self):
		return ("\nNumber of Vertices: " + str(self.num_vertices) +
				"\nNumber of Ants: " + str(self.num_ants) +
				"\nAlpha: " + str(self.alpha) +
				"\nBeta: " + str(self.beta) +
				"\np: " + str(self.p) +
				"\nq: " + str(self.q))

	def create_graph(self, dist_matrix, initial_pheromone):
		self.adj_matrix = [Edge() for i in range(0, self.num_vertices)]
		for i in range(0, self.num_vertices): self.adj_matrix[i] = [Edge() for i in range(0, self.num_vertices)]

		for i in range(0, self.num_vertices):
			for j in range(0, self.num_vertices):
				self.adj_matrix[i][j].distance = dist_matrix[i][j]
				self.adj_matrix[i][j].pheromone = initial_pheromone

	def insert_ants(self, ants):
		self.ants = ants
		for i in range(0, self.num_ants):
			initial_position = random.randrange(0, self.num_vertices)
			self.ants[i].update_route(city=initial_position)

	def calc_probability(self, ant):
		current_position = ant.route[-1]
		neighborhood = [city for city in range(0, self.num_vertices) if city not in ant.route]
		summation = 0.0
		for j in neighborhood:
				summation += (self.adj_matrix[current_position][j].pheromone**self.alpha) * ((1/self.adj_matrix[current_position][j].distance)**self.beta)
		probability = {}
		for j in neighborhood:
			probability[j] = ((self.adj_matrix[current_position][j].pheromone**self.alpha) * ((1/self.adj_matrix[current_position][j].distance)**self.beta))/summation

		return probability

	def roulette(self, probability):
		r = random.random()
		aux_sum = 0.0
		for j in probability:
			aux_sum += probability[j]
			if aux_sum >= r:
				return j

	def build_routes(self):
		for i in range(0, self.num_ants):
			for j in range(0, self.num_vertices-1):
				probability = self.calc_probability(self.ants[i])
				next_vertice = self.roulette(probability)
				self.ants[i].update_route(city=next_vertice)
			self.ants[i].calc_fitness(self.adj_matrix)

	def calculate_log(self):
		indiv_fitness = [ant.fitness for ant in self.ants]
		self.avg_fitness = np.mean(indiv_fitness)
		self.median_fitness = np.median(indiv_fitness)
		self.best_solution = min(self.ants, key=lambda a: a.fitness)
		if self.best_global == None or (self.best_solution.fitness < self.best_global.fitness):
			self.best_global = Ant()
			self.best_global.fitness = self.best_solution.fitness
			self.best_global.route = self.best_solution.route 
		self.log_itr.append((self.best_solution.fitness, self.avg_fitness, self.median_fitness))

	def clear_routes(self):
		for i in range(0, self.num_ants):
			self.ants[i].route.clear()

	def update_pheromone(self):
		for i in range(0, self.num_vertices):
			for j in range(0, self.num_vertices):
				aux_sum = 0.0
				for ant in self.ants:
					if (ant.route.index(i) == (ant.route.index(j)-1)) or ((ant.route.index(i) == self.num_vertices-1) and (ant.route.index(j) == 0)):
						aux_sum += self.q / ant.fitness
				self.adj_matrix[i][j].pheromone = ((1 - self.p) * self.adj_matrix[i][j].pheromone) + aux_sum

	def print_population(self):
		print("Population: ")
		for ant in self.ants: print(ant)

	def print_matrix(self):
		print("")
		for i in range(0, self.num_vertices):
			for j in range(0, self.num_vertices):
				print(self.adj_matrix[i][j], end=' ')
			print("")
				