# Northeastern Productivity App

## Start Web App:

#### Backend:

- `cd backend`
- `pip install flask` if not installed already
- `set FLASK_APP=app`
- `flask run`

#### How to Run Week Planner
To use the week planner, run `results.ipynb`. First, you will need to select a set of tasks to use. You can either use one ofthe pre-existing task sets in `sample_tasks` or add your own set of tasks to that folder following the structure of existing task sets. Then,generate a random plan using the `save_random_plan` method. You do not need to do this if you are using an existing task set. Be sure to specify the task file you created in the previous step when running generating a random plan. Next, run the `get_results` method specifying your task file, random plan file (from the previous step), and home address. To run the algorithm once, set the `n_runs` parameter is to 1. Now you have generated an optimized week plan!

#### Frontend:

- Open a new terminal
- `cd frontend`
- `npm install`
- `npm start`

