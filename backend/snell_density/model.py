import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
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

model_type = "rf"

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# train model
if model_type == "lr":
    model = LinearRegression()
    model.fit(X_train, y_train)
    # evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse) 
    # save model
    with open("backend/snell_density/lr.pkl", "wb") as f:
        pickle.dump(model, f)
elif model_type == "nn":
    model = Sequential([
    Dense(64, input_dim=X_train.shape[1], activation='relu'),  # input layer
    Dense(32, activation='relu'),  # hidden layer
    Dense(1)  # output layer
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)
    # evaluate
    mse = model.evaluate(X_test, y_test, verbose=0)
    print("Mean Squared Error:", mse)
    # save model
    model.save("backend/snell_density/nn.h5")
elif model_type == "dt":
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
    # Save the model
    with open("backend/snell_density/dt.pkl", "wb") as f:
        pickle.dump(model, f)
elif model_type == "rf":
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
    # Save the model
    with open("backend/snell_density/rf.pkl", "wb") as f:
        pickle.dump(model, f)