from sklearn.ensemble import IsolationForest
import numpy as np
import joblib

model = joblib.load("model/isolation_forest.pkl")

def is_anomalous(cpu, memory, latency):
    X = np.array([[cpu, memory, latency]])
    score = model.decision_function(X)[0]
    is_outlier = model.predict(X)[0] == -1
    return is_outlier, score 