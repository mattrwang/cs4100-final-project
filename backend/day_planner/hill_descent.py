""" hill_descent.py
Hill descent algorithms to use for day planning.
"""
import numpy as np
from typing import List, Tuple
from WeekPlan import WeekPlan
from task import Task
from copy import deepcopy

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
	swapped_plan = deepcopy(plan)
	tasks = week_plan.tasks
	t1_day = 0
	t2_day = 0

	t1_day = np.where(np.any(swapped_plan == t1, axis=1))[0][0]
	t2_day = np.where(np.any(swapped_plan == t2, axis=1))[0][0]

	t1_start = np.where(swapped_plan[t1_day] == t1)[0][0]
	t2_start = np.where(swapped_plan[t2_day] == t2)[0][0]

	for i in range(t1_start):
		if swapped_plan[t1_day][i] == -t1:
			swapped_plan[t1_day][i] = 0

	for i in range(t2_start):
		if swapped_plan[t2_day][i] == -t2:
			swapped_plan[t2_day][i] = 0
	
	i,j = t1_start, t2_start
	
	while (i < len(plan[t1_day]) and (plan[t1_day][i] == t1 or plan[t1_day][i] < 0)):
		swapped_plan[t1_day][i] = 0
		i += 1
	while (j < len(plan[t2_day]) and (plan[t2_day][j] == t2 or plan[t2_day][j] < 0)):
		swapped_plan[t2_day][j] = 0
		j += 1
	
	swapped_plan[t2_day], status1 = week_plan.add_task_to_day(swapped_plan[t2_day], t1-1, tasks[t1-1], t2_start, int(t2_start + tasks[t1-1].total_hours * 12))
	swapped_plan[t1_day], status2 = week_plan.add_task_to_day(swapped_plan[t1_day], t2-1, tasks[t2-1], t1_start, int(t1_start + tasks[t2-1].total_hours * 12))

	if status1 == 1 and status2 == 1:
		return swapped_plan, status
	else:
		status = 0
		return plan, status

def HILLDESCENT(iterations: int, plan: np.array, week_plan: WeekPlan) -> Tuple[np.array, float]:
	best_plan = deepcopy(plan)
	best_energy = energy_function(best_plan, week_plan.tasks)
	
	for i in range(iterations):
		t1 = np.random.randint(1, len(week_plan.tasks)+1)
		t2 = np.random.randint(1, len(week_plan.tasks)+1)
		while t2 == t1 or t1 in week_plan.fixed_time_tasks or t2 in week_plan.fixed_time_tasks:
			t1 = np.random.randint(1, len(week_plan.tasks)+1)
			t2 = np.random.randint(1, len(week_plan.tasks)+1)

		new_plan, status = swap_tasks(t1, t2, best_plan, week_plan)
	
		while status == 0:
			t1 = np.random.randint(1, len(week_plan.tasks)+1)
			t2 = np.random.randint(1, len(week_plan.tasks)+1)
			while t2 == t1 or t1 in week_plan.fixed_time_tasks or t2 in week_plan.fixed_time_tasks:
				t1 = np.random.randint(1, len(week_plan.tasks)+1)
				t2 = np.random.randint(1, len(week_plan.tasks)+1)
			new_plan, status = swap_tasks(t1, t2, best_plan, week_plan)

		new_energy = energy_function(new_plan, week_plan.tasks)
		if best_energy > new_energy:
			best_energy = new_energy
			best_plan = new_plan

		print(best_plan)
	return best_plan, best_energy


def HILLDESCENT_RANDOM_RESTART(num_searches: int, iterations: int, plan: np.array, week_plan: WeekPlan) -> Tuple[np.array, float]:
    # initialize best plan and energy
    best_plan = deepcopy(plan)
    best_energy = 1000000000000

    # run hill descent for the given number of searches
    for _ in range(num_searches):
        # get the new plan and energy from running hill descent
        print('return', HILLDESCENT(iterations, best_plan, week_plan))
        new_plan, new_energy = HILLDESCENT(iterations, best_plan, week_plan)
        # save current plan and energy as best solution if new energy is lower than current best energy
        if new_energy < best_energy:
            best_plan = new_plan
            best_energy = new_energy
    
    return best_plan, best_energy

def HILLDESCENT_RANDOM_UPHILL(num_searches: int, iterations: int, plan: np.array, week_plan: WeekPlan) -> Tuple[np.array, float]:
	
	pass


"""
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