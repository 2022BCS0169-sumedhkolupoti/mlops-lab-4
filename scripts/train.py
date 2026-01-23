import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
import os

# Define paths
# Script is in scripts/train.py. Dataset is in lab2/dataset/wine-quality.csv
# We are running from root usually, but let's use relative paths to be safe.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, 'lab2', 'dataset', 'wine-quality.csv')
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, 'artifacts')

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

print(f"Loading data from {DATA_PATH}...")
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"{DATA_PATH} not found.")

df = pd.read_csv(DATA_PATH, sep=';')

# Basic Preprocessing
print("Preprocessing data...")
X = df.drop('quality', axis=1)
y = df['quality']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
print("Training RandomForestRegressor...")
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("Evaluating model...")
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance: MSE={mse}, R2={r2}")

# Save results
model_path = os.path.join(ARTIFACTS_DIR, 'model.pkl')
metrics_path = os.path.join(ARTIFACTS_DIR, 'metrics.json')

print(f"Saving model to {model_path}...")
joblib.dump(model, model_path)

metrics = {
    "mse": mse,
    "r2": r2
}

print(f"Saving metrics to {metrics_path}...")
with open(metrics_path, 'w') as f:
    json.dump(metrics, f)

print("Training complete.")
