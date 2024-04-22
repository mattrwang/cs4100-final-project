# Northeastern Productivity App

## Start Web App:

#### Backend:

- `cd backend`
- `pip install flask` if not installed already
- `set FLASK_APP=app`
- `flask run`

#### How to Run Week Planner
To run week planner, you can run `results.ipynb`. First, you will need to select a set of tasks to use. You can either use one ofthe pre-existing tasks in `sample_tasks` or add your own set of tasks to that folder following the structure of existing sets of tasks. Then you need to generate a random plan using the `save_random_plan` method. Be sure to sepcify the task file you created in the previous step. Next, run the `get_results` method specifying your task file, random plan file (from the previous step), and home address. To run the algorithm once make sure the `n_runs` parameter is to as 1. 

#### Frontend:

- Open a new terminal
- `cd frontend`
- `npm install`
- `npm start`

