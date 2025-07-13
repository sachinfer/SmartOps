import sqlite3

DB_PATH = "/app/dashboard/data/data.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if pod_name and labels columns exist
cursor.execute("PRAGMA table_info(anomalies)")
columns = [row[1] for row in cursor.fetchall()]

select_cols = ["id", "timestamp", "cpu", "memory", "prediction"]
if "pod_name" in columns:
    select_cols.append("pod_name")
if "labels" in columns:
    select_cols.append("labels")

query = f"SELECT {', '.join(select_cols)} FROM anomalies ORDER BY id DESC LIMIT 10"
cursor.execute(query)
rows = cursor.fetchall()

print("Most recent anomalies:")
print(" | ".join(select_cols))
for row in rows:
    print(" | ".join(str(x) for x in row))

conn.close() 