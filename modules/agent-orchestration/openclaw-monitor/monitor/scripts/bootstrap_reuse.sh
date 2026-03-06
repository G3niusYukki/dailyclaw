#!/usr/bin/env bash
set -euo pipefail

# 用法:
#   bash monitor/scripts/bootstrap_reuse.sh [workspace_root]
# 默认 workspace_root 为当前目录

WORKSPACE_ROOT="${1:-$(pwd)}"
MONITOR_DIR="${WORKSPACE_ROOT}/monitor"
DATA_DIR="${MONITOR_DIR}/data"
SCRIPTS_DIR="${MONITOR_DIR}/scripts"
INSTANCE_FILE="${MONITOR_DIR}/.instance_id"
TASKS_FILE="${DATA_DIR}/tasks.json"
LEDGER_FILE="${DATA_DIR}/task_ledger.json"

mkdir -p "${DATA_DIR}" "${SCRIPTS_DIR}"

slug() {
  tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/--*/-/g; s/^-//; s/-$//'
}

if [[ -f "${INSTANCE_FILE}" ]]; then
  INSTANCE_ID="$(cat "${INSTANCE_FILE}" | tr -d '[:space:]')"
else
  ORG="${OC_ORG:-oc}"
  ENV_NAME="${OC_ENV:-prod}"
  HOST_RAW="${HOSTNAME:-$(hostname)}"
  HOST="$(printf '%s' "${HOST_RAW}" | slug)"
  SUFFIX="$(date +%s | tail -c 7)"
  INSTANCE_ID="$(printf '%s-%s-%s-%s' "${ORG}" "${ENV_NAME}" "${HOST}" "${SUFFIX}" | slug)"
  printf '%s\n' "${INSTANCE_ID}" > "${INSTANCE_FILE}"
fi

NOW_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

if [[ ! -f "${TASKS_FILE}" ]]; then
  cat > "${TASKS_FILE}" <<EOF
{
  "schema_version": "1.0",
  "instance_id": "${INSTANCE_ID}",
  "updated_at": "${NOW_UTC}",
  "tasks": []
}
EOF
fi

if [[ ! -f "${LEDGER_FILE}" ]]; then
  cat > "${LEDGER_FILE}" <<EOF
{
  "schema_version": "1.0",
  "instance_id": "${INSTANCE_ID}",
  "updated_at": "${NOW_UTC}",
  "events": []
}
EOF
fi

cat <<EOF
[bootstrap_reuse] done
workspace     : ${WORKSPACE_ROOT}
instance_id   : ${INSTANCE_ID}
tasks.json    : ${TASKS_FILE}
ledger.json   : ${LEDGER_FILE}
EOF
