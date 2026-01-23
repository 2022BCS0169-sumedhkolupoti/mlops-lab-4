import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
import os

# Load dataset (fixing the separator since UCI wine quality often uses ';')
# Use absolute path relative to this script to avoid CWD issues
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, '../dataset/wine-quality.csv')
df = pd.read_csv(dataset_path, sep=';')

# Basic Preprocessing
X = df.drop('quality', axis=1)
y = df['quality']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model (Experiment 3: Random Forest Regressor)
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Performance:")
print(f"MSE: {mse}")
print(f"R2: {r2}")

# Save results
os.makedirs('initial_model', exist_ok=True)
joblib.dump(model, 'initial_model/model.pkl')

metrics = {
    "mse": mse,
    "r2": r2
}

with open('initial_model/metrics.json', 'w') as f:
    json.dump(metrics, f)
