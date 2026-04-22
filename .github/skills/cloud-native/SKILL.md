---
name: cloud-native
description: Guide for cloud-native development using Skaffold, Kubernetes, Podman, and Kind for VedaAide local development and deployment
applyTo: "infra/**,scripts/**,skaffold.yaml,docker-compose.yml,*.yaml,*.yml"
keywords:
  - docker
  - kubernetes
  - skaffold
  - deployment
  - k8s
  - container
  - helm
  - manifest
  - podman
  - kind
  - 容器
  - 云原生
  - 部署
  - K8s
  - 镜像
  - Skaffold
  - Dockerfile
  - 配置管理
whenToUse: |
  When working on:
  - Skaffold development workflows
  - Kubernetes deployment configurations
  - Docker/Podman image building
  - Local development with Kind clusters
  - Infrastructure as Code (IaC)
---

# Cloud Native Development Guide

> **Purpose**: Reference manual for Skaffold workflows, Dockerfile templates, and K8s configuration.
>
> **Local environment constraints** (Podman instead of Docker, `kind load` instead of push, `imagePullPolicy: Never`, etc.)
> are defined in `.github/instructions/local-env.instructions.md` and apply automatically to all infra/scripts files.

---

## Introduction to Skaffold

Skaffold is an open-source cloud-native development tool by Google that automates code compilation, image building, and deployment workflows.

**Key benefits**:
- 🔄 Automatic code sync to containers (hot reload)
- 🏗️ Automatic image build and push
- 📦 Kubernetes deployment automation
- 🔍 Log streaming and port forwarding
- ⚡ Fast feedback loop

## Development Workflow Comparison

### Traditional Approach (Slow)
```
Edit code
  ↓
Manual build: docker build -t image:tag .
  ↓
Manual push: docker push image:tag
  ↓
Manual deploy: kubectl set image deployment/app app=image:tag
  ↓
View logs: kubectl logs -f pod/...
  ↓
Total time: 3-5 minutes ❌
```

### Skaffold Approach (Efficient)
```
Edit code
  ↓
Skaffold automatically:
  - Syncs code to container
  - Restarts application
  - Forwards ports and streams logs
  ↓
Total time: 1-2 seconds ✅
```

## Skaffold Configuration

### skaffold.yaml Breakdown

```yaml
apiVersion: skaffold/v4beta6
kind: Config
metadata:
  name: vedaaide

# Build configuration
build:
  artifacts:
    - image: vedaaide-api
      docker:
        dockerfile: infra/docker/Dockerfile.dev
        target: development  # multi-stage build target
    - image: vedaaide-worker
      docker:
        dockerfile: infra/docker/Dockerfile.worker

# Deploy configuration
deploy:
  kubectl: {}

# Port forwarding
portForward:
  - resourceType: deployment
    resourceName: vedaaide-api
    port: 8080        # container port
    localPort: 8080   # local port

# Code sync (hot reload)
sync:
  manual:
    - src: "src/**/*.py"      # source file pattern
      dest: /app/src          # destination path in container
    - src: "config/**/*.yaml"
      dest: /app/config

# Dev mode
dev:
  watch:
    - infra/docker/Dockerfile.dev  # watch for Dockerfile changes
    - src/**/*.py
    - config/**/*.yaml
```

## Development Workflow

### 1. Initialization

```bash
# Local machine uses Podman, targeting the Kind cluster
export KIND_CLUSTER_NAME=k8s-new

# Confirm cluster and namespace are ready
kubectl cluster-info
kubectl get ns vedaaide-dev  # should exist

# Start Skaffold dev mode (uses kind load, no Registry needed)
skaffold dev --port-forward --namespace vedaaide-dev

# Or use debug mode (supports breakpoints)
skaffold debug --port-forward --namespace vedaaide-dev
```

### 2. Development and Testing

Edit a Python file:
```python
# src/core/agent/tools.py
def calculate_similarity(query: str, doc: str) -> float:
    # modify code
    return new_similarity
```

Skaffold automatically:
- ✅ Detects file changes
- ✅ Syncs to `/app/src/` in the container
- ✅ Restarts the application (or hot-reloads)
- ✅ Streams logs to terminal

### 3. Fast Feedback

```bash
# View live logs
skaffold logs -f

# Access the application
curl http://localhost:8080/api/health

# View errors (if any)
# Skaffold automatically displays container logs
```

### 4. Debugging

Set breakpoints in VSCode, then:
```bash
# Start in debug mode
skaffold debug --port-forward

# VSCode will automatically connect to the debug port
# Set breakpoints and execute code to start debugging
```

## Local Kubernetes Cluster Setup

### Local Setup: Podman Desktop + Kind Extension

> The local cluster is managed via Podman Desktop's Kind Extension, with cluster name `k8s-new`.

```bash
# Verify cluster status
kubectl cluster-info
kubectl get nodes
# Expected: k8s-new-control-plane   Ready

# Verify vedaaide-dev namespace
kubectl get ns vedaaide-dev
```

### Loading Images into Kind (Replacing Registry)

No Docker Registry is used locally; images are loaded directly with `kind load docker-image`:

```bash
# 1. Build image with Podman
podman build -t vedaaide:latest -f infra/docker/Dockerfile.dev .

# 2. Load into Kind cluster (critical step)
kind load docker-image vedaaide:latest --name k8s-new

# 3. Verify image is loaded
podman exec k8s-new-control-plane crictl images | grep vedaaide

# 4. Deploy (must use imagePullPolicy: Never)
kubectl apply -f infra/k8s/deployment.yaml -n vedaaide-dev
```

> **Critical**: `imagePullPolicy: Never` must be set in the deployment manifest,
> otherwise K8s will attempt to pull from the internet and fail.

```yaml
# Key configuration in infra/k8s/deployment.yaml
spec:
  containers:
  - name: vedaaide-api
    image: vedaaide:latest
    imagePullPolicy: Never  # ← must be set
```

### Full Workflow Script

```bash
# scripts/k8s/deploy-local.sh
#!/bin/bash
set -e

IMAGE="vedaaide:latest"
CLUSTER="k8s-new"
NAMESPACE="vedaaide-dev"

echo "1. Building image..."
podman build -t $IMAGE -f infra/docker/Dockerfile.dev .

echo "2. Loading into Kind cluster..."
kind load docker-image $IMAGE --name $CLUSTER

echo "3. Deploying to $NAMESPACE..."
kubectl apply -f infra/k8s/ -n $NAMESPACE
kubectl rollout restart deployment/vedaaide-api -n $NAMESPACE

echo "4. Waiting for readiness..."
kubectl rollout status deployment/vedaaide-api -n $NAMESPACE

echo "✓ Deployment complete"
kubectl get pods -n $NAMESPACE
```

## Dockerfile Multi-Stage Build

### Dockerfile.dev (Development Image)

```dockerfile
FROM python:3.10-slim AS development

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root

# Copy source code
COPY src ./src
COPY config ./config

# Expose port
EXPOSE 8080

# Start application (with hot reload support)
CMD ["poetry", "run", "python", "-m", "src.main"]
```

### Dockerfile (Production Image)

```dockerfile
FROM python:3.10-slim AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-directory

FROM python:3.10-slim AS production

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /root/.cache /root/.cache

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-directory

# Copy application code
COPY src ./src
COPY config ./config

# Non-root user
RUN useradd -m -u 1000 vedaaide
USER vedaaide

EXPOSE 8080

CMD ["poetry", "run", "python", "-m", "src.main"]
```

## Performance Considerations

### Sync Latency

| Scenario | Latency | Notes |
|------|------|------|
| Small file change | 1-2s | Python file edit, auto sync |
| Large file change | 2-3s | Large data files may be slower |
