import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

csv_path = "backend/snell_density/data.csv"

df = pd.read_csv(csv_path)

X = df.drop('count', axis=1)
y = df['count']

model = LinearRegression()
model.fit(X, y)

with open("backend/snell_density/model.pkl", "wb") as f:
    pickle.dump(model, f)