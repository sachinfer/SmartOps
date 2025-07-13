from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os

# Get the current directory and construct the model path
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "model", "isolation_forest.pkl")

# Debug: Print the path and check if file exists
print(f"Current directory: {current_dir}")
print(f"Model path: {model_path}")
print(f"Model file exists: {os.path.exists(model_path)}")

# List contents of the model directory
model_dir = os.path.join(current_dir, "model")
if os.path.exists(model_dir):
    print(f"Model directory contents: {os.listdir(model_dir)}")
else:
    print(f"Model directory does not exist: {model_dir}")

model = joblib.load(model_path)

def is_anomalous(cpu, memory, latency):
    X = np.array([[cpu, memory, latency]])
    score = model.decision_function(X)[0]
    is_outlier = model.predict(X)[0] == -1
    return is_outlier, score 