---
applyTo: "infra/**,scripts/**,skaffold.yaml,docker-compose.yml,*.yaml,*.yml"
---

# Local Development Environment Constraints (Mandatory)

## Environment Facts

Local machine **does not have Docker installed**, uses **Podman Desktop** (with built-in Kind Extension).

| Component | Actual Configuration |
|------|----------|
| Container Runtime | **Podman** (not Docker) |
| Local K8s Cluster | Kind Extension, cluster name: `k8s-new` / `kind-k8s-new` |
| Image Registry | **None**, use `kind load docker-image` instead of push |
| Working Namespace | `vedaaide-dev` |

## Prohibited Patterns

When generating any infra/script code, **prohibit** using these patterns:

```bash
# ❌ Prohibited — Local machine has no Docker
docker build ...
docker push ...
docker run ...

# ❌ Prohibited — Local machine has no Registry
kubectl set image .../app=localhost:5000/...
```

## Correct Patterns

```bash
# ✅ Build image
podman build -t <image>:<tag> -f <dockerfile> .

# ✅ Load to Kind (instead of push)
kind load docker-image <image>:<tag> --name k8s-new

# ✅ Verify loaded
podman exec k8s-new-control-plane crictl images | grep <image>

# ✅ Deploy
kubectl apply -f infra/k8s/ -n vedaaide-dev
```

## K8s Manifest Mandatory Configuration

All containers in Deployment manifests must set:

```yaml
imagePullPolicy: Never  # Mandatory — otherwise K8s will attempt to pull from public network
```

## TLS Timeout Handling

After Podman Machine starts, `kubectl` might encounter TLS handshake timeout—this is normal. Wait 1-2 minutes and retry. **Do not** use `sleep` in scripts to bypass this; let users manually retry.

## Skaffold Configuration Key Points

When using Skaffold, the builder must be configured as `local` and push disabled:

```yaml
build:
  local:
    push: false  # Use kind load instead of push
```
