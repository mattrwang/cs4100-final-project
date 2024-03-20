""" hill_descent.py
Hill descent algorithms to use for day planning.
"""
import sys
import numpy as np
import random


def energyfunction(plan, tasks):
	'''
	Computes the energy as the sum of the transportation times
	and perceived energy for each task in the given plan.
	'''
	pass
	"""shortest_path, _ = ASTAR(maze, start, goal)
	path_matrix = BFS(maze, start)
	num_unreachable = np.sum(path_matrix == -1)
	energy = shortest_path + num_unreachable"""

	return -1
"""
def HILLDESCENT(maze, start_cell, goal_state, iterations):
	'''
	Fill in this function to implement Hill Descent local search.

	Your function should return the best solution found, 
	which should be a tuple containing 2 elements:

	1. The best maze found, which is a 2-dimensional numpy array.
	2. The energy of the best maze found.

	Note that you should make a local copy of the maze 
	before making any changes to it.

	If using print statements to debug, please make sure
	to remove them before your final submisison.
	'''
	new_maze = maze.copy()
	k = maze.shape[0]
	energy = energyfunction(new_maze, start_cell, goal_state)
	for _ in range(iterations):
		# pick a random cell to change that is not the goal state
		r, c = np.random.randint(0, k), np.random.randint(0, k)
		while (r, c) == goal_state:
			r, c = np.random.randint(0, k), np.random.randint(0, k)
		# store current jump value at randomly chosen cell
		old_j = new_maze[r, c]
		# pick new random jump value
		new_j = np.random.randint(1, k)
		# set randomly chosen cell's jump value to new jump value
		new_maze[r, c] = new_j
		# get new energy of the maze
		new_energy = energyfunction(new_maze, start_cell, goal_state)
		# retain the change if the energy is lower
		if energy > new_energy:
			energy = new_energy
		# otherwise reverse the change
		else:
			new_maze[r, c] = old_j
			energy = energyfunction(new_maze, start_cell, goal_state)
	return new_maze, energy


def HILLDESCENT_RANDOM_RESTART(maze, start_cell, goal_state, iterations, num_searches):
	'''
	Fill in this function to implement Hill Descent local search with Random Restarts.

	For a given number of searches (num_searches), run hill descent search.

	Keep track of the best solution through all restarts, and return that.

	Your function should return the best solution found, 
	which should be a tuple containing 2 elements:

	1. The best maze found, which is a 2-dimensional numpy array.
	2. The energy of the best maze found.

	Note that you should make a local copy of the maze 
	before making any changes to it.

	You will also need to keep a separate copy of the original maze
	to use when restarting the algorithm each time.

	If using print statements to debug, please make sure
	to remove them before your final submisison.
	'''
	# initialize best maze and mest energy
	best_maze = None
	best_energy = 100000000
	# run hill descent for the givne number of searches
	for _ in range(num_searches):
		# get the new maze and energy from running hill descent
		new_maze, new_energy = HILLDESCENT(maze, start_cell, goal_state, iterations)
		# save current maze and energy as best solution if new energy is lower than current best energy
		if new_energy < best_energy:
			best_maze = new_maze
			best_energy = new_energy
	return best_maze, best_energy



def HILLDESCENT_RANDOM_UPHILL(maze, start_cell, goal_state, iterations, probability):
	'''
	Fill in this function to implement Hill Descent local search with Random uphill steps.

	At each iteration, with probability specified by the probability
	argument, allow the algorithm to move to a worse state.

	Your function should return the best solution found, 
	which should be a tuple containing 2 elements:

	1. The best maze found, which is a 2-dimensional numpy array.
	2. The energy of the best maze found.

	Note that you should make a local copy of the maze
	before making any changes to it.

	If using print statements to debug, please make sure
	to remove them before your final submisison.
	'''
	#make a copy of current maze
	new_maze = maze.copy()
	# store dimension of maze
	k = maze.shape[0]
	# get energy of current maze
	energy = energyfunction(new_maze, start_cell, goal_state)
	# swap random's cell's jump values if the new maze it produces has a lower energy
	for _ in range(iterations):
		# pick a random cell to change that is not the goal state
		r, c = np.random.randint(0, k), np.random.randint(0, k)
		while (r, c) == goal_state:
			r, c = np.random.randint(0, k), np.random.randint(0, k)
		# store current jump value at randomly chosen cell
		old_j = new_maze[r, c]
		# pick new random jump value
		new_j = np.random.randint(1, k)
		# set randomly chosen cell's jump value to new jump value
		new_maze[r, c] = new_j
		# get energy of new maze
		new_energy = energyfunction(new_maze, start_cell, goal_state)
		# choose to retain change anyways with random probability 
		rand_prob = random.random()
		retain = rand_prob <= probability
		# retain the change if the energy is decreased
		# or with some probability of retaining
		if energy > new_energy or retain:
			energy = new_energy
		# otherwise reverse the change
		else:
			new_maze[r, c] = old_j
			energy = energyfunction(new_maze, start_cell, goal_state)
	return new_maze, energy
"""