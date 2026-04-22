#!/bin/bash
# =============================================================================
# VedaAide Local Deployment Script
# 适用于：Podman Desktop + Kind Extension（无 Docker，无 Registry）
# 集群名：k8s-new  |  Namespace：vedaaide-dev
# =============================================================================
set -e

IMAGE="vedaaide:latest"
CLUSTER="k8s-new"
NAMESPACE="vedaaide-dev"
DOCKERFILE="infra/docker/Dockerfile.dev"

# --- 颜色输出 ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# --- 前置检查 ---
preflight() {
  info "前置检查..."

  command -v podman >/dev/null 2>&1 || error "未找到 podman，请确认 Podman Desktop 已安装"
  command -v kubectl >/dev/null 2>&1 || error "未找到 kubectl"
  command -v kind    >/dev/null 2>&1 || error "未找到 kind"

  # 检查集群是否运行
  kubectl cluster-info --request-timeout=10s >/dev/null 2>&1 \
    || error "无法连接到 K8s 集群。请在 Podman Desktop 中确认 Kind 集群 '${CLUSTER}' 已启动"

  # 检查 namespace 是否存在
  kubectl get ns "$NAMESPACE" >/dev/null 2>&1 \
    || { warn "namespace ${NAMESPACE} 不存在，正在创建..."; kubectl create ns "$NAMESPACE"; }

  # 检查 Dockerfile 是否存在
  [[ -f "$DOCKERFILE" ]] || error "Dockerfile 不存在: $DOCKERFILE"

  info "前置检查完成 ✓"
}

# --- 构建镜像 ---
build_image() {
  info "用 Podman 构建镜像: ${IMAGE}..."
  podman build -t "$IMAGE" -f "$DOCKERFILE" . \
    || error "镜像构建失败"
  info "镜像构建完成 ✓"
}

# --- 加载镜像到 Kind ---
load_image() {
  info "加载镜像到 Kind 集群 '${CLUSTER}'..."
  kind load docker-image "$IMAGE" --name "$CLUSTER" \
    || error "加载镜像到 Kind 失败"
  info "镜像加载完成 ✓"
}

# --- 部署到 K8s ---
deploy() {
  info "部署到 namespace: ${NAMESPACE}..."

  if [[ -d "infra/k8s" ]]; then
    kubectl apply -f infra/k8s/ -n "$NAMESPACE"
  else
    warn "infra/k8s/ 目录不存在，跳过 kubectl apply"
  fi

  # 滚动重启（确保拉取最新镜像）
  kubectl rollout restart deployment/vedaaide-api -n "$NAMESPACE" 2>/dev/null || true

  info "等待 Pod 就绪..."
  kubectl rollout status deployment/vedaaide-api -n "$NAMESPACE" --timeout=60s 2>/dev/null || true
}

# --- 显示结果 ---
show_status() {
  echo ""
  info "部署完成！当前状态："
  kubectl get pods -n "$NAMESPACE"
  echo ""
  info "查看日志：kubectl logs -f -n ${NAMESPACE} svc/vedaaide-api"
  info "端口转发：kubectl port-forward -n ${NAMESPACE} svc/vedaaide-api 8080:8080"
}

# --- 主流程 ---
main() {
  echo ""
  echo "======================================================"
  echo "  VedaAide Local Deploy  |  Cluster: ${CLUSTER}"
  echo "  Namespace: ${NAMESPACE}  |  Image: ${IMAGE}"
  echo "======================================================"
  echo ""

  preflight
  build_image
  load_image
  deploy
  show_status
}

main "$@"
