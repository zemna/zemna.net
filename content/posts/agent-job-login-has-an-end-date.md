---
title: "Your Overnight Agent Job Has a Login With an End Date"
date: 2026-11-07T06:00:00+07:00
draft: false
slug: "agent-job-login-has-an-end-date"
description: "An unattended Claude Code job can stop with Not logged in while nothing in your code changed. The CLI now shows when a stored sign-in ends. Here is the preflight, the three proofs, and the weekly check that catch it first."
topics: ["ai-agents"]
tags: ["claude-code", "cron", "authentication", "unattended-jobs", "exit-codes", "agent-ops", "change-control"]
cover: /covers/agent-job-login-has-an-end-date.png
seo:
  primaryQuery: "claude code not logged in cron job"
  secondaryQueries:
    - "claude auth status loginExpiresAt"
    - "claude -p credential_expires_at"
    - "claude code unattended job login expires"
---

Here is a night a lot of teams will have.

You set up a nightly job in October. A coding agent reads the docs folder, writes a short report, and drops it where the team looks every morning. It runs for weeks. Nobody touches it. Then one morning the report is not there. The cron log has one line: `Not logged in`. Nothing in your code changed. Nobody changed a password. The job just stopped being allowed to talk to the model.

The annoying part is not that it broke. The annoying part is that you find out on the day you needed the report.

Claude Code shipped three small changes in the first week of November that all point at this problem. One of them shows you the date a stored sign-in ends. Two of them stop the CLI from saying "success" when it did not do the work. None of them is exciting. All of them are the kind of change that decides whether your overnight job is a tool or a trap.

The question is not whether an agent job works on the night you set it up; it is whether it still works, and still tells the truth, after the person who set it up has moved on to something else.

![Three clocks on one overnight job: the login end date, the cron schedule, and the check that the file was written](/img/agent-job-login-has-an-end-date-1.png)

## What the CLI now tells you, and what it still does not

Start with what is documented, because the details matter here.

`claude auth status` prints your authentication state as JSON, and `--text` gives a human version. It exits with code 0 if you are logged in and 1 if you are not. That alone is enough to build a check.

Running `claude -p` (the non-interactive mode for scripts) is documented to exit 0 on success and non-zero when the run fails. The same page adds a detail that is easy to skim past: when a failure happens inside the run, such as missing authentication, Claude Code prints the failure as the result on stdout. So the sentence you saw in your cron log, `Not logged in`, arrived as output, and the thing your scheduler cared about was the exit code next to it.

Now the three changes from the changelog. I read them on the official docs page and on the raw `CHANGELOG.md` in the Claude Code repository, and both say the same thing.

| Date | Release | What changed | Why a job owner cares |
|---|---|---|---|
| Nov 3 | 2.1.317 | `claude -p` no longer exits 0 when a full disk or quota lost its transcript or `~/.claude.json` writes. It prints an error and exits 1 in text and JSON output. Full NFS exports may be missed. | A run that could not save its own state used to look finished. |
| Nov 4 | 2.1.318 | `claude auth status` shows `loginExpiresAt`. `claude -p` JSON results carry `credential_expires_at`. `claude -p` text output prints a one-line warning on stderr starting 10 days before a stored claude.ai sign-in ends. | The end date is now something a script can read. |
| Nov 6 | 2.1.319 | `claude -p` no longer exits 0 in auto mode when its actions were refused because no safety check was available. `claude remote-control` no longer exits silently with status 0 when a first-run question gets no answer. Both exit 1 now. | Two more "green but did nothing" cases are closed. |

Read that table as a list of behaviors that existed until each fix shipped, not a list of features: a job could exit 0 and leave nothing behind, and a login could end with the first sign being a failed morning.

What the CLI still does not do is read your mind about the file you wanted. The CLI can tell you the process failed. It cannot know that `report.md` was supposed to appear in a folder your team opens at 09:00. That check is yours, and the rest of this post is how to build it without much code.

{{< note type="warning" title="The 10-day warning goes to stderr" >}}
The new warning is one line on stderr in `claude -p` text output. If your cron setup throws stderr away, or mails it to an address nobody reads, the warning exists and does nothing. Route it somewhere a person sees, or read the end date yourself with a script. The next section shows how.
{{< /note >}}

## One message, three different causes

"Not logged in" is a symptom, and the changelog shows three different causes for it in an unattended job.

The first is the one this post is named after. A stored claude.ai sign-in has an end date, and when the date passes the job cannot authenticate. Until this week you could not see that date from a script. Now `claude auth status` reports it as `loginExpiresAt`.

The second cause is less obvious. The 2.1.318 notes list a fix for jobs exiting with `Not logged in` when another terminal or host signs in again to the same account and organization on the same home. Read that sentence slowly. Your job did not expire. Somebody, or something, signed in again somewhere that shares the same home directory, and your job lost its footing. Think of a shared server where two people use the same service account, or a container image that mounts one home folder into several machines.

The same release also fixed `claude plugin` commands exiting before a slow token refresh was saved, which could sign you out on the next run. That is a third path to the same message, and again it has nothing to do with a calendar.

So the honest summary is this. When an unattended job prints `Not logged in`, you do not know which of these happened. A good preflight does not guess. It reports the state it can read, which is the end date, and it fails closed when it cannot read anything.

![Same message, different causes: the login ended on its date, another terminal signed in again on the same home, or a token refresh was not saved](/img/agent-job-login-has-an-end-date-2.png)

{{< field-note title="Field note" >}}
On the Laravel SaaS projects I maintain, every scheduled job that depends on a credential gets one extra line in the runbook: where the credential lives, who renewed it last, and the date it stops working. That habit started with SSL certificates and database passwords, long before agents. An agent login is the same kind of object. It is a secret with a lifetime, attached to a job nobody looks at. The fix was never clever. It was putting the date next to the cron line, where the next maintainer would trip over it.
{{< /field-note >}}

## A preflight that reads the date and refuses to guess

Here is the first script. It asks `claude auth status` for the state, reads `loginExpiresAt` if there is one, and returns one of three exit codes: 0 for fine, 10 for "fine, but the sign-in ends soon", and 2 for "do not run the job".

Two choices in it are deliberate. First, the changelog says the field holds the date a stored sign-in ends but does not say what format it uses, so the script accepts an ISO 8601 string or a Unix timestamp in seconds or milliseconds. Run `claude auth status` once on your machine and keep whichever branch you actually need. Second, an answer the script cannot parse counts as a failure, not a pass. A CLI that prints a welcome banner or an error page instead of JSON should stop the job.

```python {linenos=inline}
#!/usr/bin/env python3
"""login_preflight.py - complain before the job runs, not during it.

Exit codes: 0 = fine, 10 = fine but the sign-in ends soon, 2 = do not run.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone

WARN_DAYS = 10  # the CLI's own stderr warning starts 10 days out; match it


def parse_when(value):
    """Accept an ISO 8601 string or a Unix timestamp (seconds or milliseconds)."""
    if isinstance(value, (int, float)):
        seconds = value / 1000 if value > 1e11 else value
        return datetime.fromtimestamp(seconds, tz=timezone.utc)
    when = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return when if when.tzinfo else when.replace(tzinfo=timezone.utc)


def main() -> int:
    proc = subprocess.run(
        ["claude", "auth", "status"], capture_output=True, text=True, timeout=60
    )
    if proc.returncode != 0:  # documented: exits 1 when not logged in
        print(f"FAIL not signed in (exit {proc.returncode}): {' '.join(proc.stdout.split())[:120]}")
        return 2

    try:
        status = json.loads(proc.stdout)
    except json.JSONDecodeError:  # an unreadable answer is not a pass
        print(f"FAIL cannot read auth status: {proc.stdout.strip()[:200]!r}")
        return 2
    raw = status.get("loginExpiresAt")
    if raw is None:  # API keys and some auth methods have no end date
        print(f"OK method={status.get('authMethod')} (no end date reported)")
        return 0

    ends = parse_when(raw)
    days_left = (ends - datetime.now(timezone.utc)).days
    if days_left < 0:
        print(f"FAIL sign-in ended {ends:%Y-%m-%d}")
        return 2
    if days_left <= WARN_DAYS:
        print(f"WARN sign-in ends {ends:%Y-%m-%d} ({days_left} days left)")
        return 10
    print(f"OK sign-in ends {ends:%Y-%m-%d} ({days_left} days left)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

I ran this two ways. Against the real CLI on my host, which is version 2.1.316 and signed out, it behaves as documented: `claude auth status` exits 1 with JSON that has `"loggedIn": false`, and the script prints `FAIL not signed in (exit 1)` and returns 2. That host predates the end-date field, so for every other case I used a small stand-in `claude` script that prints what the changelog says the newer release prints. That proves the logic, the exit codes, and the failure branches. It does not prove the exact shape of `loginExpiresAt`, which is why the parser accepts several shapes. Treat the first run on a current CLI as part of the setup.

Here is what the six cases printed. All six use the stand-in; the logged-out row also matched the real CLI.

| Stand-in state | Output | Exit code |
|---|---|---|
| Sign-in ends in 40 days | `OK sign-in ends 2026-12-17 (39 days left)` | 0 |
| Sign-in ends in 3 days | `WARN sign-in ends 2026-11-10 (2 days left)` | 10 |
| Sign-in ended yesterday | `FAIL sign-in ended 2026-11-06` | 2 |
| Logged out, CLI exits 1 | `FAIL not signed in (exit 1): {"authMethod":"none"}` | 2 |
| API key, no end date | `OK method=api_key (no end date reported)` | 0 |
| CLI prints a banner, not JSON | `FAIL cannot read auth status: 'Welcome to a new CLI'` | 2 |

The days-left numbers read one lower than the stand-in's setting because the script rounds down to whole days. That is the safe direction for a warning.

## Three proofs for one job

The preflight answers one question: can the job log in tonight. It says nothing about whether the job did its work. For that I use a wrapper with three separate proofs, and I keep them separate on purpose, because each one catches a different kind of silence.

1. **The login proof.** The preflight above. If it fails, the job does not start, and the log says `BLOCKED login`.
2. **The process proof.** The exit code of `claude -p`. Non-zero means the run failed. This is the one the CLI keeps getting better at.
3. **The artifact proof.** The file the job was supposed to leave behind exists, is not empty, and is newer than the moment the job started. This is the one only you can write.

```bash
#!/usr/bin/env bash
# run_agent_job.sh <job-name> - one job, three separate proofs.
set -u
JOB="${1:?usage: run_agent_job.sh <job-name>}"
BASE="${AGENT_BASE:-/srv/agents}"
OUT_DIR="$BASE/out/$JOB"
ARTIFACT="$OUT_DIR/report.md"
mkdir -p "$OUT_DIR"
cd "$OUT_DIR" || exit 1
START_MARK="$(mktemp)"
trap 'rm -f "$START_MARK"' EXIT
stamp() { date -Is; }

# Proof 1: the login works today, and we know when it stops working.
python3 "$BASE/bin/login_preflight.py"
rc=$?
if [ "$rc" -ne 0 ] && [ "$rc" -ne 10 ]; then  # 10 = warn, still run
  echo "$(stamp) $JOB BLOCKED login"
  exit 3
fi

# Proof 2: the process says it finished.
claude -p "Audit the docs folder and write report.md here" \
  --output-format json > result.json 2> stderr.txt
code=$?
if [ "$code" -ne 0 ]; then
  echo "$(stamp) $JOB FAILED exit=$code"
  exit 4
fi

# Proof 3: the thing it had to leave behind exists, and it is new.
if [ ! -s "$ARTIFACT" ] || [ "$ARTIFACT" -ot "$START_MARK" ]; then
  echo "$(stamp) $JOB NO_ARTIFACT exit=$code"
  exit 5
fi
echo "$(stamp) $JOB OK artifact=$(wc -c < "$ARTIFACT")B"
```

The `START_MARK` temp file is the small trick that makes proof 3 honest. It is created before the run, so `-ot` ("older than") rejects a `report.md` left over from yesterday. Without it, a job that silently does nothing still passes, because last night's file is sitting there.

I ran the wrapper against the stand-in in six modes. The logged-out row also matched the real CLI, which printed `BLOCKED login` and exited 3. Each kind of failure exits with its own code, so the morning log tells you which proof failed.

| Mode | Log line | Exit code |
|---|---|---|
| Healthy, 40 days left | `nightly OK artifact=9B` | 0 |
| Healthy, 3 days left | `WARN sign-in ends ...` then `nightly OK artifact=9B` | 0 |
| Logged out | `nightly BLOCKED login` | 3 |
| Unreadable auth answer | `nightly BLOCKED login` | 3 |
| Run crashed with exit 1 | `nightly FAILED exit=1` | 4 |
| Run exited 0, wrote nothing | `nightly NO_ARTIFACT exit=0` | 5 |

The sixth row is the one to stare at. Exit 0, no file. That is the case the changelog quietly closed in three separate places this week, and it is also the case your own wrapper has to close, because the next tool you plug into this script will have its own version of it.

One bug in my first draft of this wrapper is worth telling. The first version only blocked on the preflight's exit code 2. When I fed it a CLI that printed garbage, the preflight crashed with a Python traceback, which exits 1, and the wrapper walked straight past it and ran the job. A check that fails open is worse than no check, because you trust it. The fix is the `-ne 0 && -ne 10` line: only the two known-good codes continue, and everything else stops.

![The three proofs in order: login check, process exit code, artifact exists and is newer than the start mark, each with its own log line and exit code](/img/agent-job-login-has-an-end-date-3.png)

## Exit 0 used to lie in more places than you would guess

It is worth saying plainly how many of this week's fixes are the same story. Here are the ones from the changelog, in the CLI's own words, compressed.

- A full disk or quota lost the transcript or `~/.claude.json` writes, and `claude -p` exited 0. Now it exits 1 (2.1.317).
- Auto mode refused the job's actions because no safety check was available, and `claude -p` exited 0. Now it exits 1 (2.1.319).
- `claude remote-control` exited silently with status 0 when a first-run question got no answer, which happens in scripts, services and batch jobs. Now it says why and exits 1 (2.1.319).
- `claude -p` and Agent SDK sessions reported success when an API error cut off a reply while a mod hooked `turn.step` (2.1.318).

I wrote about the general shape of this on the blog before, in [A Green Cron Exit Is Not a Finished Job](/blog/a-green-cron-exit-is-not-a-finished-job/) and [Your Cron Job Is Not Healthy Until the Artifact Proves It](/blog/your-cron-job-is-not-healthy-until-the-artifact-proves-it/). Those posts argue that an exit code is a claim, not a fact. This week's changelog is the vendor agreeing with that and fixing the cases people reported.

Do not read it as "the exit code can be trusted now." Read it as "the exit code lies less than it did last week." Your artifact check should stay exactly where it is. When the CLI later fixes the next silent case, your wrapper will already have been catching it.

If you run agents that stay up for hours instead of minutes, the same idea scales up: the job needs a heartbeat and a proof, not just a live process. I covered that in [Long-Running AI Agents: From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/) and [Your AI Agent Pipeline Has No Zombie Detection](/blog/your-ai-agent-pipeline-has-no-zombie-detection-heres-how-to-add-it/). A login that ends is a slow way to become a zombie: the schedule keeps firing, the job keeps starting, and no work comes out.

## Put the date where a person will trip over it

A script that reads the end date is half the answer. The other half is making sure a human is told while there is still time. Three cheap moves cover it.

**Check on a day shift, not a night shift.** The nightly job runs at 02:15 and nobody is awake to read a warning. Run the preflight on its own once a week at a normal working hour and send the result to wherever your team actually reads things.

```cron
# m   h  dom mon dow  command
15    2  *   *   *    /srv/agents/bin/run_agent_job.sh nightly-docs-audit >> /var/log/agents/nightly-docs-audit.log 2>&1
30    9  *   *   1    /srv/agents/bin/login_preflight.py >> /var/log/agents/login.log 2>&1 || echo "agent login needs attention" | mail -s "agent login" team@example.com
```

Note the `||` on the second line. The preflight returns 10 when the sign-in is close to ending and 2 when it is unusable, and both are non-zero, so both send mail. If you want the warning but not the alarm, branch on the exit code in a small wrapper instead.

**Write the owner and the date in the runbook.** One row per scheduled agent job, and the row has the same four fields every time.

```yaml
# docs/agent-jobs.yaml - one entry per scheduled agent job
nightly-docs-audit:
  schedule: "02:15 daily (server time)"
  login:
    kind: stored claude.ai sign-in
    home: /home/agent-svc          # nothing else may sign in on this home
    ends: read from `claude auth status`   # do not copy the date here by hand
    renewed_by: "@sri"
  artifact: /srv/agents/out/nightly-docs-audit/report.md
  fails_loud_to: "#eng-agents"
```

The `ends:` field says "read from `claude auth status`" on purpose: a hand-copied date drifts the first time somebody renews early. The runbook records where to look and who is on the hook; the script reads the truth.

**Give each job its own home.** That `home:` comment is the fix for the second cause above. If two people or two hosts share one home directory for one account, one sign-in can knock out the other. A service account with its own home, used by one job, removes that whole category.

## What you should do Monday morning

1. **List your scheduled agent jobs.** Every cron entry, scheduled task and CI job that calls an agent CLI. Most teams find one more than they expected.
2. **For each job, write down how it logs in.** Stored sign-in, API key, or a cloud provider credential. Only the stored sign-in has the end date described here.
3. **Run `claude auth status` on each job's host** and look at what `loginExpiresAt` actually looks like on your version. Adjust `parse_when` to match.
4. **Install the preflight** in front of the job and make anything other than 0 or 10 stop it.
5. **Add the artifact proof.** Name the file the job must leave behind and check that it is non-empty and newer than the start.
6. **Move the warning to daytime.** Add the weekly preflight at a time somebody is awake, and send it to a place people read.
7. **Give each job its own home and write the renewer's name** in the runbook.
8. **Update your agent CLI where the jobs run**, so the three exit-code fixes from this week apply to you, and then keep the artifact check anyway.

If you are building the wider habit of checking agent work before you trust it, the operations notes are collected on [AI Agent Operations](/ai-agent-operations/), and [Start Here](/start-here/) lists the posts in the order I would read them.

## Further reading

- {{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code changelog (2.1.317, 2.1.318, 2.1.319)" >}}
- {{< source href="https://code.claude.com/docs/en/headless" label="Claude Code docs: run Claude Code programmatically" >}}
- {{< source href="https://code.claude.com/docs/en/cli-reference" label="Claude Code docs: CLI reference, claude auth status" >}}
- {{< source href="https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md" label="Claude Code CHANGELOG.md on GitHub" >}}
