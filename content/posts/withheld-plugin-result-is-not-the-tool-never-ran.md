---
title: "A Withheld Plugin Result Is Not the Tool Never Ran"
date: 2026-10-10T07:00:00+07:00
draft: false
slug: "withheld-plugin-result-is-not-the-tool-never-ran"
description: "A denied tool with no result in chat is not proof the tool never ran. Print withheld plugin result versus never ran versus the named Claude Code owner before you file the wrong ticket."
topics: ["ai-agents"]
tags: ["claude-code", "plugins", "permissions", "coding-agents", "change-control", "post-tool-use"]
cover: /covers/withheld-plugin-result-is-not-the-tool-never-ran.png
seo:
  primaryQuery: "claude code withheld plugin result not the tool never ran"
  secondaryQueries:
    - "claude code mod denies tool after it ran"
    - "PostToolUse withhold tool result vs skipped tool"
    - "named owner for claude code never-ran tickets"
---

The junior pastes a chat. The agent asked for `Bash(git status)`. A plugin line then says Denied. The tool result is empty. They file the ticket: “the tool never ran. always-ask blocked it.”

I stop the run there. A withheld plugin result is not the tool never ran. Claude Code’s public notes that named this field are blunt: when a mod denies a tool call after the tool ran, Claude and you now read that the tool ran and a plugin withheld its result. The tool executed. The result was held. The empty pane is not a skip. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.295] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a UNC path read as a local allow in [A UNC Path Read Is Not a Local Allow](/blog/unc-path-read-is-not-a-local-allow/), a leftover `allowed-tools` rule as you still in plan mode in [A Leftover Allowed-Tools Rule Is Not You Still in Plan Mode](/blog/leftover-allowed-tools-is-not-plan-mode-stuck/), and a repeated reply ID as a second approval in [A Repeated Reply ID Is Not a Second Approval](/blog/repeated-reply-id-is-not-a-second-approval/). This post is the same desk rule for a denied tool with no result. Print withheld versus never ran. Name who owns the Claude Code answers.

The question is not whether the pane stayed empty. The question is whether the named owner can still tell a withheld plugin result from a tool that never ran.

<!--more-->

![Three columns: Withheld plugin result, Tool never ran, Named owner](/img/withheld-plugin-result-is-not-the-tool-never-ran-1.png)

## The ticket that looks like never-ran

Juniors treat a missing tool result the way they treat a skipped call. Yesterday `git status` printed in the pane. Today a mod says Denied and the pane is blank. They page the desk: “the sandbox blocked it” or “always-ask never let it start.”

Two jobs collide on that row.

1. **Keep PreToolUse and PostToolUse apart.** Official hooks page: PreToolUse fires before a tool call executes and can block it. PostToolUse fires after the tool already ran. Exit code 2 on PostToolUse still reaches Claude even though the tool already ran. `updatedToolOutput` on PostToolUse replaces the tool’s result. A deny after the call is a result problem, not a skip. [Source: https://code.claude.com/docs/en/hooks]
2. **Keep the new sentence honest.** Official changelog under the 2.1.295 heading, 8 October 2026: changed what Claude and you read when a mod denies a tool call after the tool ran — it now says the tool ran and a plugin withheld its result. That sentence is the field. It is not “the tool never ran.” It is not “deny is off.” [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.295] [Source: https://code.claude.com/docs/en/changelog]

If you only screenshot “Denied” plus an empty result, you will file never-ran. You will not file the withheld result.

{{< note type="warning" title="Do not file never-ran on a withheld plugin result" >}}
If a coding agent or a junior says the tool never ran because a plugin denied the call and the pane is empty, print whether the tool executed, whether a plugin withheld the result, and one human name on the Claude Code answers. A withheld plugin result is not the tool never ran.
{{< /note >}}

I do not invent a fake overnight outage of every plugin. I use the public contract. The withheld result is the ticket, not a version pin in the title.

## What Claude Code actually named

Read the 8 October 2026 GitHub release body, then the docs changelog under the same heading, then the hooks page that names PostToolUse. Do not trust a social recap. Do not trust this post without those pages.

The named field, published 8 October 2026:

> Changed what Claude and you read when a mod denies a tool call after the tool ran: it now says the tool ran and a plugin withheld its result

That sentence has three parts. Print all three on the ticket.

| Part | What it is | What it is not |
| --- | --- | --- |
| Tool ran | The call executed (Bash started, Read opened, Edit wrote) | Proof the pane must show stdout |
| Plugin withheld the result | A mod denied after the run and hid what the tool returned | Proof the tool was skipped |
| Named owner | The human who answers Claude Code permission rows | A coding agent, a plugin, or auto mode |

Official hooks docs keep the timing loud. PreToolUse can block the call before it starts. PostToolUse cannot un-run it. A PostToolUse hook that exits 2 still tells Claude the stderr after the tool ran. `updatedToolOutput` replaces the inbound result. Redaction and transformation belong on PostToolUse for inbound results, not on a “never started” story. [Source: https://code.claude.com/docs/en/hooks]

The miss that looks like this ticket is the opposite mix: a junior sees Denied plus no stdout and files never-ran. After 8 October 2026, the product text names the mix. Print the new sentence. Do not file a skip.

{{< details summary="Where the pin sits after the decision, not in the title" >}}
Claude Code’s public GitHub release dates this field 8 October 2026 under the v2.1.295 heading (`published_at` 2026-10-08T19:48:38Z, not a prerelease). The docs changelog lists the same bullet under `## 2.1.295`. npm `dist-tags.latest` on the morning this post shipped was 2.1.296; `dist-tags.stable` was 2.1.287; npm `time` for 2.1.295 was 2026-10-08T18:22:58.621Z. The field for this URL is the withheld-result line, not a pin in the title. Neighbor bullets in the same heading (OSC 7501, `onFailure: "block"`, disableAutoMode leftover on Desktop/SDK) are other tickets. Do not mix nested deny, leftover `allowed-tools`, or UNC reads into this heading. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.295] [Source: https://registry.npmjs.org/@anthropic-ai/claude-code]
{{< /details >}}

## Four checks before you file

A mid-senior screenshots this list. A junior who only has the chat still has a ticket they can close.

1. **Print whether the tool started.** Look for a tool call id, a process start, a file open, or a Bash pid. If the log never shows a start, the ticket is “never ran” or “PreToolUse blocked.” If it shows a start, do not file never-ran.
2. **Print withheld versus empty versus skipped.** Official release: the tool ran and a plugin withheld its result. Empty stdout after a run is not a skip. A PreToolUse block is a skip. Those are different tickets. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.295]
3. **Print PreToolUse versus PostToolUse.** Official hooks page: PreToolUse is before execute. PostToolUse is after execute. Exit 2 on PostToolUse still reaches Claude after the tool ran. Do not collapse those two events into “Denied.” [Source: https://code.claude.com/docs/en/hooks]
4. **Write one human name.** `CLAUDE_CODE_OWNER`. That name answers “is this a withheld plugin result, or did we file never-ran on a tool that executed.”

![Four checks: Tool started, Withheld vs skipped, Pre vs Post, Named owner](/img/withheld-plugin-result-is-not-the-tool-never-ran-2.png)

## Classify the row before you page the desk

Do not execute the original tool again to “prove” it. Classify the log line. The classifier below is a desk fixture. It never starts Bash. It never installs a plugin. It never hides a result.

```python {linenos=inline,hl_lines=[18,"24-32"]}
#!/usr/bin/env python3
"""Classify withheld-result vs never-ran. Never re-run the tool."""
from __future__ import annotations

from typing import TypedDict


class Ticket(TypedDict):
    this_field: bool
    ticket: str
    reason: str


def classify_row(
    tool_started: bool,
    event: str,
    plugin_withheld: bool,
) -> Ticket:
    event_name = event.strip()
    if plugin_withheld and tool_started:
        return {
            "this_field": True,
            "ticket": "withheld_plugin_result",
            "reason": "tool ran; plugin withheld the result",
        }
    if event_name == "PreToolUse" and not tool_started:
        return {
            "this_field": False,
            "ticket": "pretooluse_block",
            "reason": "call never started",
        }
    if not tool_started:
        return {
            "this_field": False,
            "ticket": "never_ran",
            "reason": "no start in the log",
        }
    return {
        "this_field": False,
        "ticket": "ran_with_visible_result",
        "reason": "tool ran and the pane still has a result",
    }


FIXTURES = [
    {"tool_started": True, "event": "PostToolUse", "plugin_withheld": True},
    {"tool_started": False, "event": "PreToolUse", "plugin_withheld": False},
    {"tool_started": True, "event": "PostToolUse", "plugin_withheld": False},
]


def main() -> int:
    for row in FIXTURES:
        out = classify_row(**row)
        print(
            f"this_field={out['this_field']} ticket={out['ticket']} {out['reason']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run that against fixtures, not against production. The first fixture is this post. The second is a PreToolUse skip. The third is a normal PostToolUse with a visible result.

Print the ticket next to the owner. Do not let the agent invent a fourth class called “deny is off.”

## Print the three lines on every withheld row

The printer is the artifact. A screenshot of Denied is not.

```python {linenos=inline,hl_lines=[22,"28-33"]}
#!/usr/bin/env python3
"""Print withheld vs never-ran vs owner. Never hide a result."""
from __future__ import annotations

import os
from classify_withheld import classify_row


def print_ticket(
    tool_name: str,
    tool_started: bool,
    event: str,
    plugin_withheld: bool,
) -> None:
    owner = os.environ.get("CLAUDE_CODE_OWNER", "").strip()
    if not owner:
        raise SystemExit("CLAUDE_CODE_OWNER is empty")
    row = classify_row(tool_started, event, plugin_withheld)
    print(f"owner={owner}")
    print(f"tool={tool_name}")
    print(f"started={tool_started} event={event} withheld={plugin_withheld}")
    print(f"this_field={row['this_field']} ticket={row['ticket']}")
    print(row["reason"])


if __name__ == "__main__":
    print_ticket(
        tool_name="Bash",
        tool_started=True,
        event="PostToolUse",
        plugin_withheld=True,
    )
```

If `CLAUDE_CODE_OWNER` is empty, stop. A coding agent does not fill that name. A Slack channel does not fill that name.

Official permissions page still evaluates deny before ask before allow. That order does not turn a PostToolUse withhold into a skip. Print the event name. Split “PreToolUse blocked” onto its own ticket. [Source: https://code.claude.com/docs/en/permissions] [Source: https://code.claude.com/docs/en/hooks]

![Ticket card: CLAUDE_CODE_OWNER, Tool started, Plugin withheld](/img/withheld-plugin-result-is-not-the-tool-never-ran-3.png)

## Scan the log for withheld, not for “empty”

An empty pane is not a classifier. Scan for the product sentence, a PostToolUse event, or a plugin-withheld flag. Do not re-run the tool to fill the pane.

```python
#!/usr/bin/env python3
"""Scan an agent log for withheld-result rows. Never execute the tool."""
from __future__ import annotations

import re
import sys
from pathlib import Path

WITHHELD_RE = re.compile(
    r"tool ran and a plugin withheld its result|plugin withheld its result",
    re.I,
)
NEVER_RAN_RE = re.compile(r"the tool never ran|tool never started", re.I)
POST_RE = re.compile(r"PostToolUse", re.I)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("agent.log")
    text = path.read_text(encoding="utf-8", errors="replace")
    withheld = 0
    never = 0
    post = 0
    for i, line in enumerate(text.splitlines(), 1):
        if WITHHELD_RE.search(line):
            print(f"{path}:{i}:this_field=True {line[:120]}")
            withheld += 1
        if NEVER_RAN_RE.search(line):
            print(f"{path}:{i}:junior_ticket=never_ran {line[:120]}")
            never += 1
        if POST_RE.search(line):
            post += 1
    print(f"withheld={withheld} never_ran_claims={never} posttooluse={post}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If the scan prints `this_field=True`, the ticket is this post. If it only prints PreToolUse blocks, look at nested deny, leftover `allowed-tools`, or UNC reads — those are other URLs. If it prints nothing, file a missing owner, a missing log, or a different permission field.

Official hooks docs still name the neighbor you must not collapse into this heading. `updatedToolOutput` replaces the inbound result after the tool ran. That is a withhold or a rewrite, not a skip. Do not write a recipe that strips PostToolUse so the pane always shows secrets. Print the event. Split “we need a visible redacted result” onto its own ticket. [Source: https://code.claude.com/docs/en/hooks]

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a plugin that redacts `.env` dumps, a junior who sees Denied on `Read(.env)`, and a chat that files never-ran because the pane is blank. I treat `CLAUDE_CODE_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) also owns “did the Read start, or did we file never-ran on a withheld plugin result.” A coding agent does not close that ticket because the pane was empty.
{{< /field-note >}}

## Neighbor fields that are not this ticket

Keep the heading small. Neighbor fires from the same week are other URLs.

| Neighbor | What it is | Why it is not this post |
| --- | --- | --- |
| Nested deny | A nested deny treated as a mod approval | Policy tree versus result pane, already shipped |
| Leftover `allowed-tools` | A skill grant that survived into a later turn | Grant lifetime versus withheld result |
| UNC path read | A network-shaped Read after a local allow | Path spelling versus result pane |
| Repeated reply ID | A phone yes that reused an ID | Channel verdict versus withheld result |
| disableAutoMode leftover | Desktop/SDK staying off auto until restart after the setting was removed | Mode switch, leftover social, not this slug |
| `$.process.spawn` withheld | Another mod denies a spawn after the child ran | Same product sentence, different tool, not this heading |

Do not steal those as a second heading. Do not clone [A Nested Deny Is Not a Mod Approval](/blog/nested-deny-is-not-a-mod-approval/). GSC this week still has no striking-distance query that asks for another nested-deny refresh. This unused URL is the withheld plugin result.

![Neighbor fields: Nested deny, UNC path read, Withheld result marked this ticket](/img/withheld-plugin-result-is-not-the-tool-never-ran-4.png)

## What you must not do

Forbidden:

1. File “the tool never ran” or “always-ask blocked it” without printing whether the tool started, withheld versus skipped, PreToolUse versus PostToolUse, and one human name.
2. Put `2.1.295`, `2.1.296`, or `8 October 2026` in the title as a version-style hook. The numbers are evidence after the decision.
3. Write a plugin-bypass or hide-result recipe: stripping PostToolUse, forging a visible secret result, disabling mods so `.env` always prints, or teaching the agent to ignore a withhold.
4. Recommend buying a plan, a 20X badge, or a seat because a pane was empty. Official hooks page lists PreToolUse and PostToolUse as timing, not a purchase ticket. [Source: https://code.claude.com/docs/en/hooks]
5. Treat nested deny, leftover `allowed-tools`, UNC reads, repeated reply ID, disableAutoMode leftover, or `$.process.spawn` withheld as this field.
6. Mix this field with allowed-mail, `ghs_` length, lockfile, redirected `rm`, or a Copilot assisted-permissions heading. Do not clone those shipped URLs.
7. Re-run the original tool against production to “fill the pane” as a demo.
8. Let a coding agent own `CLAUDE_CODE_OWNER`, or collapse a withheld result and a PreToolUse skip into one ticket.

Allowed:

1. Print whether the tool started. Redact secrets if a log leaked a result you cannot store.
2. Classify synthetic fixtures with `classify_withheld.py`. Do not execute them against live tools.
3. Scan logs for “plugin withheld its result” and for junior “never ran” claims.
4. Name one human as `CLAUDE_CODE_OWNER`.
5. Keep withheld results, PreToolUse blocks, and nested deny as separate tickets.
6. After the owner prints the four lines, treat Denied-plus-empty after a start as this field. Official release: the tool ran and a plugin withheld its result. Official hooks docs: PostToolUse is after execute. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.295] [Source: https://code.claude.com/docs/en/hooks]
7. Put one line in the agent instructions file you already own: when a plugin denies after a tool ran, print withheld versus never ran and refuse to file never-ran. Check the printed ticket. Do not trust the agent to follow the line.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about withheld results is not permission to skip the four lines.

## What you should do Monday morning

1. Open the repo that actually runs Claude Code. Export `CLAUDE_CODE_OWNER` to a human name. Run the ticket printer against yesterday’s agent log. Write `this_field=True` or `False` on the ticket next to that name.
2. For every `this_field=True` row, answer in one sentence: the tool started and a plugin withheld the result, or the call never started, or the pane still has a result, or the log never printed an event name. If you cannot answer, the ticket is “owner missing,” not “the tool never ran.”
3. Print PreToolUse versus PostToolUse. If the event is PreToolUse and the tool never started, that is a skip ticket. If the event is PostToolUse and a plugin withheld the result, official release notes name that field. Split those tickets. [Source: https://code.claude.com/docs/en/hooks] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.295]
4. Confirm coding-agent instructions on this desk name the same owner and forbid “the tool never ran” without the four lines. Forbid re-running production tools to fill a pane. Forbid writing a hide path that turns a withheld result into a visible secret dump.
5. Confirm PostToolUse still uses the documented shape: the tool already ran, exit 2 still reaches Claude, `updatedToolOutput` replaces the inbound result. Do not invent a dashboard that mints “never ran” from an empty pane. Do not display a fake skip screenshot as proof. [Source: https://code.claude.com/docs/en/hooks]
6. Leave nested deny, leftover `allowed-tools`, UNC reads, repeated reply ID, allowed-mail, `ghs_` length, lockfile, redirected `rm`, disableAutoMode leftover, and Copilot assisted-permissions off this ticket. Those are neighbor fields. Do not steal them as a second heading.

The question is not whether the changelog demos well. The question is whether the named owner can still tell a withheld plugin result from a tool that never ran after handoff.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.295" label="GitHub — Claude Code v2.1.295 release notes" >}}

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code Docs — Changelog" >}}

{{< source href="https://code.claude.com/docs/en/hooks" label="Claude Code Docs — Hooks (PostToolUse is after the tool ran)" >}}
