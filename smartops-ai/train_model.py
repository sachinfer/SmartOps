import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

# Example training data: [cpu_usage, memory_usage]
X_train = np.array([
    [0.1, 0.2],
    [0.15, 0.25],
    [0.2, 0.22],
    [0.12, 0.18],
    [0.14, 0.19],
    [0.13, 0.21],
    [0.3, 0.4],   # normal
    [0.9, 0.95],  # anomaly
])

# Train the model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_train)

# Create directory if not exists
os.makedirs("model", exist_ok=True)

# Save the model
joblib.dump(model, "model/isolation_forest.pkl")
print("Model saved to model/isolation_forest.pkl")
