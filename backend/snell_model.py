import pickle
import pandas as pd

def load_model(model_path="snell_density/model.pkl"):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def featurize(date, time):
    breaks = [
        pd.Timestamp('2024-01-01'),
        pd.Timestamp('2024-01-02'),
        pd.Timestamp('2024-01-03'),
        pd.Timestamp('2024-01-04'),
        pd.Timestamp('2024-01-05'),
        pd.Timestamp('2024-01-06'),
        pd.Timestamp('2024-01-07'),
        pd.Timestamp('2024-01-15'),
        pd.Timestamp('2024-02-19'),
        pd.Timestamp('2024-03-04'),
        pd.Timestamp('2024-03-05'),
        pd.Timestamp('2024-03-06'),
        pd.Timestamp('2024-03-07'),
        pd.Timestamp('2024-03-08'),
        pd.Timestamp('2024-03-09'),
        pd.Timestamp('2024-03-10'),
    ]
    features = []
    date = pd.Timestamp(date)
    features.append(date.month)
    features.append(date.day)
    features.append(date.year - 2021)
    features.append(time)
    features.append(date.weekday())
    is_break = date.floor("D") in breaks
    features.append(1 if is_break else 0)
    return features



def predict_density(date, time):
    features = featurize(date, time)
    print(features)
    model = load_model()
    density = model.predict([features])[0]
    return density