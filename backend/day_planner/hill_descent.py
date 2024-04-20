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

	if status1 == 1 and status2 == 1 and week_plan.valid_day_tasks(swapped_plan):
		return swapped_plan, status
	else:
		status = 0
		return plan, status


def HILLDESCENT(iterations: int, plan: np.array, week_plan: WeekPlan) -> Tuple[np.array, float]:
	best_plan = deepcopy(plan)
	best_energy = energy_function(best_plan, week_plan.tasks)
	non_fixed_tasks = [i for i in range(1, len(week_plan.tasks) + 1) if i not in week_plan.fixed_time_tasks]
	
	for i in range(iterations):
		print(f'iter {i}')
		t1 = np.random.choice(non_fixed_tasks)
		t2 = np.random.choice(non_fixed_tasks)
		while t2 == t1:
			t2 = np.random.choice(non_fixed_tasks)

		new_plan, status = swap_tasks(t1, t2, best_plan, week_plan)
	
		while status == 0:
			t1 = np.random.choice(non_fixed_tasks)
			t2 = np.random.choice(non_fixed_tasks)
			while t2 == t1:
				t2 = np.random.choice(non_fixed_tasks)
			new_plan, status = swap_tasks(t1, t2, best_plan, week_plan)

		new_energy = energy_function(new_plan, week_plan.tasks)
		if best_energy > new_energy:
			best_energy = new_energy
			best_plan = new_plan

	return best_plan, best_energy


def HILLDESCENT_RANDOM_RESTART(num_searches: int, iterations: int, plan: np.array, week_plan: WeekPlan) -> Tuple[np.array, float]:
    # initialize best plan and energy
    best_plan = deepcopy(plan)
    best_energy = 1000000000000

    # run hill descent for the given number of searches
    for _ in range(num_searches):
        # get the new plan and energy from running hill descent
        new_plan, new_energy = HILLDESCENT(iterations, best_plan, week_plan)
        # save current plan and energy as best solution if new energy is lower than current best energy
        if new_energy < best_energy:
            best_plan = new_plan
            best_energy = new_energy
    
    return best_plan, best_energy

def HILLDESCENT_RANDOM_UPHILL(iterations: int, plan: np.array, week_plan: WeekPlan, p: float) -> Tuple[np.array, float]:
	best_plan = deepcopy(plan)
	best_energy = energy_function(best_plan, week_plan.tasks)
	non_fixed_tasks = [i for i in range(1, len(week_plan.tasks) + 1) if i not in week_plan.fixed_time_tasks]
	
	for i in range(iterations):
		print(f'iter {i}')
		t1 = np.random.choice(non_fixed_tasks)
		t2 = np.random.choice(non_fixed_tasks)
		while t2 == t1:
			t2 = np.random.choice(non_fixed_tasks)

		new_plan, status = swap_tasks(t1, t2, best_plan, week_plan)
	
		while status == 0:
			t1 = np.random.choice(non_fixed_tasks)
			t2 = np.random.choice(non_fixed_tasks)
			while t2 == t1:
				t2 = np.random.choice(non_fixed_tasks)
			new_plan, status = swap_tasks(t1, t2, best_plan, week_plan)

		new_energy = energy_function(new_plan, week_plan.tasks)
		if best_energy > new_energy:
			best_energy = new_energy
			best_plan = new_plan
		else:
			rand_prob = np.random.random()
			retain = rand_prob <= p
			if best_energy < new_energy and retain:
				best_energy = new_energy
				best_plan = new_plan
	return best_plan, best_energy