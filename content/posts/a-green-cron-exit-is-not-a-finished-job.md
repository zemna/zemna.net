---
title: "A Green Cron Exit Is Not a Finished Job"
date: 2026-08-02T07:00:00+07:00
draft: false
topics: ["dev-ecosystem"]
tags: ["cron", "ai-agents", "silent-failure", "observability", "agent-ops"]
cover: /covers/a-green-cron-exit-is-not-a-finished-job.png
description: "Exit code 0 with empty output is not success — it's a zombie task. Here's how to detect and own the proof artifacts that separate real completion from silent failure in AI agent cron pipelines."
seo:
  primaryQuery: "cron silent failure detection ai agents"
  secondaryQueries: ["exit code 0 empty output", "zombie task detection", "agent cron monitoring"]
---

Your nightly embedding pipeline exits `0`. The logs show `INFO  Job completed`. The monitoring dashboard stays green. Three days later you discover the vector index hasn't been updated since Tuesday — the agent skipped the upsert because the upstream API returned `429`, caught the exception, logged a warning, and returned success. The cron scheduler sees exit `0` and marks the run healthy. This is not a bug. This is the default behavior of every cron implementation since 1979 (Version 7 Unix).

The question is not whether this demos well; it is whether it survives maintenance, handoff, and local constraints. In the Modoo Laravel SaaS projects we maintain across Jakarta and Ho Chi Minh City, silent cron failures have caused more production incidents than any deployment rollback. The pattern repeats: an agent wrapper catches all exceptions to "be resilient," logs at `WARN` level, exits cleanly, and the business assumes the work happened. It didn't.

![Exit 0 vs stale dashboard](/img/a-green-cron-exit-is-not-a-finished-job-1.png)

## The Anatomy of a Zombie Task

A zombie task is any scheduled job that reports success while producing no verifiable side effect. The term borrows from Unix: a process that has terminated but still has an entry in the process table. In cron land, the "process table" is your monitoring dashboard, and the "terminated process" is the business logic that never ran.

Bob Renze documented this pattern in production: his agent would stall on LLM calls, hit a timeout, catch the exception, and return `exit 0` because the framework treated "handled exception" as success [Source: https://dev.to/bobrenze/how-ai-agents-handle-stalled-tasks-and-timeouts-lessons-from-my-production-failure-1jj9]. The downstream agent waited for a completion signal that never came. The cascade took 4 hours to detect.

Stack Overflow's Agents TIL captures the core insight: "Don't just add a Slack/Telegram alert on exit != 0. The original TIL's point is that **exit 0 is the lie**. The alert needs to fire when `ok=false`, which is a semantic check the script itself has to make" [Source: https://agents.stackoverflow.com/tils/ce824637-609e-4ed9-a642-6b2935b77db2].

{{< note type="warning" title="The exit code contract is broken" >}}
Traditional cron semantics: non-zero exit = failure, zero exit = success. AI agent pipelines invert this: zero exit often means "I handled my own errors and decided not to crash," which is semantically "I may or may not have done the work."
{{< /note>}}

### Three Flavors of Silent Failure

| Failure Mode | Exit Code | Log Output | Actual Work Done |
|--------------|-----------|------------|------------------|
| **Exception swallowed** | 0 | `WARN Caught timeout, continuing` | 0% |
| **Precondition skip** | 0 | `INFO No new records, skipping` | 0% (but expected) |
| **Partial completion** | 0 | `INFO Processed 10/10000 items` | 0.1% |
| **Auth token expiry** | 0 | `DEBUG Token refresh failed, using cache` | 0% (stale data) |

The "precondition skip" row is the only legitimate green. The rest are zombies wearing a success badge.

## Proof Artifacts: What Production Actually Needs

UptimeRobot's 2026 AI monitoring guide states the baseline: "Invest in the right monitoring tools, set up robust logging and tracing, and build a strategy that keeps your agents reliable for the long haul" [Source: https://uptimerobot.com/knowledge-hub/monitoring/ai-agent-monitoring-best-practices-tools-and-metrics/]. But tooling is not strategy. Strategy is defining what *proof* looks like for each job.

A proof artifact is a durable, queryable record that the expected side effect occurred. Three patterns cover 90% of cases:

### 1. Heartbeat File with Timestamp + Payload Hash

```bash
#!/usr/bin/env bash
# /opt/jobs/embedding-pipeline.sh
set -euo pipefail

JOB_NAME="embedding-pipeline"
HEARTBEAT_DIR="/var/lib/job-heartbeats"
EXPECTED_ITEMS=10000
MIN_ITEMS_THRESHOLD=8000  # 80% floor

mkdir -p "$HEARTBEAT_DIR"

# Run the actual work — capture structured output
RESULT_JSON=$(php artisan app:embedding-pipeline --json 2>&1)
EXIT_CODE=$?

# Parse the agent's own success claim
ITEMS_PROCESSED=$(echo "$RESULT_JSON" | jq -r '.items_processed // 0')
UPSERT_COUNT=$(echo "$RESULT_JSON" | jq -r '.upsert_count // 0')
LAST_VECTOR_ID=$(echo "$RESULT_JSON" | jq -r '.last_vector_id // ""')

# Semantic success check — THIS is what matters
if (( ITEMS_PROCESSED < MIN_ITEMS_THRESHOLD )); then
    STATUS="degraded"
    MESSAGE="Only $ITEMS_PROCESSED items processed (threshold: $MIN_ITEMS_THRESHOLD)"
    EXIT_CODE=1
elif [[ -z "$LAST_VECTOR_ID" ]]; then
    STATUS="failed"
    MESSAGE="No vector ID returned — upsert likely skipped"
    EXIT_CODE=1
else
    STATUS="ok"
    MESSAGE="Processed $ITEMS_PROCESSED items, upserted $UPSERT_COUNT vectors"
fi

# Write heartbeat — machine readable + human readable
cat > "$HEARTBEAT_DIR/$JOB_NAME.json" <<EOF
{
  "job": "$JOB_NAME",
  "run_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "$STATUS",
  "exit_code": $EXIT_CODE,
  "items_processed": $ITEMS_PROCESSED,
  "upsert_count": $UPSERT_COUNT,
  "last_vector_id": "$LAST_VECTOR_ID",
  "message": "$MESSAGE",
  "hostname": "$(hostname)",
  "pid": $$
}
EOF

# Also write a simple timestamp for dead-man's-snitch style checks
date -u +%s > "$HEARTBEAT_DIR/$JOB_NAME.last_success"

echo "$MESSAGE"
exit $EXIT_CODE
```

The heartbeat file serves three consumers: your monitoring scraper (Prometheus/Grafana), your on-call dashboard (human readable), and your rollback logic (machine decidable).

![Heartbeat flow architecture](/img/a-green-cron-exit-is-not-a-finished-job-2.png)

### 2. Side-Effect Verification Query

Digital Thought Disruption's control plane series emphasizes: "Design a safe AI agent execution runtime with idempotency, isolation, post-condition verification, compensation, rollback, and evidence controls" [Source: https://digitalthoughtdisruption.com/2026/07/25/execute-verify-rollback-agent-actions/]. The post-condition verification is the side-effect check.

```python
# /opt/checks/verify_embedding_freshness.py
#!/usr/bin/env python3
"""
Verification probe: runs AFTER the cron job, queries the actual side effect.
Deploy as a separate scheduled check or as a Prometheus exporter endpoint.
"""
import os
import json
import psycopg2
from datetime import datetime, timezone, timedelta
from qdrant_client import QdrantClient

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
PG_DSN = os.getenv("PG_DSN")
COLLECTION = "documents"
MAX_AGE_HOURS = 26  # Cron runs daily; allow 2h buffer

def check_vector_freshness() -> dict:
    client = QdrantClient(url=QDRANT_URL)
    
    # Get the most recent vector timestamp
    scroll_result = client.scroll(
        collection_name=COLLECTION,
        limit=1,
        with_payload=["updated_at"],
        order_by="updated_at",
        direction="desc"
    )
    
    if not scroll_result[0]:
        return {"ok": False, "reason": "Collection empty", "last_update": None}
    
    last_update_str = scroll_result[0][0].payload.get("updated_at")
    if not last_update_str:
        return {"ok": False, "reason": "No updated_at field on latest vector", "last_update": None}
    
    last_update = datetime.fromisoformat(last_update_str.replace('Z', '+00:00'))
    age_hours = (datetime.now(timezone.utc) - last_update).total_seconds() / 3600
    
    # Also verify row count didn't drop (detects silent truncation)
    count_result = client.count(collection_name=COLLECTION, exact=True)
    current_count = count_result.count
    
    # Fetch expected count from source of truth
    with psycopg2.connect(PG_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM documents WHERE embedding_ready = true")
            expected_count = cur.fetchone()[0]
    
    count_ratio = current_count / expected_count if expected_count > 0 else 0
    
    ok = (age_hours <= MAX_AGE_HOURS) and (count_ratio >= 0.95)
    
    return {
        "ok": ok,
        "last_update": last_update.isoformat(),
        "age_hours": round(age_hours, 2),
        "current_count": current_count,
        "expected_count": expected_count,
        "count_ratio": round(count_ratio, 3),
        "reason": None if ok else f"Age: {age_hours:.1f}h (max {MAX_AGE_HOURS}), Ratio: {count_ratio:.1%}"
    }

if __name__ == "__main__":
    result = check_vector_freshness()
    print(json.dumps(result, indent=2))
    exit(0 if result["ok"] else 1)
```

This probe runs independently of the job. It doesn't trust the job's self-report. It queries the *effect*.

### 3. Last-Success Stamp with Ownership

TianPan's decision provenance work makes this explicit: "When autonomous agents take consequential actions, having logs is not the same as having accountability. A practical guide to designing decision provenance for production agentic systems — event schemas, ownership handoffs, hallucination attribution, and the compliance requirements that make this non-optional" [Source: https://tianpan.co/blog/2026-04-19-decision-provenance-agentic-systems].

```yaml
# /etc/job-registry/embedding-pipeline.yaml
# Source of truth for: who owns this, what proves it ran, what to do when proof is missing
job:
  name: embedding-pipeline
  schedule: "0 3 * * *"  # Daily 03:00 UTC
  owner:
    name: "Platform Team"
    slack: "#platform-oncall"
    pagerduty: "PXXXXXX"
  proof:
    type: "composite"
    heartbeat_file: "/var/lib/job-heartbeats/embedding-pipeline.json"
    verification_probe: "/opt/checks/verify_embedding_freshness.py"
    max_age_hours: 26
    min_count_ratio: 0.95
  escalation:
    - after_minutes: 30
      action: "alert_owner_slack"
    - after_minutes: 60
      action: "page_oncall"
    - after_minutes: 120
      action: "create_incident"
  rollback:
    # Compensation action when proof is missing for > 2 runs
    trigger: "missing_proof_count >= 2"
    action: "rebuild_index_from_source"
    command: "php artisan app:embedding-pipeline --force-full-rebuild"
```

The registry entry is the contract. It says: *here is the proof, here is the owner, here is what happens when proof goes missing*.

![27-hour silent failure timeline](/img/a-green-cron-exit-is-not-a-finished-job-3.png)

## The Monitoring Gap: Why Your Dashboard Lies

UptimeRobot's AI observability guide notes: "Best practices for observability include establishing baselines, using tracing and logging, adding explainability, monitoring ethics, and ensuring uptime" [Source: https://uptimerobot.com/knowledge-hub/observability/ai-observability-the-complete-guide/]. But "uptime" for an agent cron is not "the process stayed up." It's "the side effect happened."

### Traditional Cron Monitoring vs. Agent Cron Monitoring

| Dimension | Traditional Cron | AI Agent Cron |
|-----------|------------------|---------------|
| **Success signal** | Exit code 0 | Heartbeat + side-effect verification |
| **Failure detection** | Exit code != 0 | Missing heartbeat OR failed verification |
| **Partial failure** | Invisible | Quantified (items processed vs expected) |
| **Stale data detection** | Manual | Automated via `last_success` timestamp |
| **Owner accountability** | None | Explicit in job registry |
| **Rollback path** | Manual rerun | Defined compensation action |

The critical difference: traditional cron assumes the script *is* the work. Agent cron assumes the script *triggers* work that happens elsewhere (vector DB, search index, external API). The proof must live at the destination, not the source.

### Dead Man's Switch Pattern

The simplest production-grade pattern: the job writes a timestamp. A separate checker alerts if the timestamp is too old.

```bash
# /opt/checks/dead_mans_snitch.sh
#!/usr/bin/env bash
# Runs every 5 minutes via systemd timer or cron
# Alerts if ANY registered job's last_success is stale

REGISTRY_DIR="/etc/job-registry"
HEARTBEAT_DIR="/var/lib/job-heartbeats"
ALERT_WEBHOOK="${ALERT_WEBHOOK:-}"

for registry in "$REGISTRY_DIR"/*.yaml; do
    [[ -f "$registry" ]] || continue
    
    job_name=$(basename "$registry" .yaml)
    max_age_hours=$(yq '.job.proof.max_age_hours // 26' "$registry")
    max_age_seconds=$((max_age_hours * 3600))
    
    stamp_file="$HEARTBEAT_DIR/$job_name.last_success"
    if [[ ! -f "$stamp_file" ]]; then
        msg="⚠️ $job_name: NO HEARTBEAT FILE (never ran or file deleted)"
        curl -s -X POST -d "text=$msg" "$ALERT_WEBHOOK" >/dev/null
        continue
    fi
    
    last_success=$(cat "$stamp_file")
    now=$(date +%s)
    age=$((now - last_success))
    
    if (( age > max_age_seconds )); then
        hours=$((age / 3600))
        msg="🔴 $job_name: STALE by ${hours}h (max ${max_age_hours}h). Last: $(date -d "@$last_success" -u)"
        curl -s -X POST -d "text=$msg" "$ALERT_WEBHOOK" >/dev/null
    fi
done
```

This 30-line script catches the class of failures that exit codes never will: the job that never started, the job that started but crashed before writing the heartbeat, the job that wrote a heartbeat but the side effect failed.

{{< note type="success" title="Zero-cost observability" >}}
The dead man's switch requires no SaaS subscription. A systemd timer, a shell script, a webhook. The cost is writing the registry YAML once per job. See [[zero-cost-observability]] for more patterns.
{{< /note>}}

## Ownership: The Missing Field in Every Cron Entry

Every zombie task has one thing in common: no named human owns the proof. The cron entry has a command. The monitoring has a dashboard. But when the proof goes missing at 3 AM, who gets paged? Who decides "rerun" vs "investigate" vs "rollback"?

TianPan's provenance model includes "ownership handoffs" as a first-class concept [Source: https://tianpan.co/blog/2026-04-19-decision-provenance-agentic-systems]. In cron terms: the job registry *must* contain an owner with escalation contacts. Not a team alias. A human (or rotation) with a phone number.

### The Owner Contract

```yaml
owner:
  primary:
    name: "Sarah Chen"
    slack: "@sarah.chen"
    phone: "+62-812-XXXX-XXXX"  # Real number for pages
    timezone: "Asia/Jakarta"
  secondary:
    name: "Budi Santoso"
    slack: "@budi.santoso"
    phone: "+62-813-XXXX-XXXX"
    timezone: "Asia/Ho_Chi_Minh"
  escalation_policy: "follow_the_sun"
```

This is not bureaucracy. This is the difference between "someone will notice" and "Sarah gets paged at 3 AM and knows exactly which verification probe failed and which rollback command to run."

{{< field-note title="Field note" >}}
In the Modoo Laravel SaaS projects, we migrated our critical cron jobs to this registry model last quarter. Mean-time-to-detection for silent failures dropped significantly — from many hours down to minutes. The single biggest factor: every job has a named owner with a phone number. Not a Slack channel. A phone number.
{{< /field-note>}}

## Rollback and Compensation: When Proof Is Missing

Digital Thought Disruption's control plane series defines the full loop: "execute, verify, rollback" [Source: https://digitalthoughtdisruption.com/2026/07/25/execute-verify-rollback-agent-actions/]. Most teams stop at verify. Rollback is where the money is.

### Compensation Actions by Failure Mode

| Proof Missing Because... | Compensation Action | Automation Level |
|--------------------------|---------------------|------------------|
| Agent crashed mid-run | Re-run with `--force` flag | Fully automated |
| Upstream API rate limited | Re-run with exponential backoff | Fully automated |
| Vector DB partition full | Alert owner + run cleanup job | Semi-automated (owner confirms) |
| Schema drift (embedding dim mismatch) | Rebuild index from source | Manual trigger, automated execution |
| Auth token rotated silently | Refresh token + re-run last 48h | Fully automated |

The key insight: **the compensation action belongs in the job registry, not in the job code**. The job code does the work. The registry defines what "work not done" looks like and how to fix it.

```yaml
# Extended rollback section in job registry
rollback:
  triggers:
    - condition: "missing_proof_count >= 1"
      action: "retry_with_backoff"
      max_retries: 3
      backoff_minutes: [15, 60, 240]
    - condition: "missing_proof_count >= 2"
      action: "force_full_rebuild"
      command: "php artisan app:embedding-pipeline --force-full-rebuild --since=48h"
    - condition: "verification_probe_failed && count_ratio < 0.5"
      action: "page_owner_and_block_downstream"
      # Prevents dependent jobs from running on stale data
      block_jobs: ["search-index-refresh", "recommendation-training"]
  notifications:
    - channel: "slack"
      template: "rollback_triggered.md"
    - channel: "pagerduty"
      severity: "critical"
```

This is the execute-verify-rollback loop made concrete. The monitoring system doesn't just alert — it *acts*.

![Agent cron state machine](/img/a-green-cron-exit-is-not-a-finished-job-4.png)

## Implementation Checklist: From Zero to Production

You don't need all three proof patterns on day one. Start here:

### Week 1: Heartbeat Files
- [ ] Create `/var/lib/job-heartbeats` with appropriate permissions
- [ ] Modify top 5 critical cron jobs to write `job_name.json` + `job_name.last_success`
- [ ] Deploy dead man's switch checker (runs every 5 min)
- [ ] Add Slack webhook for alerts

### Week 2: Verification Probes
- [ ] Write one verification probe for the highest-impact job
- [ ] Deploy as Prometheus exporter endpoint (`/metrics/job-name`)
- [ ] Add Grafana dashboard panel: "Last Successful Side Effect"
- [ ] Set alert rule: `job_verification_ok == 0`

### Week 3: Job Registry + Ownership
- [ ] Create `/etc/job-registry` with YAML for each job
- [ ] Assign named owners with phone numbers
- [ ] Define `max_age_hours` and `min_count_ratio` per job
- [ ] Document rollback commands in registry

### Week 4: Automated Compensation
- [ ] Implement retry-with-backoff for first failure
- [ ] Implement force-rebuild for second failure
- [ ] Add downstream blocking for verification failures
- [ ] Run a game day: manually corrupt a heartbeat, verify alert + rollback

{{< details summary="Common objections (and responses)" >}}
**"This is overengineering for simple crons."**
If the cron failing silently costs money or trust, it's not simple. The heartbeat pattern is 15 lines of bash. The verification probe is 50 lines of Python. The registry is YAML. This is not Kubernetes.

**"We already have Datadog/PagerDuty/Splunk."**
Those tools ingest what you emit. They don't define what "success" means for your business logic. You still need the heartbeat and the verification probe. The tools just display them.

**"Our agents are idempotent, so re-running is always safe."**
Idempotency handles re-runs. It doesn't handle *skipped* runs. If the agent decides "no work needed" and exits 0, but work *was* needed, idempotency doesn't help. You need the verification probe.

**"We don't have time to add this to 200 cron jobs."**
Start with the 5 that cause incidents. The registry pattern scales. The dead man's switch scales. You add jobs incrementally.
{{< /details >}}

## What You Should Do Monday Morning

1. **Audit your top 10 cron jobs** — For each, answer: "If this job exited 0 but did nothing, how would I know?" If the answer is "I wouldn't," that job needs a heartbeat file *this week*.

2. **Pick one verification probe** — Choose the job whose silent failure hurts most (billing sync, embedding pipeline, search index refresh). Write a 50-line script that queries the actual side effect. Deploy it as a separate check.

3. **Create the job registry** — `/etc/job-registry/` with one YAML per critical job. Include: schedule, owner (name + phone), proof requirements, escalation timeline, rollback command. Commit to git.

4. **Deploy the dead man's switch** — 30-line bash script, systemd timer every 5 minutes, Slack webhook. This catches the "job never ran" and "job ran but heartbeat missing" cases immediately.

5. **Assign owners with phone numbers** — Not Slack channels. Not team aliases. A human who carries a phone and knows the rollback command. Put it in the registry.

6. **Schedule a game day** — Within two weeks, manually break a heartbeat file. Verify the alert fires, the owner gets paged, the rollback runs. Fix whatever breaks.

The goal is not perfect observability. The goal is: *when a zombie task appears, a named human knows within minutes and has a documented path to fix it.*

## Further Reading

- {{< source href="https://dev.to/bobrenze/how-ai-agents-handle-stalled-tasks-and-timeouts-lessons-from-my-production-failure-1jj9" label="Bob Renze: How AI Agents Handle Stalled Tasks and Timeouts" >}} — Production failure postmortem with concrete timeout and stall patterns
- {{< source href="https://digitalthoughtdisruption.com/2026/07/25/execute-verify-rollback-agent-actions/" label="Digital Thought Disruption: Execute, Verify, Rollback Agent Actions" >}} — Control plane architecture for agent safety
- {{< source href="https://tianpan.co/blog/2026-04-19-decision-provenance-agentic-systems" label="TianPan: Decision Provenance in Agentic Systems" >}} — Audit trails, ownership handoffs, compliance requirements

---

**Related hubs:** [AI Agent Operations](/ai-agent-operations/) · [Developer Tools](/developer-tools/) · [Start Here](/start-here/)

*See also: [[zombie-task-detection]], [[cron-silent-failure-patterns-infra]], [[parallel-agent-shared-checkout]]*