import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

# load dataset
csv_path = "backend/snell_density/data.csv"
df = pd.read_csv(csv_path)

# format data and labels
X = df.drop("count", axis=1)
y = df["count"]

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train model
model = LinearRegression()
model.fit(X_train, y_train)

# evaluate model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# save model
# with open("backend/snell_density/model.pkl", "wb") as f:
#     pickle.dump(model, f)