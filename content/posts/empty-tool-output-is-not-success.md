---
title: "Empty Tool Output Is Not Success Until the Harness Says Interrupted"
date: 2026-08-26T07:00:00+07:00
draft: false
slug: "empty-tool-output-is-not-success"
description: "An interrupted MCP tool in a headless coding-agent session used to look finished. Treat empty completion as a bug until the harness asserts an interrupted error."
topics: ["tutorials"]
tags: ["coding-agents", "mcp", "verification", "headless", "claude-code", "silent-failure", "harness"]
cover: /covers/empty-tool-output-is-not-success.png
seo:
  primaryQuery: "headless coding agent MCP interrupt empty output"
  secondaryQueries:
    - "MCP tool completed with no output interrupted"
    - "Claude Code headless MCP interrupt harness"
    - "coding agent silent success empty tool result"
---

The cron row is green. The JSONL says the MCP tool finished. The stdout field is empty.

That is the most expensive sentence a headless coding agent can write. The next step is invented. The PR lands. The Laravel worker image still talks to last week's schema. Nobody owns the rollback because the transcript never recorded a failure.

Anthropic's Claude Code notes for **25 August 2026** (tag `v2.1.246`, published `2026-08-25T22:31:43Z`) name the lie in one line: MCP tool calls interrupted by an incoming message in headless and remote sessions were reported to the model as **"completed with no output"** instead of an explicit interrupted error. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.246]

The question is not whether a new tag demos well. It is whether your harness still treats empty completion as a close.

<!--more-->

![Completed-empty is not the same as interrupted](/img/empty-tool-output-is-not-success-1.png)

## Empty completion is a contract, not a vibe

I run scheduled coding-agent work the same way I run a Laravel queue: the process is not the product. The product is a named side effect plus a proof artifact. [A green cron exit is not a finished job](/blog/a-green-cron-exit-is-not-a-finished-job/) already covers Unix `exit 0` with stale work. This post is the sibling case that lives **inside** the agent turn: the tool result looks done, the payload is empty, and the model keeps writing.

Official Claude Code headless docs are blunt about process exit: `claude -p` exits `0` on success and non-zero when the run fails. Invalid flags go to stderr before the run starts. Failures inside the run, such as missing authentication, print as the result on stdout. [Source: https://code.claude.com/docs/en/headless]

That is a process contract. It is not a tool-result contract.

An interrupted MCP call that is rewritten as "completed with no output" satisfies the process contract. The parent cron still sees `0`. The model still sees a finished tool. The only missing thing is the work.

{{< note type="warning" title="Do not parse emptiness as success" >}}
Empty stdout is a legal MCP result for some tools. It is also the historical lie for an interrupt. The harness has to classify **why** the result is empty: interrupted, schema-coerced, max-turns partial, or a real empty success with a proof artifact.
{{< /note >}}

The same tag also fixed a quieter cousin: a command interrupted mid-run showing as **"Ran 1 shell command"** with no sign it was cut. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.246] If your reviewer only reads the summary line, both lies look identical.

## What the 25 August notes actually changed

Do not turn this into a version table. Pin four neighboring behaviors from the same official body. They are the reasons a "tool finished" line is still not enough.

| Signal the model used to see | Official repair in the same tag | Harness rule |
|---|---|---|
| Interrupted MCP call → "completed with no output" | Explicit interrupted error | Fail the turn unless `status=interrupted` |
| Empty-schema MCP args (`{}`) sent as JSON strings | Sent as their real type | Assert argument type, not `typeof string` |
| Subagent hits `maxTurns` and looks finished | Result marked **partial**, hint to continue via `SendMessage` | Reject unmarked "done" at the turn cap |
| Background session fails closed after 45s | Open after deleted start dir, sleep, or slow host | Treat a missing session as fail-closed, not skip |

[Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.246]

Two more lines from the same notes matter for CI:

- Non-interactive sessions (`-p`, SDK, cloud) now automatically continue a response cut off mid-stream by a server error, connection loss, or stall, instead of ending with an error.
- Telemetry and metrics requests to Anthropic no longer carry the API key configured for a third-party gateway (`ANTHROPIC_BASE_URL`); a credential is sent only to its own host.

The first line is a resilience change. It is **not** permission to treat a later empty tool result as success. Automatic continue can hide a stall. The harness still has to name the last tool status.

The second line is a secret-routing change. It is not today's fixture, but it is a reminder that "the vendor patched it" is not the same as "your wrapper stopped shipping the old header."

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.246" label="Claude Code release notes — v2.1.246" >}}

![Harness board: interrupt, string args, partial turns, fail-closed](/img/empty-tool-output-is-not-success-2.png)

## Headless mode is where the lie used to hide

Interactive terminals have a human. Headless does not.

Claude Code's current headless page is the source of record for scripted runs. The primary switch is `-p` / `--print`. Combine it with `--allowedTools`, `--output-format`, `--mcp-config`, `--strict-mcp-config`, and `--max-turns`. `--bare` skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and `CLAUDE.md`. Without `--bare`, a `-p` session loads the project's `.mcp.json` with **no workspace trust dialog and no per-server approval prompt**. [Source: https://code.claude.com/docs/en/headless]

That last sentence is why a Laravel/Vue repo with a leftover `.mcp.json` is a production surface, not a toy.

Official notes on stop signals are equally specific. SIGTERM on a `-p` run exits **143**. The in-progress turn is left unfinished and records no result. SIGINT, or the Agent SDK `interrupt()`, ends the turn instead. On SIGTERM, Claude Code kills the Bash process tree, runs `SessionEnd` hooks, and starts no new tool call. [Source: https://code.claude.com/docs/en/headless]

So you already have two different "stopped" shapes:

1. **OS stop:** exit 143, no result recorded.
2. **In-turn interrupt of an MCP tool:** used to look like a completed empty tool.

If your wrapper only checks the process code, case 2 never exists.

The same docs tell you how to fail CI when a plugin or MCP server does not load. From **v2.1.221**, `-p` with `--mcp-config` waits for still-pending servers before the first turn, up to `MCP_TIMEOUT` (default **30 seconds**). A remote server with a cached tool list can show `pending` in `system/init` and connect on first tool call. From **v2.1.219**, skipped `--mcp-config` entries land in `mcp_server_errors`. If you redirect stderr, the startup warning is gone and that array is the only signal. [Source: https://code.claude.com/docs/en/headless]

A server that never loaded plus a model that still writes "I called the tool" is the same family as empty completion. Different layer. Same ownership.

{{< details summary="Headless flags that belong in the fixture, not in a changelog tweet" >}}
- `-p` / `--print` — non-interactive.
- `--bare` — no surprise MCP from the laptop profile.
- `--mcp-config` + `--strict-mcp-config` — only the servers you named.
- `--output-format json` or `stream-json` — machine-readable status.
- `--max-turns` — hard ceiling; pair with the partial-result rule.
- `MCP_TIMEOUT` — startup wait, not a tool-result timeout.
{{< /details >}}

## A fixture that refuses the empty-success story

I do not want another dashboard. I want a file the next engineer can run on Monday.

The fixture below is a **classifier**, not a Claude Code mock. It takes a captured tool event and decides whether the turn is allowed to continue. Put it in the repo that owns the cron. Pin the event shape your wrapper actually writes. Do not invent vendor-internal fields.

```python {linenos=inline,hl_lines=[18,24,31]}
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


Status = Literal["ok", "interrupted", "partial", "empty_unproven", "type_coercion"]


@dataclass(frozen=True)
class ToolEvent:
    name: str
    is_mcp: bool
    reported_status: str
    stdout: str
    stderr: str
    args: Any
    schema: dict[str, Any] | None
    hit_max_turns: bool
    proof_path: str | None


def classify_tool_event(event: ToolEvent) -> Status:
    reported = event.reported_status.lower()
    if reported in {"interrupted", "aborted", "cancel", "cancelled"}:
        return "interrupted"
    if event.hit_max_turns and reported in {"ok", "completed", "done", ""}:
        return "partial"
    if event.is_mcp and event.schema == {} and isinstance(event.args, str):
        return "type_coercion"
    empty = event.stdout.strip() == "" and event.stderr.strip() == ""
    if empty and reported in {"ok", "completed", "done", ""}:
        if event.proof_path:
            return "ok"
        return "empty_unproven"
    return "ok"


def allow_next_step(status: Status) -> bool:
    return status == "ok"
```

The rule that matters is line 31: empty + "completed" without a proof path is **not** `ok`. A real empty success has to bring a side-effect receipt — a written file, a ticket id, a `releaseURL`, a database row count. That is the same artifact rule as [background-agent recovery](/blog/building-a-background-agent-recovery-cli-the-three-gate-check/).

Wire the classifier into a pytest that names the interrupt case first.

```python
from pathlib import Path

from harness_classify import ToolEvent, classify_tool_event


def test_interrupted_mcp_is_never_empty_success():
    event = ToolEvent(
        name="mcp__tracker__create_ticket",
        is_mcp=True,
        reported_status="completed",
        stdout="",
        stderr="",
        args={"title": "bump lockfile"},
        schema={"type": "object"},
        hit_max_turns=False,
        proof_path=None,
    )
    assert classify_tool_event(event) == "empty_unproven"


def test_explicit_interrupt_fails_closed():
    event = ToolEvent(
        name="mcp__tracker__create_ticket",
        is_mcp=True,
        reported_status="interrupted",
        stdout="",
        stderr="incoming message interrupted the tool",
        args={"title": "bump lockfile"},
        schema={"type": "object"},
        hit_max_turns=False,
        proof_path=None,
    )
    assert classify_tool_event(event) == "interrupted"


def test_empty_schema_string_args_are_coercion():
    event = ToolEvent(
        name="mcp__notes__append",
        is_mcp=True,
        reported_status="ok",
        stdout="wrote",
        stderr="",
        args='{"text":"hello"}',
        schema={},
        hit_max_turns=False,
        proof_path=None,
    )
    assert classify_tool_event(event) == "type_coercion"


def test_max_turns_done_is_partial():
    event = ToolEvent(
        name="explore",
        is_mcp=False,
        reported_status="done",
        stdout="still reading files",
        stderr="",
        args={},
        schema=None,
        hit_max_turns=True,
        proof_path=None,
    )
    assert classify_tool_event(event) == "partial"


def test_proven_empty_stdout_can_pass(tmp_path: Path):
    receipt = tmp_path / "ticket.json"
    receipt.write_text('{"id":"T-19"}', encoding="utf-8")
    event = ToolEvent(
        name="mcp__tracker__create_ticket",
        is_mcp=True,
        reported_status="completed",
        stdout="",
        stderr="",
        args={"title": "bump lockfile"},
        schema={"type": "object"},
        hit_max_turns=False,
        proof_path=str(receipt),
    )
    assert classify_tool_event(event) == "ok"
```

If you only keep one test, keep the first. That is the screenshot a peer actually uses.

![Incoming message, tool cut, then classify](/img/empty-tool-output-is-not-success-3.png)

## Wrap `claude -p` so CI cannot swallow the lie

A classifier without a wrapper is a blog comment. The wrapper has to fail the job.

Official JSON output from `-p --output-format json` includes a text `result` plus session metadata. Official docs also say a SIGTERM run records no result. [Source: https://code.claude.com/docs/en/headless] Your wrapper therefore treats a missing result the same way it treats `empty_unproven`.

```bash {linenos=inline,hl_lines=[22,28]}
#!/usr/bin/env bash
# scripts/run-headless-agent.sh
set -euo pipefail

PROMPT=${1:?usage: run-headless-agent.sh "<prompt>"}
OUT=${AGENT_OUT:-/var/lib/agent-runs/last.json}
MCP_CONFIG=${MCP_CONFIG:-./.ci/mcp.json}

mkdir -p "$(dirname "$OUT")"

set +e
claude --bare -p "$PROMPT" \
  --mcp-config "$MCP_CONFIG" \
  --strict-mcp-config \
  --output-format json \
  --max-turns "${MAX_TURNS:-8}" \
  --allowedTools "Read,Bash" \
  >"$OUT"
CODE=$?
set -e

if [[ "$CODE" -eq 143 ]]; then
  echo "headless run received SIGTERM; turn unfinished" >&2
  exit 1
fi

if [[ "$CODE" -ne 0 ]]; then
  echo "headless process failed: $CODE" >&2
  exit "$CODE"
fi

python3 scripts/assert_tool_events.py "$OUT"
```

`assert_tool_events.py` is the thin reader. It does not re-implement Claude Code. It walks whatever tool events your team already persists — JSONL transcript, `stream-json` lines, or a wrapper log — and calls `classify_tool_event`.

```python
import json
import sys
from pathlib import Path

from harness_classify import ToolEvent, allow_next_step, classify_tool_event


def load_events(path: Path) -> list[ToolEvent]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    events = []
    for item in raw.get("tool_events", []):
        events.append(
            ToolEvent(
                name=item.get("name", ""),
                is_mcp=bool(item.get("is_mcp")),
                reported_status=str(item.get("status", "")),
                stdout=str(item.get("stdout", "")),
                stderr=str(item.get("stderr", "")),
                args=item.get("args"),
                schema=item.get("schema"),
                hit_max_turns=bool(item.get("hit_max_turns")),
                proof_path=item.get("proof_path"),
            )
        )
    return events


def main() -> int:
    path = Path(sys.argv[1])
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not payload.get("result"):
        print("missing result field after a zero exit", file=sys.stderr)
        return 2
    events = load_events(path)
    if not events:
        print("zero tool events with a completion claim", file=sys.stderr)
        return 2
    for event in events:
        status = classify_tool_event(event)
        if not allow_next_step(status):
            print(f"{event.name}: {status}", file=sys.stderr)
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If your current `claude -p` JSON blob does not yet include `tool_events`, stop pretending the vendor schema is the harness. Write the events yourself from `stream-json` as the run proceeds. Official stream mode emits newline-delimited events and ends with a `result` message. [Source: https://code.claude.com/docs/en/headless] Persist each `tool_use` / `tool_result` pair. Then classify.

This is the same pattern we already use for Postiz: a `success: true` create is not a published post until `/posts` readback names the state. QUEUE after a matching create is async lag. Empty completion after an interrupt is not lag. It is a wrong status.

{{< field-note title="Field note" >}}
On scheduled jobs that touch Laravel SaaS checkouts, I treat an MCP side effect the same way I treat a queue job: the git diff is not the receipt. If the tracker, the deploy hook, or the Postiz create call returns empty stdout with status `completed`, the next prompt will invent the ticket id and keep writing. The fix is a fail-closed classifier plus a proof file on disk. Same rule as [zombie detection](/blog/your-ai-agent-pipeline-has-no-zombie-detection-heres-how-to-add-it/): monitor the side effect, not the spinner.
{{< /field-note >}}

## Neighboring lies in the same family

The interrupt fix is one member of a set. Treat the others as the same Monday checklist, not as extra news.

**1. Empty schema, stringified args.** The official notes say MCP arguments were sent as JSON strings when the parameter schema was `{}`. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.246] A server that does `int(args["limit"])` then throws, or worse, concatenates the quotes into a query. Your fixture already returns `type_coercion`. Keep a golden request log.

**2. `maxTurns` that looks finished.** A subagent that stops at its turn cap now returns output marked partial, with a hint to continue via `SendMessage`. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.246] If your orchestrator still promotes "the child said done" into a merge, you will ship a half-read of the repo. Official `--max-turns` on `-p` is a hard ceiling with no default. [Source: https://code.claude.com/docs/en/cli-reference]

**3. Bash allow rules that match options.** A startup warning now fires for rules with a wildcard before the subcommand, such as `Bash(git * main)`, because they also match options inserted before the subcommand. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.246] This is permission drift, not an MCP interrupt, but it is the same class of "the policy text is not the policy." Official headless docs already warn that `Bash(git diff *)` needs the space before `*`; without it, `git diff-index` matches. [Source: https://code.claude.com/docs/en/headless]

**4. Historical silent `-p` + HTTP MCP.** GitHub issue **#32191** (opened 8 March 2026) reports `claude -p` with an HTTP MCP server exiting **0** with no stdout and no stderr, while stdio MCP worked. [Source: https://github.com/anthropics/claude-code/issues/32191] That issue is older than this week's tag. Do not claim 2.1.246 closed it. Do claim this: exit 0 plus empty output is a known failure shape on this CLI, and your wrapper already has to reject it.

![Four neighboring failure shapes: interrupt lie, string args, partial done, exit zero empty](/img/empty-tool-output-is-not-success-4.png)

## Who owns rollback when the model already wrote the next file

A harness that only prints "interrupted" still loses if the model already edited the tree.

Give the turn a lease:

1. **Worktree or branch name** owned by the job id.
2. **Proof directory** that must contain either a receipt or an interrupt marker.
3. **Named human** who can revert the branch if the marker is interrupt and the diff is non-empty.

That is change control. It is the same ownership sentence as a lockfile bump: the bump is not done when npm prints a version. It is done when a person can roll it back. Strategy this week banned version-pin posts for a reason. The useful artifact is the owner, not the tag.

On the agent-ops hub I keep this as a one-line policy: [AI agent operations](/ai-agent-operations/) is a verification problem first. Model quality is downstream.

```text
job: 2026-08-26-headless-ticket
branch: agent/2026-08-26-headless-ticket
owner: oncall-backend
proof:
  - required: proofs/2026-08-26-headless-ticket.json
  - on_interrupt: revert branch, keep proof
  - on_empty_unproven: revert branch, page owner
```

If that YAML feels heavy, write three lines in the cron comment. The name is the point.

## What you should do Monday morning

1. **Capture one real headless transcript** from a job that uses MCP. If you have none, run `claude --bare -p` against a dummy MCP that sleeps, then send SIGINT. Keep the file.
2. **Add `classify_tool_event` and the five tests** to the repo that owns the cron, not to a gist.
3. **Fail CI on `empty_unproven`, `interrupted`, `partial`, and `type_coercion`** unless a human-signed override file exists for that job id.
4. **Require a proof path** for any MCP tool whose success is a side effect (ticket, deploy, Postiz post, database write).
5. **Name the rollback owner** on the job record. If the model wrote files after an interrupt, revert the branch before the next prompt.
6. **Re-read the official v2.1.246 body** before you tell the team "we already patched." Your wrapper version and the CLI version are two pins.
7. **Link the fixture from `/developer-tools/`** so the next hire does not rediscover empty completion as a personality quirk of the model.

## Further reading

- {{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.246" label="Claude Code v2.1.246 release notes — interrupted MCP, partial maxTurns, argument types" >}}
- {{< source href="https://code.claude.com/docs/en/headless" label="Claude Code docs — run programmatically with -p, SIGTERM 143, MCP startup fields" >}}
- {{< source href="https://github.com/anthropics/claude-code/issues/32191" label="GitHub issue 32191 — claude -p + HTTP MCP silent exit 0" >}}

Related on this site: [A green cron exit is not a finished job](/blog/a-green-cron-exit-is-not-a-finished-job/), [zombie detection](/blog/your-ai-agent-pipeline-has-no-zombie-detection-heres-how-to-add-it/), [background-agent recovery CLI](/blog/building-a-background-agent-recovery-cli-the-three-gate-check/), [Start here](/start-here/).
