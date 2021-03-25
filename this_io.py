from scipy.spatial import distance
from termcolor import colored
from colored import attr
import numpy as np
import argparse
import sys

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', required=True, help='file input: -f example.txt')
	parser.add_argument('-t', required=True, help='type input: -t ADJM or EUC2D')
	parser.add_argument('-s', required=True, type=int, help='value of the best solution: -s 291')
	args = vars(parser.parse_args())

	print("\033[1m"+"\n-> File: ", args['f'])
	print("\033[1m"+"-> Type input: ", args['t'])
	print("\033[1m"+"-> value of the best solution: ", args['s'], attr("reset"),"\n")

	return args

def read_dist_matrix(file_name, sep=" ", type_file='EUC2D', start_line=0):

	dir_path = file_name
	size_indiv = sum(1 for _ in open(dir_path))
	dist_matrix = np.zeros((size_indiv, size_indiv), dtype=np.int32)
	file = open(dir_path, "r")
	
	for i, row in enumerate(file):
		values = row.split(sep)
		dist_matrix[i] = [int(j) for j in values if j.isdigit()]

	return dist_matrix, size_indiv

def read_coordinates(file_name, sep=" ", start_line=6):
	dir_path = file_name
	size_indiv = sum(1 for _ in open(dir_path)) - start_line
	file = open(dir_path, "r")
	coordinates = []
	for i, row in enumerate(file):
		if i >= start_line: 
			values = row.split(sep)
			values = [x for x in values if x != '']
			coordinates.append((float(values[1]), float(values[2].replace("\n", ""))))

	if len(values) != 3: raise Exception('Input file incompatible with the type provided') 
	return coordinates

def create_dist_matrix(coordinates):
	num_cities = len(coordinates)
	dist_matrix = np.zeros((num_cities, num_cities), dtype=np.int32)
	for i in range(0, num_cities):
		for j in range(0, num_cities):
			dist = int(distance.euclidean(coordinates[i], coordinates[j]) + 0.5)
			dist_matrix[i][j] = dist
			
	return dist_matrix, num_cities

def get_matrix(args):
	try:
		if args['t'] == "EUC2D":
			coordinates = read_coordinates(args['f'])
			dist_matrix, num_cities = create_dist_matrix(coordinates)
		else: 
			dist_matrix, num_cities = read_dist_matrix(args['f'])

	except Exception as e:
		print(colored("\033[1m"+"\n => [ERROR]: An error occurred while reading the input file, check the file and its format!\n", "red"))
		print(" => ", e, "\n")
		sys.exit()

	return dist_matrix, num_cities
