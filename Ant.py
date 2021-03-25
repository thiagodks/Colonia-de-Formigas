
class Ant:

	def __init__(self):
		self.route = []
		self.fitness = 0

	def update_route(self, city):
		self.route.append(city)

	def calc_fitness(self, adj_matrix):
		distance = 0
		for i in range(0, len(self.route)-1):
			distance += adj_matrix[self.route[i]][self.route[i+1]].distance
		distance += adj_matrix[self.route[i+1]][self.route[0]].distance
		self.fitness = distance

	def __str__(self):
		return ("\nroute: " + " - ".join([str(r) for r in self.route]) +
				"\nfitness: " + str(self.fitness)) 