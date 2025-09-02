import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load real metrics data
csv_file = "real_metrics.csv"  # Updated path to project root

df = pd.read_csv(csv_file)

# Extract features (cpu, memory)
X_train = df[["cpu", "memory"]].values

# Train Isolation Forest with very low contamination
model = IsolationForest(contamination=0.0001, random_state=42)
model.fit(X_train)

# Create model directory if it doesn't exist
os.makedirs("app/model", exist_ok=True)

# Save the trained model
joblib.dump(model, "app/model/isolation_forest.pkl")
print("Model retrained and saved to app/model/isolation_forest.pkl") 