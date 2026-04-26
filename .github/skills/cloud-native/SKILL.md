# Cloud-Native Skill — DEPRECATED

> **Status**: This skill is deprecated. VedaAide no longer uses Kubernetes, Skaffold, or Podman.

## Current Infrastructure

VedaAide uses **Docker Compose only** for local development:

```bash
# Start Qdrant (required)
docker compose up qdrant -d

# Start full stack with LangFuse (optional)
docker compose up -d
```

## Distribution

The project is distributed as a PyPI package, not a container:

```bash
pip install vedaaide
```

## For Infrastructure Questions

Refer to [local-env.instructions.md](../../instructions/local-env.instructions.md).
