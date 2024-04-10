""" hill_descent.py
Hill descent algorithms to use for day planning.
"""
import numpy as np
from typing import List, Tuple
from WeekPlan import WeekPlan
from task import Task

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
	occ_intvs = [i for i in plan.flatten() if i!=0]
	# compute total energy
	total_energy = sum([mode2pe[tasks[abs(i)-1].mode]/12 if i<0 else tasks[i-1].pe/12 for i in occ_intvs])
	# total_energy = np.sum(np.vectorize(lambda x: mode2pe[tasks[abs(x)-1].mode]/12 if x<0 else tasks[x-1].pe/12)(occ_intvs))
	return total_energy

def swap_tasks(t1: int, t2: int, plan: np.array, week_plan: WeekPlan) -> Tuple[np.array, int]:
	status = 1
	new_plan = np.copy(plan)
	tasks = week_plan.tasks
	t1_day = 0
	t2_day = 0
	for i in range(len(new_plan)):
		for j in new_plan[i]:
			if j == t1:
				t1_day = i
				break
	
	for i in range(len(new_plan)):
		for j in new_plan[i]:
			if j == t2:
				t2_day = i
				break

	print(t1, t2)
	t1_start = np.where(new_plan[t1_day] == t1)[0][0]
	t2_start = np.where(new_plan[t2_day] == t2)[0][0]

	for i in range(t1_start):
		if new_plan[t1_day][i] == -t1:
			new_plan[t1_day][i] = 0

	for i in range(t2_start):
		if new_plan[t2_day][i] == -t2:
			new_plan[t2_day][i] = 0
	
	i,j = t1_start, t2_start
	while (i < len(new_plan[t1_day]) and (new_plan[t1_day][i] == t1 or new_plan[t1_day][i] < 0)):
		new_plan[t1_day][i] = 0
		i += 1
	while (j < len(new_plan[t2_day]) and (new_plan[t2_day][j] == t2 or new_plan[t2_day][j] < 0)):
		new_plan[t2_day][j] = 0
		j += 1
	
	new_plan[t2_day], status1 = week_plan.add_task_to_day(new_plan[t2_day], t1-1, tasks[t1-1], t2_start, int(t2_start + tasks[t1-1].total_hours * 12))
	new_plan[t1_day], status2 = week_plan.add_task_to_day(new_plan[t1_day], t2-1, tasks[t2-1], t1_start, int(t1_start + tasks[t2-1].total_hours * 12))

	if status1 == 1 and status2 == 1 and week_plan.valid_plan(new_plan):
		return new_plan, status
	else:
		status = 0
		return plan, status


def HILLDESCENT(iterations: int, plan: np.array, week_plan: WeekPlan) -> Tuple[np.array, float]:
	new_plan = np.copy(plan)
	tasks = week_plan.tasks
	energy = energy_function(new_plan, tasks)
	fixed_time_tasks = [t for t in tasks if t.fixed_time is not None and t.fixed_time[1] is not None]
	for _ in range(iterations):
		t1 = np.random.randint(1, len(tasks)+1)
		t2 = np.random.randint(1, len(tasks)+1)
		new_plan, status = swap_tasks(t1, t2, new_plan, week_plan)
		while status == 0 or tasks[t1-1] in fixed_time_tasks or tasks[t2-1] in fixed_time_tasks:
			t1 = np.random.randint(1, len(tasks)+1)
			t2 = np.random.randint(1, len(tasks)+1)
			new_plan, status = swap_tasks(t1, t2, new_plan, week_plan)

		new_energy = energy_function(new_plan, tasks)
		if energy > new_energy:
			energy = new_energy
		else:
			new_plan = plan	
		print(new_plan, energy)
		print(week_plan.valid_plan(new_plan))
	return new_plan, energy

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