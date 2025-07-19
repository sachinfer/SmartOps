#!/usr/bin/env python3
"""
Script to copy the updated monitor_pod_status.py to the monitor image
"""
import shutil
import os

# Copy the updated monitoring script
source = "app/monitor_pod_status.py"
destination = "monitor_pod_status.py"

if os.path.exists(source):
    shutil.copy2(source, destination)
    print(f"Copied {source} to {destination}")
else:
    print(f"Source file {source} not found") 