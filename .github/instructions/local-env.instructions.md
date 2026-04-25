---
applyTo: "docker-compose.yml,*.yaml,*.yml"
---

# Local Development Environment

## Overview

VedaAide uses Docker Compose for local infrastructure. Kubernetes/Skaffold is NOT part of this project.

## Required Services

```bash
# Start Qdrant (required for all development)
docker compose up qdrant -d

# Verify
curl http://localhost:6333/health
```

## Optional: Full Stack (LangFuse tracing)

```bash
# Start all services (Qdrant + LangFuse + PostgreSQL + ClickHouse)
docker compose up -d

# Access LangFuse at http://localhost:3000
```

## docker-compose.yml Structure

Services defined:
- **qdrant** (port 6333) — Vector database, always needed
- **langfuse** (port 3000) — LangFuse UI, optional
- **postgres** — LangFuse backend DB, optional
- **clickhouse** — LangFuse analytics, optional

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=vedaaide
LANGFUSE_HOST=http://localhost:3000  # optional
```

## Prohibited Patterns

```bash
# ❌ Not used — project has no Kubernetes deployment
kubectl ...
skaffold ...
podman ...
kind ...
```
