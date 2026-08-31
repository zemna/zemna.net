---
title: "Long-Running AI Agents — From Demos to Production"
date: 2026-06-19T07:00:00+07:00
lastmod: 2026-08-31T07:00:00+07:00
draft: false
slug: "long-running-ai-agents-from-demos-to-production"
description: "A long-running coding agent can stay green after it changes directory. Production still needs a sandbox that survives /cd, a budget that counts nested work, and a human who owns both."
topics: ["ai-agents", "software-engineering", "devops", "llm"]
tags: ["coding-agents", "sandbox", "long-running-agents", "token-budget", "mcp", "code-review"]
cover: /covers/long-running-agents.png
seo:
  primaryQuery: "long-running ai agents"
  secondaryQueries:
    - "sandbox after cd coding agent"
    - "nested subagent token budget"
    - "coding agent sandbox must survive directory change"
---

The session was still green. The agent had typed `cd backend`, kept editing files, and wrote "done" in the log. Nobody on the ticket could say whether the sandbox moved with the working directory.

That is the failure I now refuse. A long-running agent is not production because it stayed up overnight. It is production when the boundary still holds after a directory change, after a nested helper spends tokens, and after a tool result is rewritten before the model sees it.

The question is not whether this demos well. The question is whether it survives maintenance, handoff, and the next person who has to roll the branch back.

<!--more-->

![Three facts on the ticket: cwd, sandbox root, named owner](/img/long-running-agents-1.png)

## The four failure modes still show up

Anthropic's write-up on long-running agent harnesses named four failure modes that keep repeating once a job outlives a single context window. The agent tries to one-shot too much. It leaves buggy or undocumented state. It marks features done before the app actually works. It burns a session figuring out how to run the project. [Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]

Those are still true on this desk. I had an agent that was supposed to finish an authentication module over a weekend. By Monday it had committed often, declared the feature done more than once, and left `npm start` broken. The git log looked busy. The app did not run.

The newer failure is quieter. The session does not crash. The checklist is green. The agent changed directory, spawned a helper, or accepted a tool payload that an extension already rewrote. The human reading the PR thinks the original sandbox and the original budget still apply. They do not.

{{< note type="warning" title="Green is not the boundary" >}}
A green long-running session can still be unsafe. Treat cwd, sandbox root, nested token spend, and the tool payload the model actually saw as four separate facts. If any one is missing, the run is not done.
{{< /note >}}

## A green session is not a surviving sandbox

I used to treat the sandbox as a start-of-session setting. Workspace root, network off unless named, writes only under the repo. Then the agent ran `cd` into a nested app folder because the Laravel package lived there. The next shell command ran with a new cwd. The ticket still said "sandboxed."

That sentence is how juniors get hurt. `cd` is a normal move in a real repo. A Vue admin and a PHP API often sit in sibling folders. If the harness silently loosens the sandbox when cwd changes, the agent can read files the ticket never listed: env samples one directory up, a sibling package's secrets, a deploy script outside the app.

The owner question is simple enough to put on a card:

| Fact the ticket needs | What "green" usually means | What I actually require |
| --- | --- | --- |
| Where is cwd? | Last command succeeded | Printed after every `cd` |
| Where is the sandbox root? | Session started in the repo | Same root as the ticket, or a named change |
| Who approved a weaker sandbox? | Nobody; it just happened | A named human, or the run stops |
| What did the model see from the tool? | The MCP server returned JSON | The payload after any rewrite, hashed |

I do not let `/cd` weaken the sandbox. If the working directory moves, the restriction stays at least as tight as the ticket. If the harness cannot prove that, I stop the run. Abort is not stop: abort still needs a retry owner, a next time, and an artifact. I already ranked that refusal in [Five Things I Refused This Week](/blog/five-refusals-this-week/). This page is the long-running version of the same desk rule.

One product note, as evidence, not as the title. On 29 August 2026 the Codex CLI stable line recorded a fix that **preserved restored permission profiles and prevented `/cd` from weakening sandbox restrictions**. The same notes said nested subagent tokens count toward root goal budgets, and that extensions can inspect or replace MCP tool results before they reach the model. [Source: https://github.com/openai/codex/releases/tag/rust-v0.151.0]

I do not pin a vendor tag on the ticket because a changelog shipped. I pin the behavior: cwd change must not open the house.

![After cd: keep the same sandbox or stop](/img/long-running-agents-2.png)

## Who owns the sandbox after `/cd`

Put a name on the ticket before the agent starts. The name is not "the agent." The name is not "Auto." The name is the person who will revert the branch.

I keep a small fixture in the repo so a one-year developer can run it without learning a vendor's internals. It records cwd and a declared sandbox root after a directory change. If cwd leaves the root, the fixture fails. If someone later loosens the root, git blame has a file to point at.

```bash {linenos=inline,hl_lines=[12,"18-21"]}
#!/usr/bin/env bash
# scripts/assert-sandbox-after-cd.sh
set -euo pipefail

SANDBOX_ROOT="$(git rev-parse --show-toplevel)"
TARGET="${1:-.}"

cd "$TARGET"
CWD="$(pwd -P)"
ROOT="$(cd "$SANDBOX_ROOT" && pwd -P)"

case "$CWD/" in
  "$ROOT"/*) ;;
  *)
    echo "SANDBOX_FAIL cwd=$CWD root=$ROOT" >&2
    exit 2
    ;;
esac

echo "SANDBOX_OK cwd=$CWD root=$ROOT"
```

Run it the way a junior actually runs it: from the repo root, then after the agent moves into the app folder.

```bash
chmod +x scripts/assert-sandbox-after-cd.sh
./scripts/assert-sandbox-after-cd.sh
./scripts/assert-sandbox-after-cd.sh apps/api
# This must fail if apps/api is outside the git root:
# ./scripts/assert-sandbox-after-cd.sh ../other-repo
```

That script does not replace a real OS sandbox. It is the ticket artifact. If the agent `cd`s and the next command is a file read, the CI job still has to prove the path sits under `SANDBOX_ROOT`. I wire the same check into the agent instructions so the model cannot mark the step done without printing `SANDBOX_OK`.

{{< field-note title="Field note" >}}
On a Laravel + Vue desk the agent will `cd` into `apps/web` or `packages/admin` because that is where `package.json` lives. I still own the sandbox at the git root. Nested folders do not earn extra file reads. If the harness cannot keep the original restriction after `cd`, I stop the session and put a human on the retry. The artifact is `SANDBOX_OK` plus the cwd line, not a chat message that says the sandbox is fine.
{{< /field-note >}}

## Nested tokens still count on the root budget

Long-running work loves helpers. Search in one agent. Shell in another. Browser in a third. The parent looks cheap because its own meter barely moved. The bill and the context both moved in the children.

I treat nested spend as the parent's spend. If the ticket says the job has a 2 million token ceiling, helpers count. If the parent hits the ceiling by hiding work in a subagent, that is a budget bug, not a win.

```python
from dataclasses import dataclass, field


@dataclass
class Budget:
    label: str
    limit_tokens: int
    used_tokens: int = 0
    children: list["Budget"] = field(default_factory=list)

    def charge(self, tokens: int) -> None:
        if tokens < 0:
            raise ValueError("tokens must be >= 0")
        self.used_tokens += tokens
        if self.total_used() > self.limit_tokens:
            raise RuntimeError(
                f"{self.label} over budget: {self.total_used()} > {self.limit_tokens}"
            )

    def total_used(self) -> int:
        return self.used_tokens + sum(child.total_used() for child in self.children)


def test_nested_helper_counts_on_root() -> None:
    root = Budget("ticket-4721", limit_tokens=1000)
    search = Budget("search-helper", limit_tokens=1000)
    root.children.append(search)
    root.charge(100)
    search.charge(950)
    try:
        root.charge(1)
        raise AssertionError("root should be over budget")
    except RuntimeError as exc:
        assert "over budget" in str(exc)
        assert root.total_used() == 1051
```

The test is the contract I want on Monday. A dashboard that only charts the parent will lie. Same shape as [A Green Cron Exit Is Not a Finished Job](/blog/a-green-cron-exit-is-not-a-finished-job/): the process can look healthy while the work is not.

I already refuse letting the agent pick its own model. Nested helpers make that worse, because the helper often inherits Auto or a "faster" default. The ticket still names the author model and the review model. Details live in [I Do Not Let a Coding Agent Pick Its Own Model](/blog/coding-agent-model-owner/).

## If an extension rewrote the MCP result, the model did not see the tool

Tool output is now a place people plug formatters, redactors, and "helpful" rewrites. That can be good: strip a secret, shrink a huge JSON blob. It can also be a silent lie. The MCP server returned one payload. The model answered a different one.

I keep the raw bytes. Then I keep the bytes after the rewrite. Then I hash both. If the model is going to act, the ticket stores the hash it acted on.

```python
import hashlib
import json
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def record_tool_payload(
    artifact_dir: Path,
    tool_name: str,
    raw: bytes,
    after_rewrite: bytes,
) -> dict[str, str]:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    raw_path = artifact_dir / f"{tool_name}.raw.json"
    seen_path = artifact_dir / f"{tool_name}.seen.json"
    raw_path.write_bytes(raw)
    seen_path.write_bytes(after_rewrite)
    record = {
        "tool": tool_name,
        "raw_sha256": sha256_bytes(raw),
        "seen_sha256": sha256_bytes(after_rewrite),
        "rewritten": str(raw != after_rewrite).lower(),
    }
    (artifact_dir / f"{tool_name}.meta.json").write_text(
        json.dumps(record, indent=2) + "\n",
        encoding="utf-8",
    )
    return record


def test_rewrite_is_visible() -> None:
    raw = b'{"rows":[1,2,3]}'
    seen = b'{"rows":[1,2]}'
    record = record_tool_payload(Path("/tmp/tool-artifacts"), "db.query", raw, seen)
    assert record["rewritten"] == "true"
    assert record["raw_sha256"] != record["seen_sha256"]
```

If `rewritten` is true, a human has to say that was the point (secret redaction) or a bug (rows dropped). The model does not get to shrug. This is the same family as empty tool output: missing bytes are not success. They are an interrupt, or they are a named filter.

Stale permission is the sibling bug. Someone approved a broader grant two hours ago. Then the ticket tightened the sandbox. The session kept the old grant in memory and used it after the policy change. From the chat it still looks like the same run. From the filesystem it is a different contract.

I treat a permission change as a new session. The agent does not inherit yesterday's yes. The artifact is a fresh grant line with a timestamp after the policy edit. If that line is missing, the run stops. This is cheaper than explaining a leaked `.env` in Slack.

On the Laravel SaaS repos I actually ship, the dangerous path is almost never "the model invented a new framework." It is `cd` into `packages/admin`, a helper that reads `../.env.example` because the sandbox followed cwd, and a nested search agent that burned the parent budget while the parent still looked cheap. The fix is names and files, not a pep talk.

![Nested helper tokens still count on the parent budget](/img/long-running-agents-3.png)

## Initializer, then worker, then git

The harness pattern that still works is the one Anthropic described: an initializer that does not write product code, then a worker that takes one feature at a time. The initializer leaves a feature list, an `init.sh` that can start the app, and a progress file the next session is forced to read. [Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]

```yaml
# initializer-agent.yaml
role: |
  You are an initializer agent. Read the repo. Do not write product code.
  Write only:
  1. Files to create (paths)
  2. Files to modify (what changes)
  3. Test strategy
  4. Dependencies to install
  5. Risk areas
  6. Sandbox root and the cwd the worker is allowed to use

context:
  - Full project structure
  - Existing test patterns
  - Current stack docs
```

Every meaningful worker step still ends in a git commit. Not as decoration. As the recovery unit. When the agent goes off the rails, I bisect the diff. I do not debug the chat.

```bash
git add -A
git commit -m "feat(auth): add JWT token generation

- RS256 signing with rotating keys
- Expiry 24h plus refresh
- Tests: 12 passing, 0 failing
- SANDBOX_OK cwd=... root=...
- BUDGET_USED=..."
```

I keep the agent on a branch. Main stays mergeable. If step 7 of 12 is bad, I revert step 7. I do not throw the weekend away.

The Faros 2026 engineering report, built from telemetry on 22,000 developers across 4,000 teams, named the pattern **acceleration whiplash**: volume is up, quality is down, and the gap widens as adoption deepens. In that dataset, 80% of teams were already past a 50% weekly-active-user line for AI tools. PR size was up 51%. Median review time was up 5x. Incidents per PR were up 3x. [Source: https://www.faros.ai/blog/ai-acceleration-whiplash-takeaways] [Source: https://www.faros.ai/research]

That is why one-feature-then-verify still wins. Generating the next file is cheap. Reviewing it is not. Cheap code still needs a human review. I do not let the same model grade its own diff.

## Context is a ration, not a warehouse

A five-minute prompt can hold the whole problem. A three-day agent cannot. I pass a manifest: files, docs, previous artifacts. The agent does not get to wander the monorepo "just in case."

Three modes I actually use:

1. **Accumulate** for planning. History is the point.
2. **Last plan only** for implementation. Old analysis is noise.
3. **Explicit files** for review. Extra files invent extra couplings.

End-to-end checks stay outside the agent. Unit tests can pass while the login page is blank. A browser, or a Playwright script a human wrote, is the judge. The agent does not write the contract it is graded on.

```typescript
import { chromium } from "playwright";

async function verifyAuthFlow() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto("http://localhost:3000/register");
  await page.fill("#email", "test@example.com");
  await page.fill("#password", "securePassword123");
  await page.click("#submit");
  await page.waitForURL("/dashboard");

  const cookies = await page.context().cookies();
  const token = cookies.find((c) => c.name === "auth_token");
  if (!token) {
    throw new Error("No auth token after registration");
  }

  const response = await page.goto("http://localhost:3000/api/protected");
  if (response?.status() !== 200) {
    throw new Error("Protected route inaccessible after auth");
  }

  await browser.close();
  return { passed: true, steps: 3 };
}
```

If this fails, "done" is revoked. No speech from the agent undoes a failed browser check. That is also how I treat a missing `SANDBOX_OK` line.

## What I would still build first

If I were starting the same long-running setup again, I would not begin with a bigger model. I would begin with four boring files:

1. Initializer vs worker. Planning and doing stay split.
2. Git as the timeline. Every step is a commit with sandbox and budget lines in the message.
3. Human gates at feature boundaries. The agent proposes. A named person merges. See the merge refusal in [Five Things I Refused This Week](/blog/five-refusals-this-week/).
4. A sandbox fixture that survives `cd`, plus a budget that includes helpers.

The agents that last across days are not smarter than the ones that last across minutes. They are wrapped in checks the agent cannot talk past. Hub notes for this desk live under [AI agent operations](/ai-agent-operations/). New readers can start at [Start here](/start-here/).

## What you should do Monday morning

1. Write the sandbox root on the ticket. One path. One named human.
2. Add `scripts/assert-sandbox-after-cd.sh` and run it after every agent `cd`. Fail the job if cwd leaves the root.
3. Count nested helper tokens on the parent budget. If you cannot see helper spend, you do not have a budget.
4. Store raw tool payloads and the bytes the model saw. If they differ, a human says why.
5. Stop the run when any of those artifacts is missing. Chat text is not an artifact.

## Further reading

- {{< source href="https://github.com/openai/codex/releases/tag/rust-v0.151.0" label="Codex CLI notes: sandbox after /cd, nested tokens, MCP rewrite" >}}
- {{< source href="https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents" label="Anthropic — Effective harnesses for long-running agents" >}}
- {{< source href="https://www.faros.ai/blog/ai-acceleration-whiplash-takeaways" label="Faros — AI acceleration whiplash takeaways" >}}
- [A green cron exit is not a finished job](/blog/a-green-cron-exit-is-not-a-finished-job/)
- [Five things I refused this week](/blog/five-refusals-this-week/)
