#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 可通过环境变量覆盖：
# - OC_MONITOR_ROOT: OpenClaw 工作区根目录（其下应有 monitor/）
# - OPENCLAW_HOME: OpenClaw 主目录（默认 ~/.openclaw）
DEFAULT_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.getenv('OC_MONITOR_ROOT', str(DEFAULT_ROOT))).expanduser().resolve()
OPENCLAW_HOME = Path(os.getenv('OPENCLAW_HOME', '~/.openclaw')).expanduser().resolve()
CONFIG = OPENCLAW_HOME / 'openclaw.json'
AGENTS_ROOT = OPENCLAW_HOME / 'agents'
TASKS = ROOT / 'monitor/data/tasks.json'
LEDGER = ROOT / 'monitor/data/task_ledger.json'
CODE = ROOT / 'monitor/data/code_changes.json'
TEAM_CONFIG = ROOT / 'monitor/config/team.json'

TZ = timezone(timedelta(hours=8))
NOW = lambda: datetime.now(TZ)


TEST_RATIO_RE = re.compile(r'(?:pytest|test|测试)[^\n]{0,40}?(\d{1,4})\s*/\s*(\d{1,4})', re.IGNORECASE)
CHECKLIST_RATIO_RE = re.compile(r'(?:checklist|清单|todo|任务项?)[^\n]{0,40}?(\d{1,4})\s*/\s*(\d{1,4})', re.IGNORECASE)


def run_git(repo: Path, args: list[str]) -> str:
    p = subprocess.run(['git', '-C', str(repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip())
    return p.stdout


def repo_snapshot(repo_path: str) -> dict:
    repo = Path(repo_path)
    if not (repo / '.git').exists():
        return {'repo_path': repo_path, 'error': 'not a git repository', 'tracked_files_changed': 0, 'untracked_files': 0, 'files': [], 'recent_commits': [], 'line_stats': {'added': 0, 'deleted': 0}}
    porcelain = run_git(repo, ['status', '--porcelain'])
    files, tracked, untracked = [], 0, 0
    for ln in porcelain.splitlines():
        st = ln[:2]
        fp = ln[3:] if len(ln) > 3 else ''
        is_un = st == '??'
        tracked += 0 if is_un else 1
        untracked += 1 if is_un else 0
        files.append({'status': st.strip() or st, 'path': fp, 'untracked': is_un})
    try:
        commits = run_git(repo, ['log', '-n', '5', '--pretty=format:%h%x1f%an%x1f%s'])
    except Exception:
        commits = ''
    recent = []
    for ln in commits.splitlines():
        if not ln:
            continue
        h, a, s = ln.split('\x1f', 2)
        recent.append({'hash': h, 'author': a, 'subject': s})
    try:
        branch = run_git(repo, ['rev-parse', '--abbrev-ref', 'HEAD']).strip()
    except Exception:
        branch = '(unknown)'
    return {
        'repo_path': repo_path,
        'branch': branch,
        'tracked_files_changed': tracked,
        'untracked_files': untracked,
        'files': files,
        'recent_commits': recent,
        'line_stats': {'added': 0, 'deleted': 0},
    }


def load(path: Path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f'.tmp-{os.getpid()}')
    data = json.dumps(payload, ensure_ascii=False, indent=2)

    with tmp.open('w', encoding='utf-8') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

    os.replace(tmp, path)


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def read_tail_text(path: Path, max_bytes: int = 120_000) -> str:
    try:
        with path.open('rb') as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - max_bytes))
            return f.read().decode('utf-8', errors='ignore')
    except Exception:
        return ''


def extract_text_blobs_from_jsonl(raw: str) -> str:
    blobs: list[str] = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            evt = json.loads(ln)
        except Exception:
            continue
        msg = evt.get('message') or {}
        for part in msg.get('content', []) if isinstance(msg.get('content'), list) else []:
            if isinstance(part, dict):
                txt = part.get('text') or part.get('thinking') or ''
                if txt:
                    blobs.append(str(txt))
    return '\n'.join(blobs)


def _ratio_to_percent(done: int, total: int) -> int | None:
    if total <= 0 or done < 0 or done > total:
        return None
    return round(done * 100 / total)


def _unknown_progress() -> dict:
    return {
        'progress': None,
        'progress_source': 'unknown',
        'progress_confidence': 'unknown',
        'evidence_ref': None,
    }



def _evidence_ref(path: Path, metric: str, m: re.Match) -> dict:
    return {
        'type': 'session_jsonl_text_match',
        'session_file': str(path),
        'metric': metric,
        'matched_text': m.group(0),
        'value': {'done': int(m.group(1)), 'total': int(m.group(2))},
    }



def infer_progress_from_evidence(session_file: str | None) -> dict:
    if not session_file:
        return _unknown_progress()

    path = Path(session_file)
    if not path.exists():
        return _unknown_progress()

    raw_tail = read_tail_text(path)
    if not raw_tail:
        return _unknown_progress()

    corpus = extract_text_blobs_from_jsonl(raw_tail)
    if not corpus:
        return _unknown_progress()

    test_matches = list(TEST_RATIO_RE.finditer(corpus))
    if test_matches:
        m = test_matches[-1]
        pct = _ratio_to_percent(int(m.group(1)), int(m.group(2)))
        if pct is not None:
            return {
                'progress': pct,
                'progress_source': 'test_pass_rate',
                'progress_confidence': 'high',
                'evidence_ref': _evidence_ref(path, 'test_ratio', m),
            }

    checklist_matches = list(CHECKLIST_RATIO_RE.finditer(corpus))
    if checklist_matches:
        m = checklist_matches[-1]
        pct = _ratio_to_percent(int(m.group(1)), int(m.group(2)))
        if pct is not None:
            return {
                'progress': pct,
                'progress_source': 'checklist_completion',
                'progress_confidence': 'medium',
                'evidence_ref': _evidence_ref(path, 'checklist_ratio', m),
            }

    return _unknown_progress()


def latest_active_from_main(max_age_sec: int = 900) -> set[str]:
    """Best-effort: read latest `subagents list` tool result from main session history.
    This fixes false-IDLE when lock files are absent for run-mode subagents.
    """
    base = AGENTS_ROOT / 'main' / 'sessions'
    jsonls = sorted(base.glob('*.jsonl'), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    if not jsonls:
        return set()

    text = read_tail_text(jsonls[0], max_bytes=400_000)
    if not text:
        return set()

    now_ms = int(time.time() * 1000)
    for ln in reversed(text.splitlines()):
        ln = ln.strip()
        if not ln:
            continue
        try:
            evt = json.loads(ln)
        except Exception:
            continue
        msg = evt.get('message') or {}
        if msg.get('role') != 'toolResult':
            continue
        if msg.get('toolName') != 'subagents':
            continue
        details = msg.get('details') or {}
        if details.get('action') != 'list':
            continue
        ts = int(msg.get('timestamp') or 0)
        if ts and (now_ms - ts) > max_age_sec * 1000:
            return set()
        active = details.get('active') or []
        ids = set()
        for it in active:
            sk = str((it or {}).get('sessionKey') or '')
            parts = sk.split(':')
            if len(parts) >= 2 and parts[0] == 'agent':
                ids.add(parts[1])
        return ids
    return set()


def agent_runtime(agent_id: str, active_hint: set[str] | None = None) -> dict:
    base = AGENTS_ROOT / agent_id / 'sessions'
    active = False
    newest_ts = 0
    newest_label = '无会话'
    newest_session_file: str | None = None

    for lf in base.glob('*.jsonl.lock'):
        j = load(lf, {})
        pid = int(j.get('pid', 0) or 0)
        if pid and pid_alive(pid):
            active = True

    if not active and active_hint and agent_id in active_hint:
        active = True

    sess = load(base / 'sessions.json', {})
    for _, meta in sess.items():
        upd = int(meta.get('updatedAt', 0) or 0)
        if upd > newest_ts:
            newest_ts = upd
            newest_label = meta.get('label') or meta.get('displayName') or '实时会话'
            newest_session_file = meta.get('sessionFile')

    return {'active': active, 'updatedAt': newest_ts, 'label': newest_label, 'sessionFile': newest_session_file}


def load_team_members() -> list[dict]:
    """优先读取 monitor/config/team.json；若缺失则回退到 openclaw.json agents 列表。"""
    team = load(TEAM_CONFIG, {})
    members = team.get('members') if isinstance(team, dict) else None
    out: list[dict] = []

    if isinstance(members, list) and members:
        for m in members:
            if not isinstance(m, dict):
                continue
            aid = str(m.get('agent_id') or '').strip()
            if not aid:
                continue
            out.append({
                'agent_id': aid,
                'owner_cn': str(m.get('owner_cn') or aid),
                'duty': str(m.get('duty') or '未定义职责'),
                'repo_path': str(m.get('repo_path') or ROOT),
            })
        if out:
            return out

    cfg = load(CONFIG, {})
    for a in cfg.get('agents', {}).get('list', []):
        aid = str(a.get('id') or '').strip()
        if not aid:
            continue
        out.append({
            'agent_id': aid,
            'owner_cn': str(a.get('identity', {}).get('name') or aid),
            'duty': '未定义职责',
            'repo_path': str(a.get('workspace') or ROOT),
        })
    return out


def build_realtime_tasks() -> list[dict]:
    now = NOW()
    now_iso = now.isoformat(timespec='seconds')
    members = load_team_members()
    active_hint = latest_active_from_main()

    tasks = []
    for m in members:
        aid = m['agent_id']
        name = m['owner_cn']
        duty = m['duty']
        workspace = m['repo_path']

        rt = agent_runtime(aid, active_hint)
        upd = int(rt.get('updatedAt', 0) or 0)
        dt = datetime.fromtimestamp(upd / 1000, tz=TZ).isoformat(timespec='seconds') if upd else now_iso
        status = 'DOING' if rt.get('active') else 'IDLE'
        age_s = max(0, int(now.timestamp() * 1000 - upd) // 1000) if upd else 0
        title = rt.get('label', '实时会话')
        progress_meta = infer_progress_from_evidence(rt.get('sessionFile'))

        tasks.append({
            'task_id': f'LIVE-{aid}',
            'agent_id': aid,
            'title': title,
            'owner': name,
            'owner_cn': name,
            'duty': duty,
            'repo_path': workspace,
            'status': status,
            'goal': f'live-lock={status} | age={age_s}s',
            'progress': progress_meta['progress'],
            'progress_source': progress_meta['progress_source'],
            'progress_confidence': progress_meta['progress_confidence'],
            'evidence_ref': progress_meta['evidence_ref'],
            'task_content': title,
            'blockers': '无',
            'eta': '实时',
            'acceptance_criteria': ['实时源=lock(pid alive)+sessions.json'],
            'last_status_change': dt,
        })

    return tasks


def _normalize_status(v: str | None) -> str:
    allowed = {'TODO', 'DOING', 'DONE', 'BLOCKED', 'IDLE'}
    s = str(v or '').upper().strip()
    return s if s in allowed else 'TODO'


def load_ledger_tasks() -> list[dict]:
    data = load(LEDGER, {})
    if not isinstance(data, dict):
        return []

    rows = data.get('tasks') if isinstance(data.get('tasks'), list) else []
    out: list[dict] = []
    now_iso = NOW().isoformat(timespec='seconds')

    for row in rows:
        if not isinstance(row, dict):
            continue
        task_id = str(row.get('task_id') or '').strip()
        agent_id = str(row.get('agent_id') or '').strip()
        if not task_id or not agent_id:
            continue

        owner_cn = str(row.get('owner_cn') or '').strip() or agent_id
        duty = str(row.get('duty') or '').strip() or '未标注'
        status = _normalize_status(row.get('status'))
        task_content = str(row.get('task_content') or '').strip() or task_id
        eta = str(row.get('eta') or '').strip() or '-'
        blockers = str(row.get('blockers') or '').strip() or '无'
        repo_path = str(row.get('repo_path') or '').strip() or ROOT.as_posix()

        out.append({
            'task_id': task_id,
            'agent_id': agent_id,
            'title': task_content,
            'owner': owner_cn,
            'owner_cn': owner_cn,
            'duty': duty,
            'repo_path': repo_path,
            'status': status,
            'goal': row.get('goal') or '-',
            'progress': row.get('progress'),
            'progress_source': row.get('progress_source') or 'unknown',
            'progress_confidence': row.get('progress_confidence') or 'unknown',
            'evidence_ref': row.get('evidence_ref'),
            'task_content': task_content,
            'blockers': blockers,
            'eta': eta,
            'acceptance_criteria': row.get('acceptance_criteria') or [],
            'last_status_change': row.get('last_status_change') or row.get('updated_at') or now_iso,
        })

    return out


def merge_tasks(realtime_tasks: list[dict], ledger_tasks: list[dict]) -> list[dict]:
    # 同时保留：
    # - ledger 业务任务（计划层）
    # - LIVE-* 在线态任务（执行层）
    # 这样可稳定展示“多 Agent 同时工作”的全貌。
    return [*ledger_tasks, *realtime_tasks] if ledger_tasks else realtime_tasks


def main():
    realtime_tasks = build_realtime_tasks()
    ledger_tasks = load_ledger_tasks()
    tasks = merge_tasks(realtime_tasks, ledger_tasks)

    atomic_write_json(TASKS, {
        'generated_at': NOW().isoformat(timespec='seconds'),
        'source': 'realtime lock+sessions + task_ledger',
        'tasks': tasks,
    })

    repos = sorted({t.get('repo_path') for t in tasks if t.get('repo_path')})
    snaps = {}
    for rp in repos:
        snaps[rp] = repo_snapshot(rp)
    atomic_write_json(CODE, {'generated_at': NOW().isoformat(timespec='seconds'), 'task_count': len(tasks), 'repo_count': len(snaps), 'snapshots': snaps})
    print('Updated realtime tasks/code snapshots')


if __name__ == '__main__':
    main()
