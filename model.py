import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("disease_dataset.csv")

X = data.drop(["disease", "solution"], axis=1)
y = data["disease"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "disease_model.pkl")

solution_dict = dict(zip(data["disease"], data["solution"]))
joblib.dump(solution_dict, "disease_solution.pkl")

print("High-level model trained & saved!")