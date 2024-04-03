#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
from matrix import Matrix
import networkx as nx
import heapq
import itertools


class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def greedy( self,time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		num_cities = len(cities)
		found_tour = False
		count = 0
		bssf = None
		start_time = time.time()
		impossible_path = False

		# implement greedy algorithm

		start_index = 0
		while not found_tour and start_index < num_cities - 1:
			# pick arbitrary city
			current_city = cities[start_index]
			visited_cities = [current_city]
			visited_indexes = set()
			visited_indexes.add(start_index)

			# visit every city
			while len(visited_indexes) < num_cities:
				# find the lowest cost to another unvisited city
				min_cost = np.inf
				min_index = -1

				# look at every other city that has not been visited
				for index, city in enumerate(cities):
					if index not in visited_indexes:
						# find the cost to the unvisited city
						cost_to = current_city.costTo(city)
						if cost_to < min_cost:
							# update the min cost and city index
							min_cost = cost_to
							min_index = index

				if min_index == -1:
					# no greedy path could be found
					impossible_path = True
					break

				# add the index to visited indexes
				visited_indexes.add(min_index)

				# set the current city to the one found
				current_city = cities[min_index]

				# add the current city to the list of visited cities
				visited_cities.append(current_city)


			if not impossible_path:
				# if the last city loops back to the original city, a tour has been found
				if visited_cities[-1].costTo(visited_cities[0]) < np.inf:
					found_tour = True
					count += 1

				bssf = TSPSolution(visited_cities)

			start_index += 1

		# end greedy algorithm
		end_time = time.time()
		results['cost'] = bssf.cost if found_tour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results



	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def branchAndBound(self, time_allowance=60.0):
		# get cities
		cities = self._scenario.getCities()
		num_cities = len(cities)

		# results variables
		results = {}
		found_tour = False
		bssf = None
		num_solutions = 0
		pruned = 0
		nodes_created = 0

		# initialize matrix
		matrix = Matrix(dimension=num_cities, cities=cities)
		lower_bound = matrix.reduce_matrix()

		# run greedy algorithm for an initial solution
		greedy_algo = self.greedy(time_allowance=60)
		best_cost = greedy_algo['cost']
		best_path = greedy_algo['soln'].route

		# initialize branch and bound search
		priority_queue = []
		max_queue_size = 0
		heapq.heappush(priority_queue, ([0], 0, matrix))  # initialized with ([city path], cost of path)

		start_time = time.time()

		# Start Brand and Bound Algorithm
		while priority_queue and time.time()-start_time < time_allowance:
			if len(priority_queue) > max_queue_size:
				max_queue_size = len(priority_queue)

			route = heapq.heappop(priority_queue)
			current_path, current_cost, matrix = route

			if current_cost > best_cost:
				pruned += 1
				continue

			if len(current_path) == num_cities:
				num_solutions += 1
				if current_cost < best_cost:
					best_path = current_path
					best_cost = current_cost
			else:
				for next_city in range(num_cities):
					if next_city not in current_path:
						matrix_copy = matrix.copy()
						nodes_created += 1

						next_cost = matrix_copy.update(current_path[-1], next_city)

						reduced_cost = matrix_copy.reduce_matrix()

						updated_path_cost = next_cost + reduced_cost + current_cost

						if updated_path_cost <= best_cost:
							heapq.heappush(priority_queue, (current_path + [next_city], updated_path_cost,
															matrix_copy))
						else:
							pruned += 1
		# end branch and bound algorithm

		# post processing
		city_path = []
		for index in best_path:
			city_path.append(cities[index])

		bssf = TSPSolution(city_path)


		if num_solutions > 0:
			found_tour = True

		end_time = time.time()

		# set results
		results['cost'] = bssf.cost if found_tour else math.inf
		results['time'] = end_time - start_time
		results['count'] = num_solutions
		results['soln'] = bssf
		results['max'] = max_queue_size
		results['total'] = nodes_created
		results['pruned'] = pruned
		return results

	@staticmethod
	def lower_bound_mst(matrix: Matrix, partial_tour: list[int]) -> float:
		# Create a graph from the matrix
		graph = nx.Graph(matrix.matrix)

		# Add edges from the partial tour to ensure connectivity
		for i in range(len(partial_tour) - 1):
			graph.add_edge(partial_tour[i], partial_tour[i + 1])
		graph.add_edge(partial_tour[-1], partial_tour[0])

		# Calculate the minimum spanning tree (MST) of the subgraph
		mst_edges = nx.minimum_spanning_edges(graph)

		# Calculate the sum of edge weights in the MST
		lower_bound = sum(matrix.get_cost(u, v) for u, v, _ in mst_edges)

		return lower_bound

	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		pass
