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
- Dashboard visualizes live and historical anomaly data from MongoDB.
- RBAC and service accounts are configured for secure metrics access.
- All dependencies are now correctly included in Docker images.
- Pods are healthy after the last dependency fix.

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
