#!/usr/bin/env bash
set -euo pipefail

# 一键启动（默认以当前脚本所在目录作为 workspace 根目录）
ROOT="$(cd "$(dirname "$0")" && pwd)"
export OC_MONITOR_ROOT="${OC_MONITOR_ROOT:-$ROOT}"
export MONITOR_PORT="${MONITOR_PORT:-8793}"

cd "$OC_MONITOR_ROOT"
python3 ./monitor/scripts/refresh_status.py

echo "[monitor] root=$OC_MONITOR_ROOT"
echo "[monitor] url=http://127.0.0.1:${MONITOR_PORT}/monitor/agents-dashboard.html"
python3 ./monitor/server.py
