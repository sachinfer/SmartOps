# 🚀 SmartOps
**"SmartOps: AI-Driven DevOps Automation & Monitoring Platform"**

---

## 🚀 Project Overview

**SmartOps** is an AI-driven DevOps automation and monitoring platform designed to:

- Monitor Kubernetes workloads (CPU, memory, etc.) in real time.
- Detect anomalies in resource usage using machine learning (IsolationForest and potentially other models).
- Log and visualize predictions and anomalies for operational insight.
- Provide a web-based dashboard for live and historical analytics.
- Support cloud-native deployment (GKE/GCP) with automated CI/CD.

### Key Components

1. **Main Application (`smartops-app`)**: The core workload being monitored.
2. **Anomaly Detection Service (`smartops-anomaly`)**: Uses the sidecar pattern—one container runs the FastAPI prediction API, and a second container runs the anomaly loop, calling the API via localhost.
3. **Dashboard (`smartops-dashboard`)**: Streamlit UI for real-time and historical analytics, connects to SQLite in test/dev.
    - **Clean, modern interface:** Beautiful feature cards with hover effects and smooth animations.
    - **User-friendly navigation:** Clickable cards for easy access to all features.
    - **Namespace selection:** Dropdown to filter predictions and analytics by namespace (e.g., all, smartops, test).
    - **ML-based actions:** Recommended actions are generated based on actual resource usage and anomaly type.
    - **Recent predictions table:** Shows the latest predictions and recommended actions for each event.
    - **System summary:** Plain English summary of recent anomaly counts and system health.
4. **CI/CD Pipeline**: GitHub Actions for automated build, push, and deploy to GKE with robust failure handling.
5. **Kubernetes Manifests**: YAMLs for all deployments/services, using LoadBalancer for external access.

---

#### 🧩 Sidecar Pattern for Anomaly Detection

The anomaly detection service is deployed as a multi-container pod:
- **Container 1:** Runs the FastAPI app (serving `/predict`)
- **Container 2:** Runs the anomaly loop script, which fetches metrics and calls the FastAPI endpoint via `localhost:8000/predict`
- This pattern ensures clean separation of API and background logic, and is robust for cloud-native deployments.

---hi

## 📊 Current Project Status

- Main app and anomaly service are deployed and running in GKE.
- Dashboard is deployed and exposed via LoadBalancer with a clean, modern interface.
- All services are built and deployed automatically via GitHub Actions with improved failure handling.
- Anomaly detection is live, logging to both SQLite and MongoDB Atlas.
- Dashboard visualizes live and historical anomaly data from SQLite (and MongoDB if configured).
- Dashboard now supports namespace selection and user-friendly, actionable advice for non-technical users.
- RBAC and service accounts are configured for secure metrics access.
- All dependencies are now correctly included in Docker images.
- Pods are healthy after the last dependency fix.
- **Pipeline failure notifications** are now working correctly with dashboard integration.

---

## 🎨 Dashboard Features

### Clean, Modern Interface
- **Beautiful feature cards** with hover effects and smooth animations
- **Clickable navigation** - Click any card to navigate to the corresponding page
- **Responsive design** that works on all screen sizes
- **No duplication** - Clean, single-purpose interface

### Available Pages
1. **🏠 Overview** - Cluster health status and resource usage overview
2. **🔥 Anomaly Detection** - AI-powered anomaly detection and analysis
3. **🤖 AI Actions** - AI recommendations and action history
4. **🚀 Deployments** - Deployment workflow events and tracking
5. **🛰️ Pod Explorer & Logs** - Pod management and log viewing
6. **🔍 Cluster Explorer** - Cluster resource exploration
7. **🖥️ Kubernetes Shell** - kubectl command interface

### Overview Page Features
- **Cluster Health Score** - Overall health percentage with color-coded status
- **Resource Usage Gauges** - Interactive CPU and Memory usage visualization
- **Node Health Table** - Detailed node status with health indicators
- **Pod Status Summary** - Running, pending, failed, and total pod counts
- **Quick Actions** - Direct navigation to key features

---

## 🚦 Enhanced CI/CD Pipeline with Failure Handling

The GitHub Actions pipeline now includes robust failure handling and dashboard integration:

### Key Improvements
- **Smart pod ready detection** - Checks if pods are already ready before waiting
- **Timeout protection** - All curl commands have max-time limits to prevent hanging
- **Connectivity testing** - Verifies dashboard is responding before logging events
- **Graceful fallbacks** - Continues deployment even if dashboard is unavailable
- **Multiple failure notification points** - Catches failures at different stages

### Pipeline Stages
1. **Build & Push Images** - Docker images for all services
2. **Deploy to GKE** - Kubernetes deployments with step-by-step logging
3. **Wait for Dashboard** - Smart ready detection with connectivity testing
4. **Log Events** - Dashboard integration with fallback handling
5. **Notify Success/Failure** - Telegram notifications with dashboard links

### Failure Handling
- **`if: failure()`** - Triggers when any step fails
- **`if: always()`** - Always runs regardless of success/failure
- **Dashboard logging** - Attempts to log failures to dashboard if available
- **Telegram notifications** - Always sends notifications with pipeline links

---

## 📢 Telegram Alerting & Bot Commands

SmartOps integrates with Telegram for real-time anomaly alerts and basic cluster status commands:

- **Anomaly Alerts:**
  - When an anomaly is detected, a detailed alert is sent to your configured Telegram chat or group (with CPU, memory, details, and a dashboard link).
  - Alerts use Markdown formatting for clarity.
- **Bot Commands:**
  - In your Telegram group, type `kubectl get nodes` or `kubectl get pods -n smartops`.
  - The bot will reply with the output, allowing you to check cluster and pod status from Telegram.

### Setup Steps
1. Create a Telegram bot with @BotFather and get the token.
2. Add the bot to your group and get the group chat ID (negative number).
3. Configure the bot token and chat ID in `anomaly_loop.py`.
4. Redeploy the anomaly service.

You will now receive both anomaly alerts and be able to query your cluster from Telegram!

---

## 🚨 Kubernetes-Native Log Monitoring & Non-200 Alerting

SmartOps now supports real-time monitoring of application logs directly from Kubernetes using the Kubernetes API. The anomaly-loop sidecar streams logs from the main app container and sends alerts for any non-200 HTTP responses (e.g., 404, 500) with actionable advice.

### How It Works
- The anomaly-loop container uses the Kubernetes Python client to stream logs from the main app container in the same pod.
- Any log line with a non-200 status code triggers an alert (e.g., via Telegram), including the status, log line, and recommended action.

### Setup Steps
1. **Environment Variables**
   Add these to the `anomaly-loop` container in your deployment YAML:
   ```yaml
   env:
     - name: MY_POD_NAMESPACE
       valueFrom:
         fieldRef:
           fieldPath: metadata.namespace
     - name: MY_POD_NAME
       valueFrom:
         fieldRef:
           fieldPath: metadata.name
     - name: MY_CONTAINER_NAME
       value: fastapi  # (or your main app container name)
   ```
2. **RBAC Permissions**
   Your service account must have access to `pods` and `pods/log`:
   ```yaml
   - apiGroups: [""]
     resources: ["pods"]
     verbs: ["get", "list", "watch"]
   - apiGroups: [""]
     resources: ["pods/log"]
     verbs: ["get", "watch", "list"]
   ```
3. **Startup**
   The anomaly-loop will automatically start log monitoring and send alerts for non-200 logs.

### Troubleshooting
- If you do not receive alerts:
  - Check the anomaly-loop logs for debug output (environment variables, log lines, regex matches).
  - Ensure the environment variables are set correctly in the container.
  - Ensure the service account has the correct RBAC permissions.
  - Make sure the main app container name matches `MY_CONTAINER_NAME`.
  - Trigger a non-200 response (e.g., 404, 500) and check the logs for alert activity.

---

## 🛡️ Pod Monitoring & Telegram Alerts

A custom Python script (`monitor_pod_status.py`) is provided to monitor all pods in the `smartops` namespace and send real-time alerts to Telegram:

- **Red alert** if any pod is not running or has restarted.
- **Green (recovery) alert** if a pod transitions from a non-running state to Running.
- **Red alert** if any previously-seen pod is now missing (deleted or disappeared).

### How It Works
- The script tracks the last known status of each pod in `pod_status.json`.
- On each run, it compares the current pod list and statuses to the previous run, sending alerts for failures, recoveries, and missing pods.

### Usage
1. **Configure your Telegram bot token and chat ID** in the script (already set for SmartOps).
2. **Run the script manually:**
   ```sh
   python smartops-ai/app/monitor_pod_status.py
   ```
3. **Schedule the script** for continuous monitoring (e.g., with cron or as a Kubernetes CronJob):
   ```sh
   */5 * * * * python /path/to/SmartOps/smartops-ai/app/monitor_pod_status.py
   ```
4. **Alerts** will be sent to your configured Telegram group for any pod failures, recoveries, or missing pods in the `smartops` namespace.

### Extending Monitoring
- To monitor additional namespaces, modify the script to loop over a list of namespaces.
- To add resource usage or log-based alerts, extend the script with additional checks.

---

## 🚀 Automated Monitoring CronJob Deployment

The SmartOps GitHub Actions pipeline now automatically builds, pushes, and deploys a Kubernetes CronJob for monitoring your cluster:

- **Location:** `smartops-ai/app/monitor_pod_status.py` (script), `smartops-ai/app/Dockerfile.monitor` (Dockerfile), `smartops-ai/k8s/monitor-cronjob.yaml` (CronJob manifest)
- **Pipeline Integration:** The pipeline builds the monitor image and applies the CronJob manifest after each deployment.
- **Schedule:** The CronJob runs every 1 minute (`* * * * *`), checking all Deployments in the `smartops` namespace.
- **Alerting:**
  - Alerts if any Deployment has fewer running pods than expected.
  - Alerts if a Deployment is scaled to zero or pods are missing for more than a minute.
  - Alerts are sent to your configured Telegram group.

### How It Works
- If a pod is deleted and not immediately replaced, you will receive an alert within 1 minute.
- If a pod is deleted and replaced instantly (as with Deployments), no alert is sent unless the number of running pods drops below the desired replica count.
- The monitoring is continuous and fully automated—no manual intervention required after deployment.

### Customization
- To change the monitoring interval, edit the `schedule` field in `monitor-cronjob.yaml`.
- To monitor additional namespaces or add more checks, update the monitoring script and redeploy.

---

## 🏷️ Namespace-Aware Deployment Event Logging & Filtering

SmartOps now supports namespace-aware deployment event logging and dashboard filtering.

### How It Works
- Every deployment event (started, success, failed) is logged with a `namespace` field (default: `smartops`).
- The dashboard UI allows you to filter deployment events by namespace, making it easy to track deployments for specific environments or teams.

### How to Use

#### 1. **API Usage**
To log a deployment event with a namespace:
```bash
curl -X POST "http://<dashboard-service-ip>:8000/log_event" \
  -H "Content-Type: application/json" \
  -d '{"status": "started", "message": "Deployment started", "namespace": "smartops"}'
```

#### 2. **Workflow Integration**
In your GitHub Actions workflow, include the `namespace` field in all event POSTs:
```yaml
- name: Log Deployment Started (to dashboard API)
  run: |
    curl -X POST "http://<dashboard-service-ip>:8000/log_event" \
      -H "Content-Type: application/json" \
      -d '{"status": "started", "message": "Deployment started", "namespace": "smartops"}'
```

#### 3. **Dashboard Filtering**
- The dashboard now features a **Select Deployment Namespace** dropdown above the deployment events table.
- Choose a namespace to filter events, or select "all" to view all deployment events.

#### 4. **Default Namespace**
- If not specified, the namespace defaults to `smartops`.
- You can use any string to represent your environment, team, or project.

#### 5. **Schema**
The `deployment_events` table now includes:
- `timestamp` (IST)
- `status` (started, success, failed, etc.)
- `message`
- `namespace`

---

## 🟦 Real-Time Pod Explorer in the Dashboard

SmartOps now includes a powerful, interactive pod explorer directly in the Streamlit dashboard:

- **Available Pods Card:**
  - Shows the live count of all pods in the selected namespace (or all namespaces).
  - Click the card to reveal a table of all pods, updated in real time from your GCP Kubernetes cluster.

- **Namespace Filtering:**
  - Use the namespace dropdown at the top to filter the pod count and pod table by namespace.
  - Selecting "all" shows pods from all namespaces.

- **Pod Details Displayed:**
  - **Name:** Pod name
  - **Namespace:** Namespace the pod belongs to
  - **Status:** Running, Pending, etc.
  - **Node:** Node where the pod is scheduled
  - **Start Time:** When the pod started
  - **Restarts:** Total container restarts for the pod
  - **Images:** Container images used in the pod

- **How it Works:**
  - The dashboard calls the FastAPI backend `/pods` endpoint, which queries the Kubernetes API for live pod data.
  - The pod table and count update automatically as you switch namespaces or click the card.

- **Requirements:**
  - The FastAPI backend must run inside the cluster (or with access to the GKE API) and have permission to list pods.
  - The dashboard and backend must be able to communicate (usually via `localhost:8000` or the appropriate service name).

- **Extending:**
  - You can add more pod details (labels, IP, etc.) or actions (logs, delete) by updating the backend and dashboard code.

---

## 🤖 AI/ML Automation & Human-in-the-Loop Remediation

SmartOps now includes advanced AI/ML features for Kubernetes self-healing and operator-in-the-loop automation:

- **AI Recommendations (Pending Actions):**
  - When the ML model detects an actionable anomaly (e.g., high CPU on a "stress" pod), it logs a pending AI action instead of taking action automatically.
  - In the dashboard sidebar, you will see a list of pending AI actions (e.g., "Delete pod stress-cpu3").
  - You can review the reason and confirm the action (delete the pod) with a single click.
  - All actions are logged for auditability.

- **AI Action History:**
  - The dashboard sidebar includes a full history of all AI actions (pending, completed, failed), with timestamps, pod names, reasons, and status (color-coded).
  - This provides a complete audit trail of all AI-driven recommendations and operator responses.

- **Retrain Model Button:**
  - The dashboard sidebar includes a "Retrain Model" button.
  - When clicked, it triggers the backend to retrain the IsolationForest anomaly detection model using the latest data.
  - Success or error messages are shown in the UI.

- **Human-in-the-Loop Remediation:**
  - AI never deletes pods automatically. Instead, it recommends actions for operator review and confirmation.
  - This ensures safe, auditable, and explainable AI-driven operations.

### How to Test the AI/ML Workflow

1. **Trigger an Anomaly:**
   - Deploy a pod with "stress" in its name (e.g., using a stress test YAML) that consumes high CPU.
   - Wait for the anomaly loop to detect the anomaly.
2. **Review AI Recommendations:**
   - Open the dashboard sidebar and look for pending AI actions.
   - Review the reason and confirm the action to delete the pod.
3. **Check AI Action History:**
   - All actions (pending, completed, failed) are visible in the AI Action History table in the sidebar.
4. **Retrain the Model:**
   - Click the "Retrain Model" button in the sidebar to retrain the anomaly detection model using the latest data.

---

## 🆕 Advanced Dashboard Pages

### ⚖️ Auto-Scaling Recommendations & Control
- **What:** Uses AI to analyze CPU/memory usage trends and recommend optimal Horizontal Pod Autoscaler (HPA) settings for your workloads.
- **Features:**
  - View current usage and HPA settings for all pods.
  - Get AI-driven recommendations for min/max replicas.
  - Apply recommended HPA changes directly from the dashboard (calls backend API).

### 🕒 Incident Timeline & Postmortem Report Generator
- **What:** Auto-generates a timeline of incidents (anomalies, pod crashes, alerts) and lets you export postmortem PDF reports.
- **Features:**
  - Filter incidents by namespace or app.
  - View a timeline and audit trail of all incidents.
  - Generate and download postmortem PDF reports with root cause, impact, and remediation.
  - Save postmortem reports to the audit trail (calls backend API).

### 🔗 Service Dependency Map (Real-Time)
- **What:** Visualizes service-to-service communication using Kubernetes network flows or service mesh (e.g., Istio, Linkerd).
- **Features:**
  - Dynamic dependency graph of your microservices architecture.
  - Interactive visualization (with pyvis) and static fallback (networkx/matplotlib).
  - Helps identify cascading failures and bottlenecks.
  - Fetches real data from backend API if available, otherwise uses simulated data.
  - **Live Data Integration:**
    - You can connect this page to live service mesh or network flow data (e.g., Istio, Linkerd, Cilium).
    - Example: Use Prometheus or Kiali APIs to fetch real-time service-to-service edges.
    - The backend `/service_dependencies` endpoint can be updated to query your telemetry source and return edges like:
      ```json
      { "edges": [["frontend", "backend"], ["backend", "database"], ...] }
      ```
  - **Filtering:**
    - The backend endpoint can accept query parameters (e.g., `?namespace=smartops`) to filter the graph by namespace or app.
    - The Streamlit page can be updated to let users filter the dependency map interactively.
  - **Customization:**
    - Node coloring by namespace or app
    - Edge thickness by traffic volume
    - Tooltips with live metrics
    - Auto-refresh for real-time updates

**See the Service Dependency Map page for details and instructions on connecting to your live data source.**

---

## 🛠️ Recent Improvements & Fixes

### Dashboard UI Improvements
- **Removed Analytics page** - Streamlined navigation by removing redundant analytics functionality
- **Cleaned up duplication** - Removed repetitive navigation sections and feature descriptions
- **Modern interface** - Beautiful feature cards with hover effects and smooth animations
- **Better organization** - Single "Quick Access" section with clear navigation

### Pipeline Reliability Improvements
- **Smart pod ready detection** - Checks if pods are already ready before waiting
- **Timeout protection** - All network requests have max-time limits
- **Connectivity testing** - Verifies dashboard availability before logging events
- **Graceful fallbacks** - Continues deployment even if dashboard is unavailable
- **Better error handling** - Multiple failure notification points with detailed logging

### Service Communication Improvements
- **Dynamic IP resolution** - No more hardcoded IP addresses
- **Kubernetes service discovery** - Uses internal service names for communication
- **ConfigMap configuration** - Centralized service URLs and endpoints
- **Redundant logging** - Both external and internal logging for reliability

---

## ✅ Summary

- Your system is fully cloud-native, automated, and observable.
- You have real-time anomaly detection and analytics, with a modern, clean dashboard.
- The project is in a stable, production-ready state with robust failure handling.
- All services communicate reliably using Kubernetes service discovery.

---

## 🟢 Completed Tasks

- [x] Main app and anomaly service deployed to GKE
- [x] Dashboard deployed and exposed via LoadBalancer
- [x] CI/CD pipeline (GitHub Actions) for build, push, and deploy
- [x] Anomaly detection using IsolationForest
- [x] Logging predictions to SQLite and MongoDB Atlas
- [x] Streamlit dashboard for real-time and historical analytics
- [x] RBAC and service accounts for secure metrics access
- [x] All dependencies included in Docker images
- [x] Hotfix and redeploy steps automated
- [x] **Dashboard UI cleaned up and modernized**
- [x] **Pipeline failure handling improved**
- [x] **Service communication made more robust**
- [x] **Analytics page removed for streamlined navigation**

---

