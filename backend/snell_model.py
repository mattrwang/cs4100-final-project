import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def load_model(model_path="snell_density/model.pkl"):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def featurize(date, time):
    breaks = [
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-01-02"),
        pd.Timestamp("2024-01-03"),
        pd.Timestamp("2024-01-04"),
        pd.Timestamp("2024-01-05"),
        pd.Timestamp("2024-01-06"),
        pd.Timestamp("2024-01-07"),
        pd.Timestamp("2024-01-15"),
        pd.Timestamp("2024-02-19"),
        pd.Timestamp("2024-03-04"),
        pd.Timestamp("2024-03-05"),
        pd.Timestamp("2024-03-06"),
        pd.Timestamp("2024-03-07"),
        pd.Timestamp("2024-03-08"),
        pd.Timestamp("2024-03-09"),
        pd.Timestamp("2024-03-10"),
        pd.Timestamp("2024-04-15"),
        pd.Timestamp("2024-05-27"),
        pd.Timestamp("2024-06-19"),
        pd.Timestamp("2024-07-04"),
        pd.Timestamp("2024-09-02"),
        pd.Timestamp("2024-10-14"),
        pd.Timestamp("2024-11-11"),
        pd.Timestamp("2024-11-27"),
        pd.Timestamp("2024-11-28"),
        pd.Timestamp("2024-11-29"),
        pd.Timestamp("2024-11-30"),
        pd.Timestamp("2024-12-01"),
        pd.Timestamp("2024-12-16"),
        pd.Timestamp("2024-12-17"),
        pd.Timestamp("2024-12-18"),
        pd.Timestamp("2024-12-19"),
        pd.Timestamp("2024-12-20"),
        pd.Timestamp("2024-12-21"),
        pd.Timestamp("2024-12-22"),
        pd.Timestamp("2024-12-23"),
        pd.Timestamp("2024-12-24"),
        pd.Timestamp("2024-12-25"),
        pd.Timestamp("2024-12-26"),
        pd.Timestamp("2024-12-27"),
        pd.Timestamp("2024-12-28"),
        pd.Timestamp("2024-12-29"),
        pd.Timestamp("2024-12-30"),
        pd.Timestamp("2024-12-31"),
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
    model = load_model()
    density = model.predict([features])[0]
    return density

# def generate_predictions(year=2024):
#     predictions = []

#     start_date = f"{year}-01-01 00:00:00"
#     end_date = f"{year}-12-31 23:00:00"

#     date_range = pd.date_range(start=start_date, end=end_date, freq="h")

#     for date in date_range:
#         date_str = date.strftime("%Y-%m-%d")
#         time = int(date.strftime("%H"))
#         density = predict_density(date_str, time)
#         predictions.append(density)

#     return predictions

# def plot_weekly_heatmaps(predictions, year=2024):
#     weeks_in_year = 52
#     structured_predictions = np.array(predictions).reshape((weeks_in_year, 7, 24))

#     start_date = pd.Timestamp(f"{year}-01-01")

#     for week in range(weeks_in_year):
#         week_start_date = start_date + pd.Timedelta(days=week*7)
#         week_end_date = week_start_date + pd.Timedelta(days=6)

#         week_end_date = min(week_end_date, pd.Timestamp(f"{year}-12-31"))
#         title = f"Week {week+1} ({week_start_date.strftime("%b %d")} - {week_end_date.strftime("%b %d")}, {year})"


#         plt.figure(figsize=(10, 5))
#         sns.heatmap(structured_predictions[week], cmap="viridis", annot=False, cbar=True)
#         plt.title(title)
#         plt.xlabel("Hour of Day")
#         plt.ylabel("Day of Week")
#         plt.xticks(np.arange(0.5, 24.5, 1), np.arange(1, 25))
#         plt.yticks(np.arange(0.5, 7.5, 1), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], rotation=0)
#         save_path = f"snell_density/heatmaps/week_{week+1}.png"
#         plt.savefig(save_path)
#         plt.close()

# def plot_leftovers(predictions, year=2024):
#     start_date = pd.Timestamp(f"{year}-12-31") - pd.Timedelta(days=len(predictions)//24 - 1)

#     days = len(predictions) // 24
#     structured_predictions = np.array(predictions).reshape((days, 24))

#     plt.figure(figsize=(10, 2 * days))
#     sns.heatmap(structured_predictions, cmap="viridis", annot=False, cbar=True)
    
#     if days > 1:
#         end_date = start_date + pd.Timedelta(days=days - 1)
#         title = f"Last Days ({start_date.strftime("%b %d")} - {end_date.strftime("%b %d")}, {year})"
#     else:
#         title = f"Last Day ({start_date.strftime("%b %d")}, {year})"
    
#     plt.title(title)
#     plt.xlabel("Hour of Day")
#     plt.ylabel("Day")
#     plt.xticks(np.arange(0.5, 24.5, 1), np.arange(1, 25))
#     plt.yticks(np.arange(0.5, days + 0.5, 1), ["Mon", "Tue"], rotation=0)
#     save_path = "snell_density/heatmaps/week_53.png"
#     plt.savefig(save_path)
#     plt.close()


# predictions = generate_predictions()
# plot_weekly_heatmaps(predictions[:52*7*24])
# plot_leftovers(predictions[52*7*24:])
