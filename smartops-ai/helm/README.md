# SmartOps Helm Chart

This Helm chart makes it easy to deploy SmartOps (AI-Driven DevOps Automation & Monitoring Platform) to any Kubernetes cluster.

## Usage

1. **Package or fetch the chart:**
   - If local: `cd smartops-ai/helm`
   - If remote: `helm repo add ...`

2. **Install the chart:**
   ```sh
   helm install smartops ./smartops-ai/helm \
     --set image.repository=your-docker-repo/smartops \
     --set image.tag=latest \
     --set telegram.botToken=YOUR_BOT_TOKEN \
     --set telegram.chatId=YOUR_CHAT_ID
   ```

3. **Access the dashboard:**
   - The dashboard will be exposed via LoadBalancer (default) or your chosen service type.
   - Get the external IP:
     ```sh
     kubectl get svc smartops
     ```

4. **Customize:**
   - Edit `values.yaml` or use `--set` to override image, resources, service type, etc.

## Notes
- This chart is a starting point. You may want to add PVCs, RBAC, or additional templates for a full production deployment.
- For more details, see the main SmartOps README. 