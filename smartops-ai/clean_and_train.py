import os
import sys
import subprocess

LOG_ORIG = "app.log"
LOG_CLEAN = os.path.join("smartops-ai", "app_clean.log")
PARSED_CSV = "parsed_logs.csv"

# 1. Remove null bytes from app.log and write to smartops-ai/app_clean.log
with open(LOG_ORIG, "rb") as f:
    data = f.read().replace(b'\x00', b'')
with open(LOG_CLEAN, "wb") as f:
    f.write(data)
print(f"Cleaned null bytes: {LOG_ORIG} -> {LOG_CLEAN}")

# 2. Parse the cleaned log (run from smartops-ai dir)
print("Parsing cleaned log...")
subprocess.run([sys.executable, "train_log_parser.py", "app_clean.log", PARSED_CSV], cwd="smartops-ai")

# 3. Train the Isolation Forest model
print("Training Isolation Forest model...")
subprocess.run([sys.executable, "train_model.py", PARSED_CSV], cwd="smartops-ai")

print("Done! Model saved to smartops-ai/model/isolation_forest.pkl") 