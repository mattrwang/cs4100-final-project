""" hill_descent.py
Hill descent algorithms to use for day planning.
"""

import numpy as np
from typing import List
from Task import Task

def energy_function(plan: np.array, tasks: List[Task]) -> float:
	"""
	 Computes the energy of the plan as sum total of work and trasportation 
	 percevied eneregy for each interval.
        
		Args:
            plan (np.array): scheduled activites for the week
            tasks (List[Task]): tasks to be scheduled
		Returns:
		total_energy (float): total energy of the plan
    """ 
	# define dictionary that maps perceived energy per hour of doing each mode of transportation
	mode2pe = {'transit':4, 'walking':5 ,'driving':3 , 'bicycling':5}
	# get intervals occupied by tasks or transportation 
	occ_intvs = plan[np.nonzero(plan.flatten())]
	# compute total energy
	total_energy = np.sum(np.vectorize(lambda x: mode2pe[tasks[abs(x)-1].mode]/12 if x<0 else tasks[x-1].pe/12)(occ_intvs))
	return total_energy



# def HILLDESCENT(iterations: int, plan: np.array, tasks: List[Task], api_key: str) -> Tuple[plan, new_energy]:
# 	'''
# 	Fill in this function to implement Hill Descent local search.

# 	Your function should return the best solution found, 
# 	which should be a tuple containing 2 elements:

# 	1. The best maze found, which is a 2-dimensional numpy array.
# 	2. The energy of the best maze found.

# 	Note that you should make a local copy of the maze 
# 	before making any changes to it.

# 	If using print statements to debug, please make sure
# 	to remove them before your final submisison.
# 	'''
# 	new_plan = plan.copy()
# 	energy = energy_function(new_plan, tasks, api_key)
# 	for _ in range(iterations):
# 		# pick a random day
# 		rand_day = np.random.randint(0,7)
# 		# pick a random interval in the date
# 		rand_int = np.random.randint(0, rand_day.shape[0])
# 		# pick random day and interval in the day while the interval time is long enough a random cell to change that is not the goal state
# 		while (r, c) == goal_state:
# 			r, c = np.random.randint(0, k), np.random.randint(0, k)
		
# 		# store current jump value at randomly chosen cell
# 		old_j = new_maze[r, c]
# 		# pick new random jump value
# 		new_j = np.random.randint(1, k)
# 		# set randomly chosen cell's jump value to new jump value
# 		new_maze[r, c] = new_j
# 		# get new energy of the maze
# 		new_energy = energyfunction(new_maze, start_cell, goal_state)
# 		# retain the change if the energy is lower
# 		if energy > new_energy:
# 			energy = new_energy
# 		# otherwise reverse the change
# 		else:
# 			new_maze[r, c] = old_j
# 			energy = energyfunction(new_maze, start_cell, goal_state)
# 	return new_maze, energy

"""
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