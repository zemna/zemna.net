---
title: "Building a Background Agent Recovery CLI: The Three-Gate Check"
date: 2026-08-14T07:00:00+07:00
lastmod: 2026-09-02T07:00:00+07:00
draft: false
slug: "building-a-background-agent-recovery-cli-the-three-gate-check"
description: "Chat said done is not recovered. I wait for a file on disk, a job log that names why the run stopped, and one fail-once restart from the last good commit."
topics: ["tutorials"]
tags: ["coding-agents", "verification", "background-agents", "cli", "change-control"]
cover: /covers/building-background-agent-verification-cli.png
seo:
  primaryQuery: "background agent verification CLI"
  secondaryQueries:
    - "chat said done is not recovered"
    - "coding agent artifact check"
    - "fail-once restart from last good commit"
---

The overnight coding agent wrote "Done." The chat was green. The shipping cost file on disk was still yesterday's version.

I do not mark that run recovered. Recovered means three things I can show a junior without opening the vendor UI: a file that exists, a job log that names why the process stopped, and one restart from the last good commit that is allowed to fail once.

The question is not whether the agent demos well. The question is whether the next person can restart the job from a known commit when I am offline.

<!--more-->

![Three-gate recovery: file on disk, job log, one fail-once restart](/img/building-background-agent-verification-cli-1.png)

## Chat said done is not recovered

Vendors train you to trust the last message. VS Code even stores a checkpoint on every agent response, and **Restore Checkpoint** rolls the workspace and the chat back together [Source: https://code.visualstudio.com/learn/foundations/reviewing-and-controlling-agent-changes]. That is a useful undo. It is not a recovery record.

Addy Osmani's long-running-agent write-up names the failure I still see: the model forgets, it declares the task complete when it is not, and a single sitting is the wrong shape for overnight work. State has to live outside the chat [Source: https://addyosmani.com/blog/long-running-agents/]. Anthropic's harness post is the same idea in files: a progress log on disk, a feature list that starts failing, and the next session reading those files instead of the last boast [Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents].

On this desk the translation is smaller than a product. I do not wait for a new CLI brand. I wait for three artifacts:

| Gate | What "Done" in chat usually means | What I require |
| --- | --- | --- |
| 1. File on disk | The model listed a path | The path exists and is newer than the job start |
| 2. Job log | The session ended | A log line names why it stopped |
| 3. Fail-once restart | Someone can click Run again | One restart from the last good commit, then stop |

If any gate is empty, the job is hung or lying. I do not open a second agent to "just finish it." That is how you get two half-writes and no owner.

{{< note type="warning" title="Done is a sentence, not a file" >}}
A green chat is a claim. Recovered is a file, a stop reason, and one restart you can point at. If you cannot name those three, the overnight run is not closed.
{{< /note >}}

{{< field-note title="Field note" >}}
On the Laravel/Vue SaaS desks I keep, the overnight agent often touches `app/Services/ShippingCost.php`. Chat says the shipping test is green. I still `stat` that file, read `artifacts/job.log` for the stop line, and only then allow one `git reset --hard` to the last tagged good commit plus one re-run. I do not Full-Auto a second session because the first one typed Done. That is how a shipping change survives handoff when I am asleep and someone else has to roll the branch back.
{{< /field-note >}}

## Gate 1 — the file has to be on disk

Juniors get hurt here because the chat lists paths. Listing is cheap. Writing is the work.

I pin the expected path on the ticket before the first prompt. For a shipping bug that is one file, not the whole tree. The map-as-allow-list rule from [Your Coding Agent Needs a Map, Not a Bigger Context Window — Part 2](/blog/your-coding-agent-needs-a-map-not-a-bigger-context-window-part-2/) still applies: if the agent grepped a sibling folder, the run already left the ticket.

The check is boring on purpose. A one-year developer can run it.

```bash {linenos=inline,hl_lines=[8,"14-18"]}
#!/usr/bin/env bash
# scripts/assert-recovery-file.sh
# Usage: assert-recovery-file.sh PATH JOB_START_EPOCH
set -euo pipefail

path="${1:?expected file path}"
start="${2:?job start unix time}"

if [[ ! -f "$path" ]]; then
  echo "FAIL: recovered file missing: $path" >&2
  exit 1
fi

mtime="$(stat -c %Y "$path" 2>/dev/null || stat -f %m "$path")"
if [[ "$mtime" -lt "$start" ]]; then
  echo "FAIL: $path mtime $mtime is older than job start $start" >&2
  exit 1
fi

echo "PASS: $path exists and is newer than job start"
```

I store the job start as a number in `artifacts/job-start.txt` when the wrapper launches. If the file is missing, I do not argue with the chat. The gate failed.

Claude Code keeps file snapshots for the 100 most recent checkpoints in a session, and `/rewind` (or Esc twice on an empty prompt) opens a restore menu [Source: https://code.claude.com/docs/en/checkpointing]. Use that when you need to undo a bad turn. Do not treat rewind as proof the overnight file landed. Rewind is a chat tool. Gate 1 is `stat`.

Claude Code also says checkpointing does not track files changed by bash, and it is not a replacement for Git [Source: https://code.claude.com/docs/en/checkpointing]. That is why gate 3 is `git reset --hard` to a named good commit, not Esc twice on a hung overnight wrapper.

## Gate 2 — the job log has to name the stop

A process that exits 0 with an empty log is the same lie as a green cron. I already wrote the empty-output version in [Empty Tool Output Is Not Success Until the Harness Says Interrupted](/blog/empty-tool-output-is-not-success/). Recovery needs one more line: **why it stopped**.

Accept only a small set of stop reasons. Everything else is "unknown" and fails the gate.

```text
STOP_REASON=completed
STOP_REASON=interrupted
STOP_REASON=timeout
STOP_REASON=oom
STOP_REASON=tests_failed
```

The wrapper writes that line. The model does not. If the agent wants to claim completed, it still has to leave the file from gate 1. The log is the harness speaking.

```python {linenos=inline,hl_lines=[12,"20-24"]}
#!/usr/bin/env python3
"""scripts/assert-stop-reason.py — fail unless the job log names a stop."""
from __future__ import annotations

import sys
from pathlib import Path

ALLOWED = {
    "completed",
    "interrupted",
    "timeout",
    "oom",
    "tests_failed",
}


def main() -> int:
    log_path = Path(sys.argv[1] if len(sys.argv) > 1 else "artifacts/job.log")
    if not log_path.is_file():
        print(f"FAIL: job log missing: {log_path}", file=sys.stderr)
        return 1
    text = log_path.read_text(encoding="utf-8", errors="replace")
    reasons = [
        line.split("=", 1)[1].strip()
        for line in text.splitlines()
        if line.startswith("STOP_REASON=")
    ]
    if not reasons:
        print("FAIL: job log has no STOP_REASON= line", file=sys.stderr)
        return 1
    last = reasons[-1]
    if last not in ALLOWED:
        print(f"FAIL: unknown STOP_REASON={last}", file=sys.stderr)
        return 1
    print(f"PASS: STOP_REASON={last}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Addy Osmani's limitation section is blunt: auditing 24 hours of autonomous activity is a human-time problem, and structured artifacts (PRs, commits, briefings, test runs) are how you make it tractable [Source: https://addyosmani.com/blog/long-running-agents/]. A `STOP_REASON=` line is that artifact at the smallest size that still names the stop.

{{< note type="note" title="Interrupted is a real stop" >}}
If the harness was killed, write `STOP_REASON=interrupted`. Do not leave the last chat bubble as the record. Interrupted plus a missing file is hung. Interrupted plus a new file is a half-write you can restart once.
{{< /note >}}

![Recovery loop: detect the missing file, read the stop line, restart once](/img/building-background-agent-verification-cli-2.png)

## Gate 3 — one fail-once restart from the last good commit

Restart is where teams leak. Chat said done, someone hits Run again, the agent writes a second patch on top of a dirty tree, and now nobody knows which commit was good.

I tag the last good commit before the overnight job starts. Recovery is allowed to hard-reset to that tag **once**. If the second run also fails a gate, the ticket goes to a human. There is no third click.

```bash {linenos=inline,hl_lines=[11,"18-22"]}
#!/usr/bin/env bash
# scripts/fail-once-restart.sh
# Usage: fail-once-restart.sh GOOD_REF JOB_ID
set -euo pipefail

good="${1:?last good commit or tag}"
job_id="${2:?job id}"
stamp_dir="artifacts/restarts"
mkdir -p "$stamp_dir"
stamp="$stamp_dir/${job_id}.once"

if [[ -f "$stamp" ]]; then
  echo "FAIL: restart already used for $job_id — human owns the next step" >&2
  exit 1
fi

git rev-parse --verify "$good^{commit}" >/dev/null
git reset --hard "$good"
date -Iseconds >"$stamp"
echo "PASS: reset to $good; restart stamp written"
echo "Re-run the job wrapper now. Do not click a third time."
```

VS Code's restore is a conversation rollback. Git reset is the production rollback. Keep them separate. Restore Checkpoint when you are still in the IDE and the turn went wrong [Source: https://code.visualstudio.com/learn/foundations/reviewing-and-controlling-agent-changes]. Use the fail-once script when the overnight wrapper is the process you trust.

Long-running production still needs a sandbox that survives a directory change and a human who owns the budget. That page is [Long-Running AI Agents — From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/). This page is the morning after: the chat is closed, and you still have to prove recovered.

## Wire the three gates in one wrapper

You do not need a published binary named `agent-recover`. You need a wrapper that refuses to print success until the three files exist. Put it next to the Laravel app so the next person on the ticket can run it.

```bash {linenos=inline,hl_lines=[6,"28-32"]}
#!/usr/bin/env bash
# scripts/run-overnight-agent.sh
set -euo pipefail

job_id="${JOB_ID:-shipping-$(date +%Y%m%d)}"
expected="${EXPECTED_FILE:-app/Services/ShippingCost.php}"
good="${GOOD_REF:-recovery-good}"
root="$(git rev-parse --show-toplevel)"
art="$root/artifacts"
mkdir -p "$art"

date +%s >"$art/job-start.txt"
start="$(cat "$art/job-start.txt")"

# Replace this block with your real agent command.
# The wrapper owns the log. The model does not write STOP_REASON=.
set +e
your_agent_cmd --task "$job_id"
agent_ec=$?
set -e

if [[ "$agent_ec" -eq 0 ]]; then
  echo "STOP_REASON=completed" >>"$art/job.log"
else
  echo "STOP_REASON=tests_failed" >>"$art/job.log"
fi

set +e
"$root/scripts/assert-recovery-file.sh" "$root/$expected" "$start"
file_ec=$?
"$root/scripts/assert-stop-reason.py" "$art/job.log"
log_ec=$?
set -e

if [[ "$file_ec" -eq 0 && "$log_ec" -eq 0 ]]; then
  echo "RECOVERED: file + stop reason present"
  exit 0
fi

echo "NOT RECOVERED: running fail-once restart"
"$root/scripts/fail-once-restart.sh" "$good" "$job_id"
```

The wrapper is the CLI. If you later extract a Go binary, the contract stays the same: expected path, stop line, one stamp file. Do not wait for a GitHub release to start using the three files.

![Checklist YAML is optional; the three files are not](/img/building-background-agent-verification-cli-4.png)

## What this is not

This is not the five-name editor contract from [Five Things I Refused This Week](/blog/five-refusals-this-week/). That list is who pins the model, who merges, who retries. This page is only: **is the overnight job recovered.**

This is not a second zombie-detection essay. Detection without a file is still a dashboard. Recovery is the file.

This is not "restore the chat and call it a night." Chat restore is for a bad turn while you are watching. Overnight recovery is for a process you were not watching.

Anthropic's initializer agent writes `claude-progress.txt` so the next session is not blank [Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]. Keep a progress file if you want. I still fail the job if the shipping file is old. Progress text without an mtime check is another chat.

{{< details summary="Optional: a tiny verification.yaml next to the wrapper" >}}
If you already keep a checklist, keep it short. File existence, tests, build. Do not grow it into a second review system.

```yaml
task: "Fix shipping cost calculation"
expected_file: app/Services/ShippingCost.php
stop_reasons:
  - completed
  - interrupted
  - timeout
  - oom
  - tests_failed
restart:
  good_ref: recovery-good
  max: 1
checks:
  - id: file_newer_than_job
    type: file_mtime
    path: app/Services/ShippingCost.php
  - id: tests
    type: command
    command: php artisan test --filter=ShippingCost
```
{{< /details >}}

## Name the owner of the three files

A wrapper without an owner becomes folklore. Put three names on the ticket before the overnight run:

1. Who writes `EXPECTED_FILE`
2. Who reads `artifacts/job.log` in the morning
3. Who is allowed to click the fail-once restart

If those names are blank, do not start the agent. Abort is not stop. Abort still needs a retry owner. I ranked that refusal already. Here the artifact is the stamp file under `artifacts/restarts/`.

The operations hub for this family is [/ai-agent-operations/](/ai-agent-operations/). The map page tells the agent where it may search. The long-running page tells you the sandbox still has to hold after `cd`. This page tells you when you may say the job came back.

![Named owner for the grant: expected file, job log, restart stamp](/img/building-background-agent-verification-cli-5.png)

## What you should do Monday morning

1. Pick one overnight job this week. Write the expected path on the ticket (`app/Services/ShippingCost.php` or your equivalent). Do not start the agent until the path is there.
2. Copy `assert-recovery-file.sh`, `assert-stop-reason.py`, and `fail-once-restart.sh` into `scripts/`. Run them against last night's run even if chat said done.
3. Tag `recovery-good` on the last commit you would actually ship. That is the only reset target.
4. Create `artifacts/job.log` from the wrapper, not from the model. Require a `STOP_REASON=` line.
5. If the first restart stamp already exists, do not click Run. Assign a human. That person reads the diff.
6. Link this page, the [map allow-list](/blog/your-coding-agent-needs-a-map-not-a-bigger-context-window-part-2/), and [long-running agents](/blog/long-running-ai-agents-from-demos-to-production/) on the ticket so the next person does not invent a fourth gate.

If you are new to this desk, start at [/start-here/](/start-here/) and the [developer tools](/developer-tools/) hub. Then come back and fail one overnight job on purpose so you see the stamp file.

## Further reading

{{< source href="https://addyosmani.com/blog/long-running-agents/" label="Addy Osmani: Long-running Agents" >}}

{{< source href="https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents" label="Anthropic: Effective harnesses for long-running agents" >}}

{{< source href="https://code.visualstudio.com/learn/foundations/reviewing-and-controlling-agent-changes" label="VS Code: Reviewing and controlling agent changes" >}}

{{< source href="https://code.claude.com/docs/en/checkpointing" label="Claude Code docs: Checkpointing" >}}
