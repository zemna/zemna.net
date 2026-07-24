---
title: "Audit the resume boundary: verify a coding agent from repository evidence"
description: "A practical way to decide whether a resumed coding-agent run is safe to continue: inspect local evidence, enforce command gates, review the diff, preserve test logs, and make rollback cheap."
date: 2026-07-23T07:00:00+07:00
draft: false
slug: "audit-agent-resume"
topics: ["dev-ecosystem", "tutorials"]
tags: ["coding-agents", "git", "testing", "developer-workflow", "verification"]
cover: "/covers/audit-agent-resume.png"
seo:
  primaryQuery: "coding agent resume verification"
  secondaryQueries:
    - "audit coding agent changes"
    - "git diff test log verification"
    - "coding agent rollback workflow"
---

A transcript tells you what an agent said it did. A repository tells you what it left behind.

That difference matters when a coding-agent session ends at an inconvenient point: the terminal disconnects, a context window closes, a machine reboots, a CI command hangs, or someone simply returns the next day. The tempting move is to resume and ask, "Where were we?" That question invites a narrative. It does not establish a safe starting point.

Treat the moment between an interrupted run and the next command as a boundary that needs an audit. The work may be correct. It may also be half-applied, based on a stale assumption, or blocked behind a test failure that never made it into the conversation. You do not need to distrust every agent. You need a procedure that does not require trust in a transcript.

This is a Dev Ecosystem tutorial about that procedure. It is vendor-neutral on purpose. The artifacts are ordinary repository facts: Git state, changed paths, generated evidence, command output, and a rollback point. Those facts survive a lost chat window and remain useful when a different person or tool takes over.

![A repository evidence trail before an agent resumes work](/img/audit-agent-resume-1.png)

{{< note >}}
A resume command is a navigation feature, not a verification result. Run the audit before you grant a resumed process permission to modify files, commit, deploy, or open a pull request.
{{< /note >}}

## Define the resume boundary before you resume anything

A resume boundary is the precise point where you stop treating prior conversation as evidence and start measuring the working tree. It has two sides:

- **Before the boundary:** what Git and local evidence files can prove at the time of inspection.
- **After the boundary:** new commands are allowed only after they pass explicit gates.

That sounds formal, but the first implementation can be small. Create a directory that records one audit per interrupted run. Keep it inside the repository if the team wants it reviewed, or put it in a local ignored directory if it contains paths or other machine-specific details. The important part is that the capture happens before any cleanup, rebase, formatter, dependency install, or new agent prompt changes the evidence.

Start with a clean, timestamped snapshot. This Bash script writes data that a reviewer can inspect later. It deliberately records command output instead of summarizing it. A summary can omit the one line that explains the failure.

```bash
#!/usr/bin/env bash
# scripts/audit-resume-boundary.sh
set -euo pipefail

stamp="$(date -u +%Y%m%dT%H%M%SZ)"
out=".agent-evidence/resume-${stamp}"
mkdir -p "$out"

git rev-parse --show-toplevel > "$out/repository-root.txt"
git status --short --branch > "$out/git-status.txt"
git diff --binary > "$out/working-tree.patch"
git diff --cached --binary > "$out/index.patch"
git diff --stat > "$out/diff-stat.txt"
git log -1 --format=fuller > "$out/head.txt"
git rev-parse HEAD > "$out/head-sha.txt"
git ls-files --others --exclude-standard > "$out/untracked-files.txt"

printf '%s\n' "$stamp" > "$out/captured-at-utc.txt"
printf 'Captured %s\n' "$out"
```

Run it from the repository root, then stop and read the capture. Do not let an agent run this script and immediately continue into implementation. The point is to create a human-readable checkpoint before any action changes the tree.

The script captures staged and unstaged changes separately because those states mean different things. A staged migration and an unstaged generated lockfile should not be bundled into one vague statement that "there are changes." It also captures untracked files. A coding agent can create a new test fixture, a temporary migration dump, or an accidental credential file without adding it to Git. `git diff` alone does not show that.

{{< details summary="Why record binary diffs?" >}}
Binary diffs make the audit directory larger, but they preserve the fact that a binary-tracked file changed. If repository policy excludes generated artifacts or large binaries, replace this with a file list and hashes that match that policy. Do not silently omit the category.
{{< /details >}}

For Claude Code specifically, Anthropic documents two ways to re-enter a prior conversation: `claude --resume <session>` resumes a selected session, and `claude --continue` resumes the most recent session in the current directory. Those commands locate conversation state. They do not compare the conversation with the current working tree. Capture the repository state first, then use the session feature if it remains useful.

{{< source href="https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-sessions" label="Anthropic: work with Claude Code sessions" note="Session continuation and resumption" >}}
{{< source href="https://docs.anthropic.com/en/docs/claude-code/hooks" label="Anthropic: Claude Code hooks reference" note="SessionStart behavior" >}}

## Make evidence files first-class repository outputs

A good evidence file answers a narrow question and names the command that produced it. Avoid one giant `agent-notes.md` where progress, guesses, and test output get mixed together. That document becomes another transcript.

Use separate files with stable meanings:

| Evidence file | Question it answers | Producer | Retention |
| --- | --- | --- | --- |
| `git-status.txt` | What was modified, staged, or untracked? | Git snapshot script | Keep with the audit |
| `working-tree.patch` | What content changed outside the index? | `git diff --binary` | Keep until review closes |
| `test-*.log` | What command ran and what did it print? | Test gate wrapper | Keep for the change set |
| `commands.jsonl` | Which gated commands ran, in what order, with which exit code? | Command wrapper | Keep with the audit |
| `rollback.txt` | Which commit or patch restores the starting state? | Auditor | Keep until merge or abandonment |

The files should be boring. That is a feature. A reviewer should be able to open a directory and answer: what changed, what was checked, what failed, and how do we undo it?

A JSON Lines command ledger works well because it is append-only and machine-readable without requiring a database. The wrapper below records the command as arguments, timestamps it in UTC, captures output, and appends its exit status. It does not use `eval`, so shell quoting stays out of the execution path.

```python
#!/usr/bin/env python3
# scripts/gate.py
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

if len(sys.argv) < 3:
    raise SystemExit("usage: gate.py <evidence-dir> <command> [args...]")

out_dir = Path(sys.argv[1])
command = sys.argv[2:]
out_dir.mkdir(parents=True, exist_ok=True)
started = datetime.now(timezone.utc).isoformat()
result = subprocess.run(command, text=True, capture_output=True, check=False)
finished = datetime.now(timezone.utc).isoformat()

log_name = "test-" + command[0].replace("/", "_") + ".log"
(out_dir / log_name).write_text(
    "$ " + " ".join(command) + "\n\nSTDOUT\n" + result.stdout +
    "\nSTDERR\n" + result.stderr,
    encoding="utf-8",
)
record = {
    "started_at": started,
    "finished_at": finished,
    "command": command,
    "exit_code": result.returncode,
    "log": log_name,
}
with (out_dir / "commands.jsonl").open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record, sort_keys=True) + "\n")

raise SystemExit(result.returncode)
```

Use it as a gate, not as decoration:

```bash
python3 scripts/gate.py "$EVIDENCE_DIR" npm run lint
python3 scripts/gate.py "$EVIDENCE_DIR" npm test -- --runInBand
python3 scripts/gate.py "$EVIDENCE_DIR" php artisan test
```

The wrapper stops the shell at the first nonzero exit only if the caller uses `set -e`. That is usually what you want in a gate script. If you need every check to run, call each command from a small driver that records failures and exits nonzero after the final command. Either way, preserve the log from a failure. Do not replace it with "tests failed; agent will investigate."

A repository may need different commands for its real contract: type checking, static analysis, a focused suite, a build, schema validation, or integration tests. Put the selection in versioned configuration rather than hiding it in a prompt. The agent can read the policy; the reviewer can change it in a pull request.

```yaml
# .agent-audit.yml
version: 1
evidenceDirectory: .agent-evidence
preResume:
  - git status --short --branch
  - git diff --check
requiredGates:
  - npm run lint
  - npm run typecheck
  - php artisan test --testsuite=Feature
review:
  requireDiffStat: true
  requireUntrackedReview: true
rollback:
  createPatch: true
  requireStartingHead: true
```

This file is not a security boundary. A process that can edit the repository can edit the configuration. It is an operational contract: the visible list of checks that must be met before the next phase of work. Enforce it in CI or a local wrapper when the risk warrants enforcement.

## Inspect the diff as a change, not as a story

The transcript may say "I fixed validation." The diff can show whether validation moved from a request object into a controller, whether a test was added, whether an unrelated dependency lockfile changed, and whether the code path that matters is even covered.

Read the diff in layers.

First, run `git diff --check`. It catches whitespace errors and conflict markers that slip through surprisingly often. Then inspect `git diff --stat` to establish the size and shape of the change. A one-line bug fix that touches forty files deserves an explanation before it deserves another prompt.

Next, inspect the full patch with the question "What is the behavioral claim here?" Write down the claim in plain language. For example: "A signed-out user receives a 401 from the billing export endpoint." Then find the code branch that implements it and the test that would fail before the change. If you cannot locate either, the agent has not given you enough evidence to continue safely.

This is where local artifacts beat a fluent conversation. The patch cannot tell you whether the test ran, but it can tell you whether the code and test refer to the same route name, feature flag, schema field, or error status. A test log cannot tell you whether the diff is appropriate, but it can tell you exactly what command exited zero. Each artifact has limits. Together they narrow the gap.

![Inspecting a code diff and repository graph before mutation](/img/audit-agent-resume-2.png)

For Laravel applications, inspect migration and configuration changes with extra care. A test suite running against SQLite may pass while a production database rejects the migration or interprets an index differently. The audit does not solve that mismatch by itself. It makes the mismatch visible: record the test environment, the migration status command, and the intended rollback command.

{{< field-note title="Laravel SaaS verification: audit the customer boundary" >}}
For a Laravel SaaS, put a tenant-isolation check in the required gates. Capture the test command and its log, then inspect the diff for tenancy middleware, query scopes, and route binding changes. If the agent changed an export endpoint, test both a tenant that owns the record and a tenant that does not. A passing happy-path test is not evidence that the boundary stayed intact.
{{< /field-note >}}

Vue applications need the same discipline in a different place. A resumed agent may change a composable, a store, and a component template in one pass. Review the component diff for the user-visible claim, then check the test output for the mode it ran under. A unit test that stubs the store may be useful, but it does not prove the route loads the data you changed. Record what the test establishes. Do not let a green check acquire a larger meaning than it earned.

## Put command gates between observation and mutation

After you capture the boundary, decide which commands are read-only and which commands are allowed to change the tree. This is the practical control that prevents an eager resume from erasing the state you meant to inspect.

A simple gate sequence has four phases:

1. **Observe:** record Git status, patches, untracked files, HEAD, and existing evidence.
2. **Validate the base:** run low-risk checks such as `git diff --check`, dependency integrity checks already used by the repository, and focused tests that do not write fixtures into the working tree.
3. **Authorize mutation:** only after the audit is reviewed, permit the agent to edit files, format code, update snapshots, or install dependencies.
4. **Validate the result:** capture the final diff, run the required gates, and write rollback instructions.

The word "authorize" is intentional. A prompt such as "continue where you left off" merges observation and mutation into one opaque step. Instead, give the resumed agent a bounded instruction: read these evidence files; do not modify files; report conflicts between the evidence and the current repository. Then let it edit only after a human or policy gate approves the report.

A useful first prompt is short:

> Read `.agent-evidence/resume-<timestamp>/`. Do not edit files or run commands that mutate the working tree. Compare `head-sha.txt`, `git-status.txt`, the patches, and command logs with the current repository. List any mismatch, missing test, untracked file, or failed command. Stop after the report.

This does not require a special agent platform. It works with a local CLI, an IDE extension, or a CI worker. It also separates a reviewable task from an implementation task.

Claude Code offers a concrete place to automate part of this control. Anthropic's hooks documentation says `SessionStart` hooks run when a session starts or resumes. A repository can use that event to print the current branch, record Git status, or warn when an evidence directory is missing. Do not use the hook to declare the work safe. A hook runs automatically; the decision still belongs to your gates and review process.

If the environment permits it, make the SessionStart hook call a read-only snapshot script. Keep the script fast and make its output obvious. A slow hook that performs network calls or edits files turns every resume into a surprise.

## Preserve test logs as evidence, not as terminal noise

Terminal output is fragile. It scrolls away, gets truncated in a chat client, and often disappears when a session closes. A test result that cannot be inspected later is weak evidence, especially after the code changes again.

Store the full command, standard output, standard error, exit code, start time, and finish time. The Python wrapper above records all of these except the environment. Add the selected runtime versions when your project depends on them. For example, a Laravel project may record `php -v` and `php artisan --version`; a Node project may record `node --version` and package-manager output. Record facts, not interpretations such as "correct version installed."

Do not treat a zero exit code as a universal approval. A passing command has a scope:

- A linter establishes that the configured lint rules passed on the files it examined.
- A type checker establishes that the configured type analysis completed successfully.
- A focused test establishes behavior for its cases and environment.
- A production deployment check establishes something else entirely.

Write that scope next to the gate list when it is easy to misunderstand. This prevents the familiar failure mode where an agent says "all tests pass" after it ran one targeted test while the full suite still fails.

For AI-agent verification, logs also help answer a more basic question: did the agent execute the command it claimed to execute? Require the command ledger in the same change review. A reviewer should not have to reconstruct command history from prose or screenshots.

{{< details summary="Do not overwrite logs on rerun" >}}
Give each audit its own timestamped directory. Overwriting `test.log` with a later green run hides the earlier failure and removes sequence information. A later success may be enough to proceed, but it does not change what happened before it.
{{< /details >}}

## Design rollback before the resumed run gets creative

Rollback is easiest when the starting state is named before the next mutation. At minimum, capture the starting `HEAD` SHA and preserve patches for staged and unstaged changes. That gives you two different recovery tools:

- If the starting tree was clean, return to the recorded commit with the repository's approved reset or revert workflow.
- If the starting tree already contained work, use the captured patches and a separate branch or worktree. Do not run a destructive reset and hope the earlier local changes were somewhere in the agent transcript.

There is no single safe Git command for every repository state. `git reset --hard` discards uncommitted changes. That may be correct in a disposable worktree and destructive in a developer's branch. Write the rollback command only after inspecting the capture.

A practical rollback record looks like this:

```text
Starting HEAD: 8d4f... (recorded in head-sha.txt)
Starting tree: dirty; preserve working-tree.patch and index.patch
Rollback plan: create a new worktree at Starting HEAD, apply patches there,
then compare the resumed-run diff against that worktree before discarding anything.
```

The record can be plain text because it is an instruction for the next person. Include the conditions that make it safe. "Reset to HEAD" is not a rollback plan when HEAD moved after the audit.

![A reversible repository checkpoint for safe rollback](/img/audit-agent-resume-3.png)

If the agent has already made a bad follow-up edit, stop expanding the patch. Capture a second boundary, compare it with the first, and decide whether to revert a narrow commit, restore specific paths, or abandon the worktree. More changes rarely make an uncertain state easier to audit.

## How to verify this advice

Test the procedure on a deliberately dirty branch before adopting it as team policy. Create one staged change, one unstaged change, and one untracked fixture, then run the snapshot script and confirm that each state appears in its own evidence artifact. Leave one focused test failing, capture the command ledger, and verify that the log remains available after a later successful rerun. Finally, rehearse the rollback record in a separate worktree: restore the recorded starting commit, apply the captured patches there, and compare the result before discarding anything from the original tree.

## What you should do Monday morning

Pick one repository where coding agents already make edits. Do not begin with a platform rollout. Add a small `.agent-evidence/` entry to `.gitignore` if the artifacts should stay local, or decide that the evidence directory belongs in review. Then implement these steps:

1. Add the snapshot script and run it once against a deliberately dirty working tree. Confirm that staged, unstaged, and untracked files appear in separate evidence files.
2. Choose three commands that represent your repository's minimum safety check. Put them in `.agent-audit.yml` and run them through the command ledger wrapper.
3. Write a one-paragraph resumed-agent prompt that prohibits mutations until it reports on the captured evidence.
4. Test the failure path: leave one failing test in place, capture the boundary, and verify that the log remains available after a later successful run.
5. Document one rollback path for a clean tree and one for a dirty tree. Have another developer read it without the original transcript.

The goal is not to create bureaucracy around every terminal command. The goal is to make interruption cheap. When a session resumes, the repository should provide enough evidence to decide what happens next without asking a language model to reconstruct history from its own words.

## Further reading

- Anthropic, [Work with sessions in Claude Code](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-sessions), for `--continue` and resumption by session ID or name.
- Anthropic, [Claude Code hooks reference](https://docs.anthropic.com/en/docs/claude-code/hooks), for `SessionStart` and other lifecycle hooks.
- Anthropic, [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference), for command-line options and usage.
- Zemna, [AI agent operations](/ai-agent-operations/), for operational practices around agent-run work.
- Zemna, [Developer tools](/developer-tools/), for tools that support a reviewable development workflow.
- Zemna, [Start here](/start-here/), for the broader engineering guide.
