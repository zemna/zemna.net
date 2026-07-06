---
title: "Your Cron Job Is Not Healthy Until the Artifact Proves It"
date: 2026-06-30T07:00:00+07:00
draft: false
description: "A production checklist for cron jobs that proves useful artifacts exist, are fresh, and can be consumed downstream after the process exits."
topics: ["tutorial", "reliability"]
cover: /covers/artifact-health-checks-for-agent-cron-jobs.png
---

Your cron job exited zero. Fine. Where is the artifact?

That is the question I want on every scheduled job review now. Not "did the process run?" Not "did the dashboard stay green?" Not "did the log avoid a stack trace?" A scheduled job is healthy only when the expected artifact exists, is fresh, and passes a domain check. Anything weaker is process theater.

I learned this the boring way: daily automations that returned success while producing stale files, empty drafts, partial JSON, or a social post with no live URL. The shell was satisfied. The work was not done. Classic cron monitoring catches missed schedules and non-zero exits. It does not know whether your export has rows, whether your blog post reached `content/posts/`, whether your agent wrote the report, or whether a downstream consumer can use the output.

This is a hands-on tutorial and deep-dive for fixing that gap. It works for backups, analytics pulls, AI agent jobs, static-site publishing, and any task where the real deliverable is an artifact. The pattern is deliberately small: define the artifact contract, wrap the producer, verify the artifact, then ping success. You do not need a new platform to start. You need one scheduled job, one verifier, and the discipline to make the success signal come after the result is inspected.

![Three-state health model for cron jobs](/img/artifact-health-checks-for-agent-cron-jobs-1.png)

## Process health and artifact health are different signals

Most cron monitoring starts with a heartbeat. A job sends a ping when it completes; if the ping does not arrive on time, the monitor alerts. Healthchecks.io documents this pattern directly: the cron job sends an HTTP request every time it completes, and the service notifies you when the ping does not arrive at the expected time. [Source: https://healthchecks.io/docs/monitoring_cron_jobs/]

That is useful. Keep it. It catches jobs that never ran, servers that died, schedules that drifted, and scripts that crashed before the final ping.

But heartbeat monitoring answers one question: did the job report completion? It does not answer the more expensive question: did the job produce useful work?

Cronitor's public examples show the same completion-ping pattern, with richer metadata such as duration and counts attached to a completion request. [Source: https://cronitor.io/cron-job-monitoring] That metadata is the hint. A serious job should not just say "complete." It should say "complete, and here is the artifact I produced, here is its size, here is its age, here is the record count, here is the URL that returned HTTP 200."

The distinction matters because many failures are not crashes. A web-alert guide phrases the problem plainly: a job can succeed with exit code 0 while producing wrong results, such as processing 0 records instead of 10,000. [Source: https://web-alert.io/blog/cron-job-monitoring-background-tasks]

For AI agent jobs, this gets worse. Bob Renze documented an AgentChat silent failure where a health check cron ran 180 times across six hours and logged warnings, but the human was not notified. [Source: https://dev.to/bobrenze/ai-agent-silent-failures-what-6-hours-of-undetected-downtime-taught-me-about-monitoring-3ja8] That number belongs to Renze's system, not mine. The lesson generalizes: if the job can report activity while failing to produce output, the artifact is the only honest witness.

Here is the simple model I use:

| Layer | Question | Example check | Failure it catches |
|---|---|---|---|
| Process | Did the command exit cleanly? | exit code, timeout, final ping | crashes, missed schedules |
| Artifact | Did the deliverable exist? | file exists, non-zero size, mtime | empty output, wrong path, stale file |
| Domain | Is the deliverable useful? | JSON field, row count, HTTP 200, word count | partial work, no-op success, broken downstream |

The first layer is necessary. The second and third layers are where most silent failures die.

This also changes alert quality. A page that says "cron missed expected ping" is useful, but it still leaves the responder asking what state the job left behind. A page that says "daily-social.json is 91 bytes, missing platforms, and contains empty result" points straight at the failure. The responder knows whether to rerun collection, inspect credentials, or backfill a downstream table. Artifact checks turn monitoring from a binary alive/dead signal into a short diagnosis attached to the artifact that users actually depend on.

## Start every scheduled job by naming the artifact

Before writing a verifier, write one sentence:

> This job is successful when `[artifact]` exists, is newer than `[freshness window]`, and passes `[domain check]`.

That sentence forces decisions that logs hide.

For a database backup, the artifact is a compressed dump file. It must be larger than a minimum size, newer than the schedule window, and restorable enough that `pg_restore --list` can read it.

For a static-site blog job, the artifact is not `/tmp/blog-draft.md`. A draft is an intermediate. The real artifact is the published post under `content/posts/`, the generated page under `public/blog/<slug>/`, the pushed commit, and the live URL returning HTTP 200.

For an analytics job, the artifact is not "script finished." It is a JSON snapshot containing a date, platform names, and numeric metrics. An empty array may be valid for some systems, but if your daily social report normally contains platform metrics, an empty array is a failure until proven otherwise.

For an AI agent cron, the artifact is often a Markdown report, a queue state transition, a database row, a pull request, or a scheduled Buffer post ID. The verifier should inspect that object, not the agent's self-report.

![Artifact contract checklist](/img/artifact-health-checks-for-agent-cron-jobs-2.png)

A useful artifact contract has four fields:

| Field | Meaning | Bad default |
|---|---|---|
| Path or handle | Where the result must appear | relying on stdout only |
| Freshness window | How new it must be | accepting yesterday's file |
| Minimum substance | Size, rows, words, records, IDs | accepting a zero-byte file |
| Domain assertion | The result is actually usable | checking only file existence |

The point is not bureaucracy. The point is making success machine-checkable.

Be careful with artifacts that represent intentional emptiness. Some jobs legitimately produce zero records: no failed payments today, no abuse reports this hour, no new leads overnight. Do not let that case weaken the verifier into accepting any empty output. Encode the idle state explicitly. A JSON artifact can say `{"status":"idle","reason":"no_new_records","checked_at":"..."}`. A Markdown report can contain a required `## No incidents` section. The difference between "nothing happened" and "the job failed to look" must appear in the artifact, not in a human's memory of how the system usually behaves.

## Wrap the job so verification runs on every exit path

The easiest shell pattern is an `EXIT` trap. The job does its work. The trap verifies the artifact. If the job exits zero but the artifact fails validation, the wrapper exits non-zero.

```bash
#!/usr/bin/env bash
set -euo pipefail

ARTIFACT="/var/reports/daily-social.json"
PING_URL="${PING_URL:-}"

verify_artifact() {
  python3 /opt/jobs/verify_artifact.py \
    --path "$ARTIFACT" \
    --max-age-minutes 90 \
    --min-bytes 200 \
    --json-field date \
    --json-field platforms \
    --json-equals status=ok
}

on_exit() {
  status=$?

  if verify_artifact; then
    if [ -n "$PING_URL" ]; then
      curl -fsS -m 10 --retry 3 -o /dev/null "$PING_URL?status=ok" || true
    fi
    exit "$status"
  fi

  if [ -n "$PING_URL" ]; then
    curl -fsS -m 10 --retry 3 -o /dev/null "$PING_URL?status=artifact_failed" || true
  fi
  exit 1
}

trap on_exit EXIT

python3 /opt/jobs/collect_social_metrics.py --output "$ARTIFACT"
```

This wrapper is intentionally plain. `set -euo pipefail` catches common shell mistakes. The verifier is separate Python because artifact checks grow quickly. The heartbeat happens after validation, not before it.

Healthchecks.io shows the common cron pattern where a successful script is followed by `curl` to a ping URL. [Source: https://healthchecks.io/docs/monitoring_cron_jobs/] Move that ping behind your artifact verifier. A ping before verification says "the process ended." A ping after verification says "the deliverable survived inspection."

There is one subtle choice in the wrapper: if the original job failed with a non-zero status and the artifact still verifies, the wrapper preserves the original status. That is conservative. You can change it for jobs where artifact validity is the only success signal, but do it deliberately.

## Use a verifier that checks existence, freshness, size, and content

Here is a small Python verifier I keep around. It is boring on purpose. It checks that a file exists, is recent enough, is large enough, avoids known failure markers, and optionally contains required JSON fields.

```python
#!/usr/bin/env python3
import argparse
import json
import sys
import time
from pathlib import Path

FAILURE_MARKERS = [
    "No response generated",
    "empty result",
    "timeout window",
    "Traceback (most recent call last)",
    "rate_limit_exceeded",
]


def fail(message: str) -> int:
    print(f"ARTIFACT_CHECK_FAIL: {message}", file=sys.stderr)
    return 1


def load_text(path: Path, limit: int = 2_000_000) -> str:
    data = path.read_bytes()
    return data[:limit].decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--max-age-minutes", type=int, default=60)
    parser.add_argument("--min-bytes", type=int, default=1)
    parser.add_argument("--json-field", action="append", default=[])
    parser.add_argument("--json-equals", action="append", default=[], help="field=value check")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        return fail(f"missing file: {path}")
    if not path.is_file():
        return fail(f"not a regular file: {path}")

    stat = path.stat()
    if stat.st_size < args.min_bytes:
        return fail(f"too small: {stat.st_size} bytes < {args.min_bytes}")

    age_seconds = time.time() - stat.st_mtime
    max_age_seconds = args.max_age_minutes * 60
    if age_seconds > max_age_seconds:
        return fail(f"stale file: {age_seconds:.0f}s old > {max_age_seconds}s")

    text = load_text(path)
    for marker in FAILURE_MARKERS:
        if marker in text:
            return fail(f"contains failure marker: {marker}")

    if args.json_field:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            return fail(f"invalid JSON: {exc}")
        for field in args.json_field:
            if field not in payload:
                return fail(f"missing JSON field: {field}")
            if payload[field] in (None, "", [], {}):
                return fail(f"empty JSON field: {field}")
        for check in args.json_equals:
            if "=" not in check:
                return fail(f"bad json-equals check, expected field=value: {check}")
            field, expected = check.split("=", 1)
            if str(payload.get(field)) != expected:
                return fail(f"JSON field {field}={payload.get(field)!r}, expected {expected!r}")

    print(f"ARTIFACT_CHECK_OK: {path} size={stat.st_size} age={age_seconds:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it locally before wiring it to cron:

```bash
python3 verify_artifact.py \
  --path /var/reports/daily-social.json \
  --max-age-minutes 90 \
  --min-bytes 200 \
  --json-field date \
  --json-field platforms
```

Do not make the verifier clever too early. Clever verifiers become another silent failure surface. Start with four boring checks. Add domain checks only when a real incident proves you need them.

### Put domain checks close to the domain

A file can exist and still be wrong. That is where domain checks earn their keep.

For a blog publish job, I would check all of these before reporting success:

```bash
#!/usr/bin/env bash
set -euo pipefail

POST_SLUG="$1"
POST_FILE="$HOME/projects/zemna.net/content/posts/${POST_SLUG}.md"
PUBLIC_DIR="$HOME/projects/zemna.net/public/blog/${POST_SLUG}"
URL="https://zemna.net/blog/${POST_SLUG}/"

test -s "$POST_FILE"
grep -q '^topics:' "$POST_FILE"
grep -q '^cover:' "$POST_FILE"

words=$(python3 - "$POST_FILE" <<'PY'
import re, sys
text = open(sys.argv[1], encoding='utf-8').read()
body = text.split('---', 2)[-1]
print(len(re.findall(r"\b[\w'-]+\b", body)))
PY
)

test "$words" -ge 2500

test -d "$PUBLIC_DIR"
status=$(curl -s -o /dev/null -w '%{http_code}' "$URL")
test "$status" = "200"

echo "BLOG_ARTIFACT_OK slug=$POST_SLUG words=$words status=$status"
```

For an analytics job, the domain check is different. You care about schema and numbers:

```python
#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("/var/reports/social-metrics-history.json")
payload = json.loads(path.read_text())

required_platforms = {"instagram", "x", "threads"}
seen = {item["platform"] for item in payload["platforms"]}
missing = required_platforms - seen
if missing:
    raise SystemExit(f"missing platforms: {sorted(missing)}")

for item in payload["platforms"]:
    if "posts" not in item or "engagement_rate" not in item:
        raise SystemExit(f"incomplete metric row: {item}")

print("SOCIAL_METRICS_ARTIFACT_OK")
```

For a queue worker, the artifact may be a database transition: `pending` to `done`, `done_at` within the run window, and a non-empty result payload. For a crawler, it may be row count plus dedupe ratio. For an AI agent, it may be a file, a task ID, a commit SHA, or a Buffer post ID.

![Domain checks for scheduled jobs](/img/artifact-health-checks-for-agent-cron-jobs-3.png)

The domain check should be owned by the team that owns the domain. Operations can tell you whether the process ran. Only the domain can tell you whether the work matters.

## Wire the verifier into cron and CI

Here is a crontab entry that treats the wrapper as the only scheduled command:

```cron
# daily social metrics, Asia/Jakarta server time
5 8 * * * PING_URL="https://hc-ping.com/your-uuid" /opt/jobs/run_social_metrics_with_artifact_check.sh >> /var/log/social-metrics.log 2>&1
```

And here is a GitHub Actions version for a scheduled static-site check:

```yaml
name: scheduled-artifact-check

on:
  schedule:
    - cron: "10 1 * * *"
  workflow_dispatch:

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run publisher
        run: ./scripts/publish_daily_post.sh
      - name: Verify artifact
        run: |
          python3 scripts/verify_artifact.py \
            --path public/blog/latest/index.html \
            --max-age-minutes 30 \
            --min-bytes 5000
      - name: Ping monitor after artifact check
        if: success()
        run: curl -fsS -m 10 --retry 3 -o /dev/null "$PING_URL"
        env:
          PING_URL: ${{ secrets.HEALTHCHECKS_URL }}
```

The ordering is the whole point. Run job. Verify artifact. Ping monitor. Report success.

If you ping before verification, the monitor becomes a diary of attempts. If you ping after verification, it becomes a signal of completed work.

## What you should do Monday morning

Pick three scheduled jobs. Do not start with the whole fleet. Choose one that writes a file, one that calls an API, and one that publishes something visible.

For each job, write the artifact contract sentence:

1. What exact artifact proves success?
2. How fresh must it be?
3. What minimum size, row count, word count, or ID must exist?
4. What domain assertion proves it is usable?

Then add the smallest verifier that catches the failure you already know is possible. A backup verifier does not need a full restore on day one; it can start with non-zero size and `pg_restore --list`. A blog verifier does not need browser automation on day one; it can start with frontmatter, word count, generated HTML, and HTTP 200. An agent verifier does not need full semantic grading; it can start with non-empty output, absence of failure markers, and a task state transition.

After that, move your success ping behind the verifier. This is the step that changes behavior. The monitoring service should only receive a success signal after the artifact passes. Send failure metadata if your monitor supports it. Cronitor documents completion pings with optional metadata such as duration and count; use that style to send artifact size, row count, or URL status when available. [Source: https://cronitor.io/cron-job-monitoring]

Finally, write down the first false positive. You will get one. In one environment, the minimum byte threshold is too high. On a quiet holiday, a legitimate report produces zero rows. A long-running report needs a wider freshness window. Tune from real misses, not from imagination.

One more practical move: keep the verifier output stable. Print one success line and one failure prefix. `ARTIFACT_CHECK_OK` and `ARTIFACT_CHECK_FAIL` are boring strings, which is exactly why they work. Your log search, alert rule, and postmortem notes can key on them without parsing a paragraph of agent prose. If the job uses an LLM, this matters even more. The agent can write fluent explanations all day; the verifier should write a small deterministic sentence that another program can trust.

Also separate retry from verification. Retrying a failed API call is fine. Retrying a failed artifact check can hide damage if the second run overwrites the evidence. When a verifier fails, preserve the bad artifact with a timestamped suffix before the next attempt. A broken JSON file is more useful than a clean log that says the retry eventually worked. Production debugging starts with the first bad artifact, not the final green run.

### The real rule

Cron is allowed to say "I ran." It is not allowed to say "I succeeded" by itself.

For scheduled work, success lives in the artifact. The file exists. The timestamp is fresh. The content has substance. The domain check passes. The downstream URL opens. The queue row moved. The report contains data.

That is the line I use now: no artifact, no success.

## Further reading

- Healthchecks.io: monitoring cron jobs with completion pings — https://healthchecks.io/docs/monitoring_cron_jobs/
- Cronitor: cron job monitoring and completion metadata — https://cronitor.io/cron-job-monitoring
- Bob Renze: AI agent silent failures and the six-hour AgentChat incident — https://dev.to/bobrenze/ai-agent-silent-failures-what-6-hours-of-undetected-downtime-taught-me-about-monitoring-3ja8
