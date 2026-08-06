---
title: "Parallel AI Agents on a Shared Checkout — The Lease Contract You Need"
date: 2026-08-06T07:00:00+07:00
draft: false
topics: ["ai-agents"]
tags: ["parallel-agents", "git-worktree", "lease-contract", "agent-ops", "concurrency"]
cover: /covers/parallel-agents-shared-checkout-lease.png
description: "Running multiple coding agents on one Git working tree without a lease contract is a merge race, not parallelism. Here's the isolation and ownership pattern that prevents silent corruption."
seo:
  primaryQuery: "parallel ai agents git worktree isolation"
  secondaryQueries: ["git worktree lease contract", "coding agent concurrency control", "agent edit contract ownership"]
---

Two agents. One checkout. No lease. The merge race starts the moment the second agent writes.

Your team adopts Claude Code for the backend, Codex for the frontend, and a Hermes subagent for the migration script. They all target `main`. The first agent creates a feature branch, stages changes, commits. The second agent, unaware, checks out the same branch, stages its own changes, commits. The third agent runs a rebase. The result: orphan commits, staging pollution, a force-push that rewrites history, and three hours of forensic git archaeology to recover what was lost. This is not a hypothetical. GeekNews has documented parallel agent failure patterns including branch hijacking, orphan commits, staging pollution, and double implementation [Source: https://news.hada.io/topic?id=26120].

![Staging pollution: one commit, two agents, zero intent](/img/parallel-agents-shared-checkout-lease-1.png)

The question is not whether this demos well; it is whether it survives maintenance, handoff, and local constraints. In the Modoo Laravel SaaS projects we maintain across Jakarta and Ho Chi Minh City, parallel agent runs without isolation have caused more silent data loss than any deployment rollback. The pattern repeats: teams treat "run agents in parallel" as a speed button. It is a migration contract — isolation, ownership, and a named integration gate.

![Parallel agents on shared checkout — merge race illustration](/img/parallel-agents-shared-checkout-lease-1.png)

## The Anatomy of a Shared-Checkout Merge Race

A shared-checkout merge race occurs when two or more autonomous coding agents operate on the same Git working tree without explicit coordination. Unlike traditional parallel development where humans communicate via PRs and Slack, agents operate at machine speed with no implicit coordination protocol.

GeekNews identifies four primary failure modes [Source: https://news.hada.io/topic?id=26120]:

| Failure Mode | Mechanism | Detection Difficulty |
|--------------|-----------|---------------------|
| **Branch hijacking** | Agent B force-moves the branch tip while Agent A is still writing | Low (visible in reflog) |
| **Orphan commits** | Agent A commits; Agent B resets hard; Agent A's commits become unreachable | Medium (requires `git reflog`) |
| **Staging pollution** | Agent A stages files; Agent B stages different files; `git commit` captures both | High (silent, looks intentional) |
| **Double implementation** | Both agents implement the same feature independently in different files | Very high (discovered at PR review) |

The critical insight: **staging pollution is the most dangerous** because it produces a single commit that looks correct but contains changes from two unrelated agents. No test fails. No conflict marker appears. The corruption ships.

{{< note type="warning" title="Parallel ≠ Concurrent" >}}
Running three agents simultaneously on one checkout is not parallelism. It is a data race with a commit hash as the shared mutable state. True parallelism requires isolation boundaries — separate worktrees, explicit leases, and a deterministic integration gate.
{{< /note>}}

## Why Git Worktree Is the Isolation Primitive

Git's `worktree` command (stable since Git 2.5, 2015) creates additional working directories linked to the same repository. Each worktree has its own checked-out branch, index, and HEAD — but shares the object database. This is exactly the isolation boundary parallel agents need.

```bash
# Main repo at /home/developer/project
cd /home/developer/project

# Create isolated worktree for Agent A (backend)
git worktree add ../project-agent-a feature/agent-a-backend-api
# Creates /home/developer/project-agent-a with feature/agent-a-backend-api checked out

# Create isolated worktree for Agent B (frontend)
git worktree add ../project-agent-b feature/agent-b-frontend-ui
# Creates /home/developer/project-agent-b with feature/agent-b-frontend-ui checked out

# Create isolated worktree for Agent C (migration)
git worktree add ../project-agent-c feature/agent-c-migration
# Creates /home/developer/project-agent-c with feature/agent-c-migration checked out

# List all worktrees
git worktree list
```

![Git worktree isolation — separate index, separate HEAD, shared object DB](/img/parallel-agents-shared-checkout-lease-2.png)

Each agent now operates in its own directory with its own branch. No staging pollution. No branch hijacking. No orphan commits from a sibling's `reset --hard`.

![Git worktree isolation architecture](/img/parallel-agents-shared-checkout-lease-2.png)

### Worktree Lifecycle Management

Worktrees are lightweight but not free. Each consumes disk space for the working tree (not the `.git` objects). Cleanup is essential.

```bash
# /opt/agents/cleanup-worktrees.sh
#!/usr/bin/env bash
# Runs daily via systemd timer. Removes worktrees for merged/deleted branches.

set -euo pipefail

REPO_ROOT="/home/developer/project"
MAX_AGE_DAYS=7

cd "$REPO_ROOT"

# Prune dead worktree administrative files
git worktree prune

# Remove worktrees for branches that have been merged to main
for wt in $(git worktree list --porcelain | grep '^worktree ' | cut -d' ' -f2); do
    branch=$(git -C "$wt" branch --show-current 2>/dev/null || echo "")
    [[ -z "$branch" ]] && continue
    
    # Skip main branch worktree
    [[ "$branch" == "main" ]] && continue
    
    # Check if branch is merged to main
    if git merge-base --is-ancestor "$branch" main 2>/dev/null; then
        echo "Removing merged worktree: $wt (branch: $branch)"
        git worktree remove "$wt" --force
        continue
    fi
    
    # Check age of last commit on branch
    last_commit_date=$(git -C "$wt" log -1 --format=%ct "$branch" 2>/dev/null || echo 0)
    if [[ $last_commit_date -gt 0 ]]; then
        age_days=$(( ($(date +%s) - last_commit_date) / 86400 ))
        if (( age_days > MAX_AGE_DAYS )); then
            echo "Removing stale worktree: $wt (branch: $branch, age: ${age_days}d)"
            git worktree remove "$wt" --force
        fi
    fi
done
```

## The Lease Contract: Ownership Before Access

Isolation via worktrees solves the structural problem. But you still need a coordination protocol: **who owns what, for how long, and what happens when the lease expires**.

Digital Thought Disruption's control plane series describes the pattern: designing a safe AI agent execution runtime with idempotency, isolation, post-condition verification, compensation, rollback, and evidence controls [Source: https://digitalthoughtdisruption.com/2026/07/25/execute-verify-rollback-agent-actions/]. The lease contract is the isolation + ownership layer.

```yaml
# /etc/agent-leases/agent-a-backend.yaml
# Lease contract for Agent A (backend API work)
agent:
  id: "claude-code-backend"
  role: "backend-api"
  capabilities: ["php", "laravel", "sql", "redis"]
  
lease:
  resource: "git-worktree"
  path: "/home/developer/project-agent-a"
  branch: "feature/agent-a-backend-api"
  max_duration_hours: 4
  heartbeat_interval_seconds: 60
  
ownership:
  primary:
    name: "Platform Team"
    slack: "#platform-oncall"
    phone: "+62-812-XXXX-XXXX"
  escalation:
    - after_minutes: 30
      action: "alert_owner_slack"
    - after_minutes: 60
      action: "page_oncall"
    - after_minutes: 120
      action: "revoke_lease_and_cleanup"
      
proof:
  type: "composite"
  heartbeat_file: "/var/lib/agent-leases/agent-a-backend.json"
  verification_probe: "/opt/agents/verify_agent_a.py"
  max_age_hours: 5
  
integration_gate:
  required_reviews: 1
  required_checks: ["phpstan", "pest", "lint"]
  auto_merge: false
  merge_strategy: "squash"
```

The lease contract says: *Agent A owns this worktree for up to 4 hours. It must heartbeat every 60 seconds. If the heartbeat stops, the lease is revoked and the worktree cleaned up. Integration requires human review and passing checks.*

![Lease lifecycle: request → heartbeat → verify → integrate → cleanup](/img/parallel-agents-shared-checkout-lease-3.png)

### Heartbeat Implementation

```python
# /opt/agents/lease_heartbeat.py
#!/usr/bin/env python3
"""
Lease heartbeat writer. Called by the agent wrapper every 60 seconds.
Writes a machine-readable heartbeat file with agent status.
"""
import json
import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone

LEASE_DIR = Path("/var/lib/agent-leases")
LEASE_DIR.mkdir(parents=True, exist_ok=True)

def write_heartbeat(agent_id: str, worktree_path: str, branch: str, status: str, details: dict = None) -> None:
    heartbeat = {
        "agent_id": agent_id,
        "worktree_path": worktree_path,
        "branch": branch,
        "status": status,  # "running", "completed", "failed", "revoked"
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pid": os.getpid(),
        "hostname": os.uname().nodename,
        "details": details or {}
    }
    
    heartbeat_file = LEASE_DIR / f"{agent_id}.json"
    heartbeat_file.write_text(json.dumps(heartbeat, indent=2))
    
    # Also write simple timestamp for dead-man's-switch checks
    timestamp_file = LEASE_DIR / f"{agent_id}.last_heartbeat"
    timestamp_file.write_text(str(int(time.time())))

def check_lease_expiry(agent_id: str, max_age_seconds: int) -> bool:
    """Returns True if lease is expired (no heartbeat within max_age)."""
    timestamp_file = LEASE_DIR / f"{agent_id}.last_heartbeat"
    if not timestamp_file.exists():
        return True
    last_heartbeat = int(timestamp_file.read_text().strip())
    return (time.time() - last_heartbeat) > max_age_seconds

if __name__ == "__main__":
    # Example: python lease_heartbeat.py claude-code-backend /home/dev/project-agent-a feature/agent-a-backend-api running
    if len(sys.argv) < 5:
        print("Usage: lease_heartbeat.py <agent_id> <worktree_path> <branch> <status> [details_json]")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    worktree_path = sys.argv[2]
    branch = sys.argv[3]
    status = sys.argv[4]
    details = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}
    
    write_heartbeat(agent_id, worktree_path, branch, status, details)
```

## Post-Condition Verification: Trust But Verify

TianPan's decision provenance work makes this explicit: "When autonomous agents take consequential actions, having logs is not the same as having accountability." The article provides a practical guide to designing decision provenance for production agentic systems — covering event schemas, ownership handoffs, hallucination attribution, and compliance requirements [Source: https://tianpan.co/blog/2026-04-19-decision-provenance-agentic-systems].

The lease contract defines *who owns what*. The verification probe defines *what proves the work happened*.

```python
# /opt/agents/verify_agent_a.py
#!/usr/bin/env python3
"""
Verification probe for Agent A (backend API).
Runs AFTER the agent claims completion. Queries actual side effects.
"""
import os
import json
import subprocess
from pathlib import Path

WORKTREE_PATH = "/home/developer/project-agent-a"
BRANCH = "feature/agent-a-backend-api"
EXPECTED_FILES = [
    "app/Http/Controllers/Api/V1/UserController.php",
    "app/Services/UserService.php",
    "tests/Feature/Api/UserApiTest.php"
]
MIN_TEST_COVERAGE = 80

def check_files_exist() -> dict:
    missing = []
    for f in EXPECTED_FILES:
        if not Path(WORKTREE_PATH, f).exists():
            missing.append(f)
    return {
        "ok": len(missing) == 0,
        "missing_files": missing
    }

def check_tests_pass() -> dict:
    result = subprocess.run(
        ["./vendor/bin/pest", "--coverage", "--min=80"],
        cwd=WORKTREE_PATH,
        capture_output=True,
        text=True,
        timeout=300
    )
    return {
        "ok": result.returncode == 0,
        "output": result.stdout[-2000:] if result.stdout else "",
        "error": result.stderr[-2000:] if result.stderr else ""
    }

def check_static_analysis() -> dict:
    result = subprocess.run(
        ["./vendor/bin/phpstan", "analyse", "--level=5"],
        cwd=WORKTREE_PATH,
        capture_output=True,
        text=True,
        timeout=180
    )
    return {
        "ok": result.returncode == 0,
        "output": result.stdout[-2000:] if result.stdout else ""
    }

def check_git_status() -> dict:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=WORKTREE_PATH,
        capture_output=True,
        text=True
    )
    # Should be clean (all changes committed)
    return {
        "ok": result.stdout.strip() == "",
        "uncommitted_changes": result.stdout.strip().split('\n') if result.stdout.strip() else []
    }

if __name__ == "__main__":
    results = {
        "files": check_files_exist(),
        "tests": check_tests_pass(),
        "static_analysis": check_static_analysis(),
        "git_status": check_git_status()
    }
    
    overall_ok = all(r["ok"] for r in results.values())
    results["overall"] = overall_ok
    
    print(json.dumps(results, indent=2))
    sys.exit(0 if overall_ok else 1)
```

This probe runs independently of the agent. It doesn't trust the agent's self-report. It queries the *effect* — files created, tests passing, static analysis clean, git status clean.

![Post-condition verification: trust the effect, not the agent](/img/parallel-agents-shared-checkout-lease-4.png)

![Lease contract flow: heartbeat → verification → integration gate](/img/parallel-agents-shared-checkout-lease-3.png)

## Integration Gate: The Human-in-the-Loop Merge

The final stage is the integration gate. Digital Thought Disruption's control plane emphasizes: "execute, verify, rollback" [Source: https://digitalthoughtdisruption.com/2026/07/25/execute-verify-rollback-agent-actions/]. Most teams stop at verify. The integration gate is where the lease contract pays off.

```yaml
# Extended integration gate in lease contract
integration_gate:
  required_reviews: 1
  required_checks: ["phpstan", "pest", "lint"]
  auto_merge: false
  merge_strategy: "squash"
  pre_merge_hooks:
    - "verify_agent_a.py"
    - "check_conflicts_with_main.py"
  post_merge_actions:
    - "cleanup_worktree.py"
    - "notify_downstream_agents.py"
    - "update_deployment_manifest.py"
```

### Conflict Detection Before Merge

```python
# /opt/agents/check_conflicts_with_main.py
#!/usr/bin/env python3
"""
Pre-merge conflict check. Runs in the agent's worktree.
Detects if the agent's branch has conflicts with main before attempting merge.
"""
import subprocess
import sys
from pathlib import Path

WORKTREE_PATH = "/home/developer/project-agent-a"
BRANCH = "feature/agent-a-backend-api"

def has_conflicts_with_main() -> dict:
    # Fetch latest main
    subprocess.run(["git", "fetch", "origin", "main"], cwd=WORKTREE_PATH, check=True)
    
    # Try merge in memory (--no-commit --no-ff)
    result = subprocess.run(
        ["git", "merge", "--no-commit", "--no-ff", "origin/main"],
        cwd=WORKTREE_PATH,
        capture_output=True,
        text=True
    )
    
    has_conflict = result.returncode != 0
    
    # Abort the test merge
    subprocess.run(["git", "merge", "--abort"], cwd=WORKTREE_PATH, capture_output=True)
    
    return {
        "ok": not has_conflict,
        "conflicts": result.stdout if has_conflict else [],
        "message": "Conflict detected with main" if has_conflict else "Clean merge possible"
    }

if __name__ == "__main__":
    result = has_conflicts_with_main()
    import json
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["ok"] else 1)
```

## Rollback and Compensation: When the Lease Expires

The lease contract must define what happens when things go wrong. Digital Thought Disruption's control plane series defines the full loop: "execute, verify, rollback" [Source: https://digitalthoughtdisruption.com/2026/07/25/execute-verify-rollback-agent-actions/].

```yaml
# Rollback section in lease contract
rollback:
  triggers:
    - condition: "heartbeat_expired"
      action: "revoke_lease_and_cleanup"
      cleanup:
        - "git worktree remove --force"
        - "delete_heartbeat_files"
        - "notify_owner"
    - condition: "verification_failed"
      action: "return_to_agent_with_feedback"
      max_retries: 2
      backoff_minutes: [15, 60]
    - condition: "integration_conflict"
      action: "create_conflict_resolution_task"
      assign_to: "platform_team"
    - condition: "max_duration_exceeded"
      action: "force_checkpoint_and_extend_or_revoke"
      checkpoint_command: "git commit -am 'WIP: lease checkpoint at $(date)'"
      extend_hours: 2
      max_extensions: 1
```

The key insight: **the compensation action belongs in the lease contract, not in the agent code**. The agent does the work. The contract defines what "work not done" looks like and how to fix it.

![Compensation actions defined in contract, not agent code](/img/parallel-agents-shared-checkout-lease-5.png)

## Implementation Checklist: From Zero to Production

You don't need all components on day one. Start here:

### Week 1: Worktree Isolation
- [ ] Audit current agent runs — identify all agents targeting the same repo
- [ ] Create worktrees for each agent role (backend, frontend, migration, etc.)
- [ ] Update agent wrappers to `cd` into their assigned worktree before running
- [ ] Verify no staging pollution or branch conflicts in a test run

### Week 2: Lease Contracts
- [ ] Create `/etc/agent-leases/` with one YAML per agent
- [ ] Define: resource, max_duration, heartbeat_interval, ownership, proof requirements
- [ ] Deploy heartbeat writer (systemd timer or agent wrapper integration)
- [ ] Deploy dead man's switch checker (runs every 2 minutes)

### Week 3: Verification Probes
- [ ] Write one verification probe for the highest-impact agent
- [ ] Define expected files, test commands, static analysis rules
- [ ] Deploy as a standalone check (not part of the agent run)
- [ ] Add to lease contract's `proof.verification_probe`

### Week 4: Integration Gate + Rollback
- [ ] Configure required reviews and checks in lease contract
- [ ] Implement pre-merge conflict detection
- [ ] Define rollback triggers and compensation actions
- [ ] Run a game day: manually expire a lease, verify cleanup + owner notification

{{< details summary="Common objections (and responses)" >}}
**"This is overengineering for two agents."**
If two agents on one checkout have ever caused a force-push recovery session, it's not overengineering. The worktree pattern is 3 `git` commands. The lease contract is YAML. The heartbeat is 30 lines of Python. This is not Kubernetes.

**"Our agents are polite — they use different branches."**
Branches in the same worktree share the index. Staging pollution still happens. `git commit` captures everything staged. Worktrees give each agent its own index.

**"We already have PR reviews."**
PR reviews happen *after* the agent pushes. The lease contract prevents the corruption *before* it reaches the remote. The integration gate *is* the PR review, but with verified pre-conditions.

**"Our agents are idempotent, so re-running is always safe."**
Idempotency handles re-runs. It doesn't handle *silent corruption* from staging pollution. If Agent A stages `UserController.php` and Agent B stages `UserService.php`, a single commit contains both. Idempotency doesn't undo that.

**"We don't have time to add this to every agent."**
Start with the agent pair that shares a repo. The pattern scales. You add leases incrementally.
{{< /details >}}

{{< field-note title="Field note" >}}
In the Modoo Laravel SaaS projects, we migrated our parallel agent pipelines to worktree isolation last quarter. The single biggest factor in eliminating silent corruption: each agent gets its own worktree with a lease contract that expires. No more "who force-pushed main at 2 AM" incidents. The heartbeat file is 30 lines of Python. The verification probe is 50 lines. The lease YAML is 40 lines. This is not infrastructure — it's discipline encoded as code.
{{< /field-note>}}

## What You Should Do Monday Morning

1. **Audit your agent fleet** — List every coding agent (Claude Code, Codex, OpenCode, Hermes subagents, custom wrappers) that targets the same Git repository. For each pair, answer: "If they run simultaneously on the same checkout, what breaks?" If the answer includes "staging pollution" or "force-push recovery," that pair needs worktree isolation *this week*.

2. **Create the first worktree pair** — Pick the two highest-impact agents. Run `git worktree add` for each. Update their wrapper scripts to `cd` into the worktree. Run a test parallel execution. Verify zero staging pollution.

3. **Write the first lease contract** — `/etc/agent-leases/agent-a.yaml` with: resource (worktree path), max_duration_hours (4), heartbeat_interval_seconds (60), ownership (name + phone), proof (heartbeat file + verification probe path). Commit to git.

4. **Deploy the heartbeat writer** — 30-line Python script, called by the agent wrapper every 60 seconds. Deploy the dead man's switch checker — systemd timer every 2 minutes, alerts to Slack + PagerDuty.

5. **Write one verification probe** — Choose the agent whose silent failure hurts most (API changes, migration scripts, schema edits). Write a 50-line script that queries actual side effects: files created, tests passing, static analysis clean, git status clean.

6. **Schedule a game day** — Within two weeks, manually expire a lease heartbeat. Verify the cleanup runs, the owner gets alerted, the worktree is removed, and no orphan commits remain.

The goal is not perfect isolation. The goal is: *when a parallel agent run produces silent corruption, a named human knows within minutes and has a documented path to fix it.*

## Further Reading

- {{< source href="https://git-scm.com/docs/git-worktree" label="Git Worktree Documentation" >}} — Official reference for worktree commands and options
- {{< source href="https://news.hada.io/topic?id=26120" label="GeekNews: Parallel AI Workers (PAW)" >}} — Git worktree, Kanban UI, tmux for parallel AI agent management
- {{< source href="https://digitalthoughtdisruption.com/2026/07/25/execute-verify-rollback-agent-actions/" label="Digital Thought Disruption: Execute, Verify, Rollback Agent Actions" >}} — Control plane architecture for agent safety
- {{< source href="https://tianpan.co/blog/2026-04-19-decision-provenance-agentic-systems" label="TianPan: Decision Provenance in Agentic Systems" >}} — Audit trails, ownership handoffs, compliance requirements

---

**Related hubs:** [AI Agent Operations](/ai-agent-operations/) · [Developer Tools](/developer-tools/) · [Start Here](/start-here/)

*See also: [[parallel-agent-shared-checkout]], [[zombie-task-detection]], [[cron-silent-failure-patterns-infra]], [[agent-edit-contract]], [[autonomous-agent-cron-pipelines]]*