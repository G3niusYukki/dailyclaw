#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 可通过环境变量覆盖：
# - OC_MONITOR_ROOT: OpenClaw 工作区根目录（其下应有 monitor/）
DEFAULT_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.getenv('OC_MONITOR_ROOT', str(DEFAULT_ROOT))).expanduser().resolve()
LEDGER = ROOT / 'monitor/data/task_ledger.json'
REFRESH = ROOT / 'monitor/scripts/refresh_status.py'
TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec='seconds')


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f'.tmp-{os.getpid()}')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='新增或更新任务台账记录（支持 main 主会话任务登记）')
    p.add_argument('--task-id', required=True)
    p.add_argument('--agent-id', required=True)
    p.add_argument('--owner-cn', required=True)
    p.add_argument('--duty', required=True)
    p.add_argument('--status', required=True, choices=['TODO', 'DOING', 'DONE', 'BLOCKED', 'IDLE'])
    p.add_argument('--task-content', required=True)
    p.add_argument('--eta', default='-')
    p.add_argument('--blockers', default='无')
    p.add_argument('--repo-path', default=str(ROOT))
    p.add_argument('--refresh', action='store_true', help='写入后立即刷新 tasks.json/code_changes.json')
    return p.parse_args()


def upsert_task(args: argparse.Namespace) -> dict:
    data = load_json(LEDGER, {'generated_at': now_iso(), 'source': 'task_upsert', 'tasks': []})
    tasks = data.get('tasks') if isinstance(data.get('tasks'), list) else []

    row = {
        'task_id': args.task_id,
        'agent_id': args.agent_id,
        'owner_cn': args.owner_cn,
        'duty': args.duty,
        'status': args.status,
        'task_content': args.task_content,
        'eta': args.eta,
        'blockers': args.blockers,
        'repo_path': args.repo_path,
        'updated_at': now_iso(),
    }

    replaced = False
    for i, t in enumerate(tasks):
        if isinstance(t, dict) and str(t.get('task_id')) == args.task_id:
            tasks[i] = {**t, **row}
            replaced = True
            break

    if not replaced:
        tasks.append(row)

    data['generated_at'] = now_iso()
    data['source'] = 'task_upsert'
    data['tasks'] = tasks
    atomic_write_json(LEDGER, data)
    return row


def main() -> None:
    args = parse_args()
    row = upsert_task(args)
    print(json.dumps({'ok': True, 'task': row, 'ledger': str(LEDGER)}, ensure_ascii=False))

    if args.refresh:
        subprocess.run(['python3', str(REFRESH)], check=False)


if __name__ == '__main__':
    main()
