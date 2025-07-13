# SmartOps
“SmartOps: AI-Driven DevOps Automation & Monitoring Platform”

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
    - **User-friendly interface:** Color-coded banners, plain English advice, and actionable recommendations.
    - **Namespace selection:** Dropdown to filter predictions and analytics by namespace (e.g., all, smartops, test).
    - **ML-based actions:** Recommended actions are generated based on actual resource usage and anomaly type.
    - **Recent predictions table:** Shows the latest predictions and recommended actions for each event.
    - **System summary:** Plain English summary of recent anomaly counts and system health.
4. **CI/CD Pipeline**: GitHub Actions for automated build, push, and deploy to GKE.
5. **Kubernetes Manifests**: YAMLs for all deployments/services, using LoadBalancer for external access.

---

#### 🧩 Sidecar Pattern for Anomaly Detection

The anomaly detection service is deployed as a multi-container pod:
- **Container 1:** Runs the FastAPI app (serving `/predict`)
- **Container 2:** Runs the anomaly loop script, which fetches metrics and calls the FastAPI endpoint via `localhost:8000/predict`
- This pattern ensures clean separation of API and background logic, and is robust for cloud-native deployments.

---

## 📊 Current Project Status

- Main app and anomaly service are deployed and running in GKE.
- Dashboard is deployed and exposed via LoadBalancer.
- All services are built and deployed automatically via GitHub Actions.
- Anomaly detection is live, logging to both SQLite and MongoDB Atlas.
- Dashboard visualizes live and historical anomaly data from SQLite (and MongoDB if configured).
- Dashboard now supports namespace selection and user-friendly, actionable advice for non-technical users.
- RBAC and service accounts are configured for secure metrics access.
- All dependencies are now correctly included in Docker images.
- Pods are healthy after the last dependency fix.

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

## 🚦 Telegram Deployment Notifications from CI/CD

You can receive Telegram alerts when a deployment starts, succeeds, or fails via your GitHub Actions pipeline.

### How to Set Up
1. **Add your bot to your Telegram group.**
2. **Send a message in the group as a user** (this is required for Telegram to allow the bot to send messages).
3. **Get your group chat ID** (it will look like `-100xxxxxxxxxx`).
4. **Add your bot token and chat ID as GitHub repository secrets:**
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
5. **Your workflow will send messages at key stages:**
   - 🚀 *Production deployment started!*
   - ✅ *Production deployment completed successfully!*
   - ❌ *Production deployment failed!*

### Example Workflow Snippet
```yaml
- name: Notify Telegram - Deployment Started
  run: |
    curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
      -d chat_id=${{ secrets.TELEGRAM_CHAT_ID }} \
      -d text="🚀 *Production deployment started!*" \
      -d parse_mode=Markdown

- name: Notify Telegram - Deployment Success
  if: success()
  run: |
    curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
      -d chat_id=${{ secrets.TELEGRAM_CHAT_ID }} \
      -d text="✅ *Production deployment completed successfully!*" \
      -d parse_mode=Markdown

- name: Notify Telegram - Deployment Failed
  if: failure()
  run: |
    curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
      -d chat_id=${{ secrets.TELEGRAM_CHAT_ID }} \
      -d text="❌ *Production deployment failed!*" \
      -d parse_mode=Markdown
```

### Troubleshooting: 'chat not found' Error
- **Make sure your bot is in the group.**
- **Send a message in the group as a user after adding the bot.**
- **Use the correct chat ID (starts with -100 for supergroups).**
- **Check that your bot is not blocked or restricted.**
- **Double-check your bot token and chat ID in GitHub secrets.**

If you follow these steps, you will receive real-time deployment notifications in your Telegram group!

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

## ✅ Summary

- Your system is fully cloud-native, automated, and observable.
- You have real-time anomaly detection and analytics, with a modern dashboard.
- The project is in a stable, production-ready state.

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

---

## 🟡 Upcoming Tasks

- [ ] Add alerting (Slack/email) for detected anomalies
- [ ] Add support for additional ML models and compare metrics (ROC, Precision/Recall)
- [ ] Enhance dashboard with more analytics (trend charts, pod-level drilldown)
- [ ] Integrate with GCP Pub/Sub or Logging for advanced automation
- [ ] Add simulated load generator for testing anomaly detection
- [ ] Add user authentication to dashboard (optional)
- [ ] Clean up and optimize Kubernetes manifests
- [ ] Add more documentation and usage examples

Next Steps (Optional)
Tune thresholds or model sensitivity as needed for your environment.
Add more “bad” data over time to improve the model.
Use this workflow for real incident response and root cause analysis
