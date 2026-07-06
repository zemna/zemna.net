---
title: "Zero-Cost Observability for Agent Crons"
date: 2026-07-06T07:00:00+07:00
draft: false
topics: ["devops", "reliability"]
tags: ["observability", "cron", "ai-agents", "laravel", "vue", "posthog", "sentry", "opentelemetry"]
description: "A low-cost observability pattern for agent crons using logs, artifacts, summaries, and delivery checks before adding paid monitoring tools."
cover: /covers/zero-cost-observability-agent-crons.png
slug: zero-cost-observability-agent-crons
---

A cron job that says `success` can still leave no customer email sent, no blog post published, no report attached, and no safe way back. AI-assisted development makes that failure mode sharper: the agent often completes the instruction it was given, while the system around it has no proof that the work is usable.

The fix is not a larger dashboard on day one. Before adding another paid automation layer, prove three things on the smallest possible surface: one artifact, one alert, and one rollback path. The question is not whether this demos well; it is whether it survives maintenance, handoff, and local constraints.

This post is for solo maintainers and small teams running AI agents, cron jobs, Laravel/Vue SaaS flows, content pipelines, and internal scripts that already have enough moving parts. The goal is zero-cost observability first: local files, structured logs, a shell verifier, GitHub Actions, and free developer or usage-based free tiers only when they earn their place.

<!--more-->

{{< note type="warning" title="Success is not evidence" >}}
Exit code zero only proves that a process ended cleanly. It does not prove the expected artifact exists, the artifact is fresh, the downstream route works, or the previous version can be restored.
{{< /note >}}

![Three proof checkpoints: artifact, alert, and rollback](/img/zero-cost-observability-agent-crons-1.png)

## Start With the Three Proofs

The smallest useful observability contract has three proofs.

| Proof | Question it answers | Cheap implementation | Failure it catches |
|---|---|---|---|
| Artifact | Did the job create the thing users or maintainers need? | File existence, checksum, timestamp, row count, published URL | Empty reports, missing exports, stale generated content |
| Alert | Will a human or system know the job failed? | CI failure, Sentry Cron miss, email, Slack webhook, GitHub issue | Silent cron failures, hung agents, partial deploys |
| Rollback | Can the previous known-good state be restored? | Git revert, release symlink, database snapshot, content backup | Broken auto-publish, bad AI edits, corrupted generated files |

This is not a replacement for full observability. It is the entry ticket. The OpenTelemetry observability primer describes observability in terms of emitting signals such as traces, metrics, and logs so developers can troubleshoot without adding more instrumentation during the incident [Source: https://opentelemetry.io/docs/concepts/observability-primer/]. That definition is useful, but it also reveals the trap: teams can collect signals and still miss the artifact that mattered.

For an AI-agent cron, the artifact is usually simple:

- a Markdown post generated under `content/posts/`
- a JSON report with non-empty `items`
- a CSV export with a minimum row count
- an email body rendered and queued
- a Laravel job record marked complete with a linked object
- a public URL returning HTTP 200

The alert should be boring. It should fire when the proof fails, not when someone remembers to check a dashboard. Sentry documents Cron Monitoring as a way to monitor the uptime and performance of scheduled, recurring jobs [Source: https://docs.sentry.io/product/crons/]. That is useful once the job boundary is clear. First, define the boundary yourself: what output proves the job did the right work?

The rollback path is where many small systems are weakest. A cron writes a file, commits it, pushes it, and triggers a deployment. If the content is wrong, the rollback cannot depend on another AI agent guessing the repair. It needs a named command, a previous revision, or a backup directory.

{{< details summary="The zero-cost rule" >}}
Zero-cost does not mean never paying for tools. It means the first layer should be portable, inspectable, and cheap enough to run before the team has pricing meetings. Sentry advertises a free developer plan on its pricing page [Source: https://sentry.io/pricing/]. PostHog presents transparent usage-based pricing with a free tier and says a card is only needed when usage exceeds free-tier limits or advanced needs apply [Source: https://posthog.com/pricing]. Use those tiers after the local proof exists, not instead of it.
{{< /details >}}

## Build the Artifact Verifier First

A verifier is a small program that refuses to accept vague success. It checks the artifact directly and exits non-zero when the output is missing, stale, empty, or suspicious.

For a content pipeline, I usually start with shell because it runs everywhere: Linux servers, GitHub Actions, local WSL, cheap VPS boxes, and most CI systems.

```bash
#!/usr/bin/env bash
set -euo pipefail

ARTIFACT_PATH="${1:?usage: verify-artifact.sh <path> <max_age_seconds>}"
MAX_AGE_SECONDS="${2:-900}"
MIN_BYTES="${MIN_BYTES:-400}"

if [[ ! -f "$ARTIFACT_PATH" ]]; then
  echo "artifact_missing path=$ARTIFACT_PATH" >&2
  exit 20
fi

size=$(wc -c < "$ARTIFACT_PATH" | tr -d ' ')
if (( size < MIN_BYTES )); then
  echo "artifact_too_small path=$ARTIFACT_PATH bytes=$size min=$MIN_BYTES" >&2
  exit 21
fi

now=$(date +%s)
modified=$(stat -c %Y "$ARTIFACT_PATH")
age=$(( now - modified ))
if (( age > MAX_AGE_SECONDS )); then
  echo "artifact_stale path=$ARTIFACT_PATH age_seconds=$age max=$MAX_AGE_SECONDS" >&2
  exit 22
fi

sha=$(sha256sum "$ARTIFACT_PATH" | awk '{print $1}')
echo "artifact_ok path=$ARTIFACT_PATH bytes=$size age_seconds=$age sha256=$sha"
```

This script does four things that a dashboard cannot infer reliably:

1. It checks the actual file.
2. It rejects tiny output that looks like a template failure.
3. It rejects stale output from a previous run.
4. It prints a checksum that can be pasted into a handoff note.

The checksum matters because AI-assisted workflows often rewrite the same filename repeatedly. When a maintainer asks, "Which draft did the agent publish?" the answer should not be "the latest one, I think." It should be a path, timestamp, and hash.

For JSON artifacts, use a stricter verifier. This one fails if the file is invalid JSON, if required keys are missing, or if an array is empty.

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
required_key = sys.argv[2] if len(sys.argv) > 2 else "items"

if not path.exists():
    print(f"json_missing path={path}", file=sys.stderr)
    sys.exit(30)

try:
    data = json.loads(path.read_text())
except json.JSONDecodeError as exc:
    print(f"json_invalid path={path} error={exc}", file=sys.stderr)
    sys.exit(31)

if required_key not in data:
    print(f"json_key_missing path={path} key={required_key}", file=sys.stderr)
    sys.exit(32)

value = data[required_key]
if isinstance(value, list) and len(value) == 0:
    print(f"json_array_empty path={path} key={required_key}", file=sys.stderr)
    sys.exit(33)

print(f"json_ok path={path} key={required_key} type={type(value).__name__}")
```

Do not make this verifier clever. It should be strict, short, and easy to run at 07:15 on a Monday when the published page is wrong and the agent transcript is too long to read.

![Terminal inspection panel for artifact and rollback checks](/img/zero-cost-observability-agent-crons-3.png)

## Wire the Alert Where the Job Already Runs

After the artifact verifier exists, put it in the same place the job runs. Do not start with a separate observability service. Start with the scheduler or CI lane that already owns the work.

Here is a GitHub Actions workflow for an AI-generated content draft. It runs the generation command, verifies the Markdown artifact, checks a JSON fact-check report, and uploads both as CI artifacts. If any verifier fails, the workflow fails.

```yaml
name: content-cron-proof

on:
  schedule:
    - cron: "0 0 * * 1-5"
  workflow_dispatch:

jobs:
  generate-and-verify:
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@v4

      - name: Generate draft
        run: |
          ./scripts/run-content-agent.sh \
            --topic-file ./ops/today-topic.md \
            --output /tmp/blog-draft.md \
            --factcheck /tmp/factcheck.json

      - name: Verify markdown artifact
        env:
          MIN_BYTES: "2500"
        run: |
          ./ops/verify-artifact.sh /tmp/blog-draft.md 1800

      - name: Verify fact-check JSON
        run: |
          python3 ./ops/verify-json.py /tmp/factcheck.json claims

      - name: Upload proofs
        uses: actions/upload-artifact@v4
        with:
          name: content-cron-proof
          path: |
            /tmp/blog-draft.md
            /tmp/factcheck.json
```

This workflow gives you one alert without buying anything: the CI job fails. It also gives you one artifact bundle: the draft and the fact-check report. That bundle is useful during handoff because the maintainer can download what the agent produced rather than reconstruct it from logs.

For server cron, the same pattern is a crontab plus a wrapper script:

```cron
# /etc/cron.d/content-agent
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

15 7 * * 1-5 deploy cd /srv/zemna && ./ops/run-content-cron.sh >> /var/log/content-agent.log 2>&1
```

The wrapper should write a compact state file every run:

```bash
#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="/srv/zemna/var/cron-state"
mkdir -p "$STATE_DIR"

run_id="$(date -u +%Y%m%dT%H%M%SZ)"
state="$STATE_DIR/content-agent-$run_id.json"
latest="$STATE_DIR/content-agent-latest.json"

./scripts/run-content-agent.sh --output /tmp/blog-draft.md --factcheck /tmp/factcheck.json
./ops/verify-artifact.sh /tmp/blog-draft.md 1800
python3 ./ops/verify-json.py /tmp/factcheck.json claims

python3 - <<'PY' > "$state"
import json, os, time
payload = {
    "status": "ok",
    "run_id": os.environ.get("run_id", "unknown"),
    "checked_at": int(time.time()),
    "artifact": "/tmp/blog-draft.md",
    "factcheck": "/tmp/factcheck.json",
}
print(json.dumps(payload, indent=2))
PY

cp "$state" "$latest"
```

The example above uses an inline Python snippet for JSON writing. In a production repository, I prefer a tiny committed script so shell quoting cannot break the state file. The principle stays the same: the cron writes a proof, not just a log line.

Sentry Crons fits after this boundary is defined. It can monitor scheduled recurring jobs and alert on missed or failed check-ins [Source: https://docs.sentry.io/product/crons/]. The product pricing page lists Sentry's free developer plan [Source: https://sentry.io/pricing/], so small teams can test the alert path without starting from an enterprise procurement path. Keep the local verifier anyway. Vendor alerts should confirm your proof, not replace it.

{{< source href="https://docs.sentry.io/product/crons/" label="Sentry Cron Monitoring documentation" >}}

## Add Product Signals Only After the Job Has Proof

Product analytics answers a different question from cron monitoring. Cron monitoring asks, "Did the scheduled work run?" Product analytics asks, "Did the user's behavior or product state show the expected result?"

PostHog's product analytics docs cover capturing and analyzing product events, and its docs include event capture as the base unit for reports [Source: https://posthog.com/docs/product-analytics]. PostHog's pricing page describes transparent, usage-based pricing with a free tier [Source: https://posthog.com/pricing]. That makes it a good second layer for small teams, as long as the event is tied to a real product outcome.

A Laravel SaaS example: an AI assistant generates a weekly workspace summary. The cron artifact is the rendered summary file or database row. The product signal is whether the summary became visible to a user and whether the user opened it.

```php
<?php

namespace App\Jobs;

use App\Models\Workspace;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Support\Facades\Http;
use Sentry\State\Scope;

class GenerateWorkspaceSummary implements ShouldQueue
{
    use Queueable;

    public function handle(Workspace $workspace): void
    {
        \Sentry\configureScope(function (Scope $scope) use ($workspace): void {
            $scope->setTag('cron.name', 'workspace-summary');
            $scope->setTag('workspace.id', (string) $workspace->id);
        });

        $summary = app('summary.generator')->forWorkspace($workspace);
        $path = storage_path("app/summaries/{$workspace->id}.md");
        file_put_contents($path, $summary->markdown);

        if (strlen($summary->markdown) < 800) {
            throw new \RuntimeException('Generated summary is too small to publish safely.');
        }

        Http::withHeaders([
            'Authorization' => 'Bearer '.config('services.posthog.key'),
        ])->post('https://app.posthog.com/capture/', [
            'api_key' => config('services.posthog.project_key'),
            'event' => 'workspace summary generated',
            'distinct_id' => 'workspace:'.$workspace->id,
            'properties' => [
                'workspace_id' => $workspace->id,
                'bytes' => strlen($summary->markdown),
                'artifact_path' => $path,
                'generator' => 'weekly-agent-cron',
            ],
        ]);
    }
}
```

This code does not treat analytics as proof by itself. The proof is still the file size check and the saved artifact. The PostHog event adds a product timeline that helps later: which workspace had a generated summary, how large was it, and when did the event fire?

| Layer | Good question | Bad question |
|---|---|---|
| Local verifier | Does the artifact exist and pass minimum quality gates? | Can I infer success from a green dashboard? |
| Cron monitor | Did the scheduled job start, finish, or miss its window? | Can the monitor know whether my generated content is useful? |
| Product analytics | Did the user-facing event happen after the job? | Can product events replace logs and artifacts? |
| Traces/logs/metrics | Where did the time, error, or dependency failure happen? | Can signals compensate for no rollback plan? |

OpenTelemetry's primer frames logs, metrics, and traces as signals emitted by instrumented systems [Source: https://opentelemetry.io/docs/concepts/observability-primer/]. For small teams, those signals become valuable after the job has a stable proof contract. Without the contract, you are collecting context around an undefined result.

![Layered observability stack from local verifier to telemetry signals](/img/zero-cost-observability-agent-crons-2.png)

## Keep the Rollback Path Boring

A rollback path should be executable by someone who did not write the automation. It should avoid mystery dashboards, avoid ad hoc database edits, and avoid asking an AI agent to "fix it" under pressure.

For content pipelines, I like a release directory pattern:

```bash
#!/usr/bin/env bash
set -euo pipefail

RELEASES="/srv/zemna/releases"
CURRENT="/srv/zemna/current"
BUILD_DIR="${1:?usage: promote-release.sh <build-dir>}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TARGET="$RELEASES/$STAMP"

mkdir -p "$RELEASES"
cp -a "$BUILD_DIR" "$TARGET"
ln -sfn "$TARGET" "$CURRENT"

echo "release_promoted target=$TARGET current=$CURRENT"
```

Rollback becomes one command:

```bash
#!/usr/bin/env bash
set -euo pipefail

RELEASES="/srv/zemna/releases"
CURRENT="/srv/zemna/current"
PREVIOUS="$(find "$RELEASES" -maxdepth 1 -mindepth 1 -type d | sort | tail -n 2 | head -n 1)"

if [[ -z "$PREVIOUS" ]]; then
  echo "rollback_failed reason=no_previous_release" >&2
  exit 40
fi

ln -sfn "$PREVIOUS" "$CURRENT"
echo "rollback_ok target=$PREVIOUS"
```

For Laravel, the rollback path can be as simple as "disable the schedule entry, restore the previous generated file, clear queue jobs for this class, and redeploy the previous commit." The important part is that the command exists before the incident.

{{< field-note title="Field note" >}}
In Modoo Laravel SaaS projects, the maintenance pressure usually appears in the seams: a queued Laravel job writes a file, Vue renders a dashboard card, a Windows-based operator checks the exported document, and a PHP cron updates the state. The failure is rarely one dramatic crash. It is a quiet mismatch between what the job claims and what the next person can verify. I treat every AI-agent verification task the same way: leave behind a path, a checksum, an event, and a rollback command that a tired maintainer can run without reading the whole transcript.
{{< /field-note >}}

Rollbacks also need naming. `rollback.sh` is better than a wiki paragraph. `make rollback-content` is better than a Slack memory. A GitHub Actions manual workflow is better than a private terminal incantation.

For SaaS features, add a feature flag to the rollback plan. If an AI-assisted job fills a recommendation table, the UI should be able to hide that recommendation block while the backfill is repaired. Product analytics can then confirm whether users stopped seeing the broken feature, but the flag is the rollback mechanism.

## Use Free Tiers With a Narrow Contract

The strongest reason to start with zero-cost observability is not saving money. It is preserving architecture discipline. A bigger dashboard can hide a weak boundary. A strict artifact verifier exposes it.

Use external tools when each one has a narrow contract:

- Sentry Crons: scheduled job check-ins, missed runs, duration, failure alerting [Source: https://docs.sentry.io/product/crons/]
- Sentry pricing page: a free developer plan exists for starting small [Source: https://sentry.io/pricing/]
- PostHog product analytics: product events, reports, and behavior analysis [Source: https://posthog.com/docs/product-analytics]
- PostHog pricing page: usage-based pricing with a free tier is published [Source: https://posthog.com/pricing]
- OpenTelemetry: shared language for emitted signals such as traces, metrics, and logs [Source: https://opentelemetry.io/docs/concepts/observability-primer/]

That list is enough for most small pipelines. It covers job health, product behavior, and future instrumentation vocabulary without requiring a custom platform team.

The contract should fit on one screen:

```yaml
observability_contract:
  job: content-agent-weekday
  artifact:
    path: /tmp/blog-draft.md
    verifier: ./ops/verify-artifact.sh /tmp/blog-draft.md 1800
    minimum_bytes: 2500
  alert:
    primary: github_actions_failure
    secondary: sentry_cron_checkin
  product_signal:
    provider: posthog
    event: blog draft generated
  rollback:
    command: ./ops/rollback-content.sh
    owner_note: "Restores previous release symlink and disables content cron if repeated failures occur."
```

This small YAML file has more operational value than a vague dashboard named "AI Automation Health." It tells the maintainer what to inspect, what should alert, what event should exist, and how to go back.

{{< note type="success" title="A useful dashboard comes later" >}}
Once the artifact, alert, and rollback path are stable, a dashboard becomes a view over known facts. Before that, it becomes a place to admire uncertainty.
{{< /note >}}

![YAML maintenance contract card with artifact, alert, product signal, and rollback](/img/zero-cost-observability-agent-crons-4.png)

## What You Should Do Monday Morning

Do this before buying a bigger automation dashboard.

1. **Pick one recurring job.** Choose the job that creates real user or maintainer pain when it silently fails. Good candidates: content publishing, invoices, weekly reports, AI review summaries, sitemap generation, data imports, and email digests.

2. **Name the artifact.** Write the exact path, table, URL, or message queue record that proves the job did its work. If you cannot name the artifact, the job is not ready for observability work. It is still design work.

3. **Write the verifier.** Start with file existence, minimum size, freshness, JSON validity, row count, or HTTP 200. Keep the first version under fifty lines.

4. **Run the verifier in the same lane as the job.** If the job runs in cron, call the verifier in the cron wrapper. If it runs in GitHub Actions, add a verification step. If it runs in Laravel Scheduler, make failed verification throw an exception and report it.

5. **Add one alert.** CI failure is acceptable. Sentry Cron Monitoring is acceptable once the job boundary is named. A Slack webhook is acceptable if it fires only on proof failure.

6. **Write the rollback command.** Do not write "manually restore previous version." Write the command. Test it on a non-production path.

7. **Add one product event only if it answers a user-facing question.** Use PostHog or another analytics tool to mark a visible product outcome, not to compensate for missing artifact proof.

8. **Make the proof easy to hand off.** Store the latest state file, artifact hash, CI artifact bundle, and rollback instruction where another maintainer can find them.

By Friday, you should be able to answer four questions without reading an agent transcript:

- What did the job create?
- Who or what alerts when the proof fails?
- What product event confirms the user-facing result?
- What command gets us back to the previous known-good state?

If those answers exist, then a dashboard has something real to display. If they do not exist, a dashboard only changes the shape of the uncertainty.

### Further reading

- {{< source href="https://opentelemetry.io/docs/concepts/observability-primer/" label="OpenTelemetry observability primer" >}}
- {{< source href="https://docs.sentry.io/product/crons/" label="Sentry Cron Monitoring" >}}
- {{< source href="https://posthog.com/docs/product-analytics" label="PostHog product analytics documentation" >}}

A small team does not need to observe everything on Monday. It needs one artifact, one alert, and one rollback path that actually work. Start there. Everything else can earn its place.
