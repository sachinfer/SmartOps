from kubernetes import client, config

def get_pod_restart_counts(namespace="smartops"):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    restarts = {}
    pods = v1.list_namespaced_pod(namespace=namespace)
    for pod in pods.items:
        for c in pod.status.container_statuses:
            if c.restart_count > 2:
                restarts[pod.metadata.name] = c.restart_count
    return restarts 