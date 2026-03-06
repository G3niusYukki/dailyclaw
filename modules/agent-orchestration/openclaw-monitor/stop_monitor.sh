#!/usr/bin/env bash
set -euo pipefail

PORT="${MONITOR_PORT:-8793}"
PIDS="$(lsof -tiTCP:${PORT} -sTCP:LISTEN || true)"

if [[ -z "${PIDS}" ]]; then
  echo "[monitor] no process listening on :${PORT}"
  exit 0
fi

echo "[monitor] stopping process(es) on :${PORT}: ${PIDS}"
kill ${PIDS}
sleep 0.5

LEFT="$(lsof -tiTCP:${PORT} -sTCP:LISTEN || true)"
if [[ -n "${LEFT}" ]]; then
  echo "[monitor] force killing: ${LEFT}"
  kill -9 ${LEFT} || true
fi

echo "[monitor] stopped"
