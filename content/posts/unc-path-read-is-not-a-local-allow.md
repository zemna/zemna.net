---
title: "A UNC Path Read Is Not a Local Allow"
date: 2026-10-09T07:00:00+07:00
draft: false
slug: "unc-path-read-is-not-a-local-allow"
description: "A quiet Read on a network share after you approved a local folder, or after auto mode, is not proof always-ask is off. Print UNC versus local versus the named Claude Code owner before you file the wrong ticket."
topics: ["devops"]
tags: ["claude-code", "unc", "permissions", "auto-mode", "coding-agents", "change-control"]
cover: /covers/unc-path-read-is-not-a-local-allow.png
seo:
  primaryQuery: "claude code UNC path read not a local allow"
  secondaryQueries:
    - "claude code network share permission prompt auto mode"
    - "PreToolUse hook approval UNC path"
    - "named owner for claude code always-ask tickets"
---

The junior approved `Read` on `C:\work\app\config.yaml`. The next turn reads `\\fileserver\share\app\config.yaml` with no dialog. Chat files the ticket: “always-ask is off. the sandbox already allowed it.”

I stop the run there. A UNC path read is not a local allow. Claude Code’s public notes that named this field are blunt: PreToolUse hook approvals and auto mode used to bypass the permission prompt for file reads from network (UNC) paths. Official permissions docs already say a command whose arguments include a network (UNC) path prompts, because looking that path up can send Windows credentials to the host it names. The human approved a local spelling. The second path is not that allow. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.292] [Source: https://code.claude.com/docs/en/permissions]

I already refused to treat a leftover `allowed-tools` rule as you still in plan mode in [A Leftover Allowed-Tools Rule Is Not You Still in Plan Mode](/blog/leftover-allowed-tools-is-not-plan-mode-stuck/), a repeated reply ID as a second approval in [A Repeated Reply ID Is Not a Second Approval](/blog/repeated-reply-id-is-not-a-second-approval/), and sandbox auto-allow as a retry tax on equals in [Sandbox Auto-Allow Is Not a Retry Tax on Equals in Inline Scripts](/blog/sandbox-auto-allow-is-not-a-retry-tax-on-equals/). This post is the same desk rule for a network-shaped read. Print the path class. Print whether the allow was local. Name who owns the Claude Code answers.

The question is not whether the prompt stayed quiet. The question is whether the named owner can still tell a UNC path read from a local allow.

<!--more-->

![Three columns: UNC path read, Local allow, Named Claude Code owner](/img/unc-path-read-is-not-a-local-allow-1.png)

## The ticket that looks like always-ask-is-off

Juniors treat a quiet Read the way they treat a skipped always-ask. Yesterday they approved a file under the checkout. Today auto mode, or a PreToolUse hook that already said yes, reads the same filename through a share. They page the desk: “always-ask broke” or “the sandbox already allowed it.”

Two jobs collide on that row.

1. **Keep local allows local.** Official permissions page: read-only file tools in the working directory and additional directories do not prompt. You extend that set with `--add-dir`, `/add-dir`, or `additionalDirectories`. You cannot add most network paths, such as the UNC share `\\server\share`, as working directories, because looking one up can contact the host it names. On Windows, map the share to a drive letter, then pass that drive at startup. [Source: https://code.claude.com/docs/en/permissions]
2. **Keep the network spelling on its own prompt.** Official changelog, 6 October 2026: PreToolUse hook approvals and auto mode bypassing the permission prompt for file reads from network (UNC) paths is the named miss. After that date the miss is the field. It is not proof always-ask is off, and it is not proof a local allow covered the share. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.292] [Source: https://code.claude.com/docs/en/changelog]

If you only screenshot “I already said yes to config.yaml,” you will file always-ask-broken. You will not file the UNC read.

{{< note type="warning" title="Do not file always-ask-broken on a UNC path read" >}}
If a coding agent or a junior says always-ask is off because a network share was read after a local allow, or after auto mode, print the path spelling, whether that spelling is UNC or `/net` or a mapped drive, and one human name on the Claude Code answers. A UNC path read is not a local allow.
{{< /note >}}

I do not invent a fake overnight outage of every Windows share. I use the public contract. The network-shaped read is the ticket, not a version pin in the title.

## What Claude Code actually named

Read the 6 October 2026 GitHub release body, then the permissions page, then the hooks page that names what a silent PreToolUse hook does. Do not trust a social recap. Do not trust this post without those pages.

The named field, published 6 October 2026:

> Security: Fixed PreToolUse hook approvals and auto mode bypassing the permission prompt for file reads from network (UNC) paths

That sentence has three parts. Print all three on the ticket.

| Part | What it is | What it is not |
| --- | --- | --- |
| UNC / network path read | A Read whose spelling names a share, a `\\server\share` host, or a `/net/<host>/` automount | Proof a local folder allow still covers it |
| Local allow | A yes on a path inside the working directory or an added local directory | A yes on every filename that happens to match |
| Named owner | The human who answers Claude Code permission rows | A coding agent, a PreToolUse hook, or auto mode |

Official permissions docs keep the network case loud. A command whose arguments include a network (UNC) path, such as `\\server\share\file`, prompts because accessing a network path can send your Windows credentials to the host it names. The same check applies to PowerShell tool commands. [Source: https://code.claude.com/docs/en/permissions]

Official hooks docs keep PreToolUse small. The hook fires before a tool call executes. It can block the call. Exit code 0 with no output means the hook has no decision to report, so the tool call continues through the normal permission flow. The hook can deny the call. Staying silent does not approve it. [Source: https://code.claude.com/docs/en/hooks]

The miss that looks like this ticket is the opposite mix: a PreToolUse yes, or auto mode, treated a network-shaped Read as already allowed. Right filename, wrong spelling. After 6 October 2026, a share read that skipped the prompt because a hook or auto mode had already waved a local path is that miss, not always-ask off. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.292] [Source: https://code.claude.com/docs/en/hooks]

{{< details summary="Where the pin sits after the decision, not in the title" >}}
Claude Code’s public GitHub release dates this field 6 October 2026 under the v2.1.292 heading (`published_at` 2026-10-06T18:59:30Z, not a prerelease). The same day’s notes also name leftover `allowed-tools`, first-run plugin install versus managed settings, and `/ultrareview` staged copies. npm `dist-tags.latest` on the morning this post shipped was 2.1.295; `dist-tags.stable` was 2.1.286. The field for this URL is the UNC line, not a pin in the title. Do not mix redirected `rm`, nested deny, leftover allowed-tools, or sandbox-equals into this heading. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.292]
{{< /details >}}

## Four checks before you file

A mid-senior screenshots this list. A junior who only has the agent log still has a ticket they can close.

1. **Print the path spelling.** Copy the Read argument as the tool received it. If the log only shows a basename, the ticket is “path missing,” not always-ask-broken.
2. **Print UNC versus local versus mapped drive.** `\\server\share\...` or `//server/share/...` is UNC. `/net/<host>/...` is an automount. `Z:\app\config.yaml` after `net use Z:` is a mapped drive the permissions page tells you to pass with `--add-dir`. `C:\work\app\config.yaml` is local. Do not collapse those four into “the same file.” [Source: https://code.claude.com/docs/en/permissions]
3. **Print what was actually approved.** A local working-directory Read, an `--add-dir` folder, a PreToolUse `permissionDecision: "allow"`, or auto mode. Official hooks page: a silent hook is not an allow. [Source: https://code.claude.com/docs/en/hooks]
4. **Write one human name.** `CLAUDE_CODE_OWNER`. That name answers “is this a UNC path read, or did we file always-ask-broken on a local allow.”

![Four checks: Print the spelling, UNC versus local, What was approved, Named human](/img/unc-path-read-is-not-a-local-allow-2.png)

## Probe the spelling before you file the ticket

Do not open the share “to see if the prompt still fires.” Classify the string. Save the next block as `classify_path_shape.py`. The probe never talks to Claude Code. It never mounts a drive. It never reads a file.

```python
#!/usr/bin/env python3
"""Classify a Read path spelling. Never open the path. Never talk to a share."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def classify_spelling(raw: str) -> dict[str, Any]:
    text = (raw or "").strip()
    lowered = text.replace("/", "\\").lower()
    is_unc = text.startswith("\\\\") or text.startswith("//")
    is_automount = text.startswith("/net/")
    is_drive = len(text) >= 3 and text[1] == ":" and text[0].isalpha()
    is_local_posix = text.startswith("/") and not is_automount and not is_unc
    if is_unc or is_automount:
        ticket = "unc-path-read-not-a-local-allow"
        reason = "network-shaped spelling — this field"
    elif is_drive or is_local_posix:
        ticket = "local-allow-or-other-field"
        reason = "local spelling — not this UNC ticket"
    else:
        ticket = "owner-missing-or-path-missing"
        reason = "cannot classify — print the raw Read argument"
    return {
        "raw": text,
        "this_field": ticket == "unc-path-read-not-a-local-allow",
        "ticket": ticket,
        "reason": reason,
        "looks_like_dav": "davwwwroot" in lowered or "@ssl@" in lowered,
    }


def classify_file(path: Path) -> dict[str, Any]:
    line = path.read_text(encoding="utf-8").splitlines()[0] if path.exists() else ""
    row = classify_spelling(line)
    row["fixture"] = str(path)
    return row


if __name__ == "__main__":
    import json
    import sys

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("fixtures/read-path.txt")
    print(json.dumps(classify_file(target), indent=2))
```

The fixture is one line. Put the Read argument in `fixtures/read-path.txt`. Do not put a live password, a live hostname you have not already redacted, or a production share URL you are not allowed to store.

```json
{
  "owner": "Shinjae",
  "approved_path": "C:\\work\\app\\config.yaml",
  "read_path": "\\\\fileserver\\share\\app\\config.yaml",
  "mode_when_read": "auto",
  "pretooluse_decision": "allow",
  "ticket": "unc-path-read-not-a-local-allow"
}
```

Export `CLAUDE_CODE_OWNER=Shinjae`. Export `APPROVED_PATH` and `READ_PATH` from the log, not from memory. If the printer says `ticket=unc-path-read-not-a-local-allow`, close always-ask-broken. Open this field. If it says `owner-missing-or-path-missing`, the ticket is a missing name or a missing spelling, not a broken prompt.

```python
#!/usr/bin/env python3
"""Print the UNC ticket. Never mount. Never call Claude Code."""
from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    owner = os.environ.get("CLAUDE_CODE_OWNER", "").strip()
    approved = os.environ.get("APPROVED_PATH", "").strip()
    read_path = os.environ.get("READ_PATH", "").strip()
    mode = os.environ.get("PERMISSION_MODE_WHEN_READ", "").strip()
    if not owner:
        print("ticket=owner-missing")
        return 2
    from classify_path_shape import classify_spelling

    read_row = classify_spelling(read_path)
    approved_row = classify_spelling(approved)
    this_field = read_row["this_field"] and not approved_row["this_field"]
    ticket = (
        "unc-path-read-not-a-local-allow"
        if this_field
        else read_row["ticket"]
    )
    payload = {
        "owner": owner,
        "approved_class": approved_row["ticket"],
        "read_class": read_row["ticket"],
        "mode_when_read": mode,
        "ticket": ticket,
    }
    out = Path("unc-ticket.json")
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"ticket={ticket}")
    print(f"owner={owner}")
    return 0 if this_field else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

If `ticket=unc-path-read-not-a-local-allow`, the later quiet Read is this post. If both spellings classify as local, this is not the field. If both classify as UNC, you still print the owner, then you still refuse to call that a local allow.

![Ticket card: CLAUDE_CODE_OWNER, approved local path, network-shaped read, this ticket](/img/unc-path-read-is-not-a-local-allow-3.png)

## Scan the log for the spelling, not for “quiet”

A quiet tool line is not a classifier. Scan for the Read argument. Redact the host if the log is leaving the building.

```python
#!/usr/bin/env python3
"""Scan an agent log for Read paths. Never execute the Read."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from classify_path_shape import classify_spelling

READ_RE = re.compile(r"Read\(([^)]+)\)")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("agent.log")
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = 0
    for i, line in enumerate(text.splitlines(), 1):
        for match in READ_RE.finditer(line):
            raw = match.group(1).strip().strip("\"'")
            row = classify_spelling(raw)
            print(f"{path}:{i}:this_field={row['this_field']} ticket={row['ticket']} {raw[:80]}")
            hits += 1
    print(f"hits={hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If the scan prints `this_field=True`, the ticket is this post. If it only prints local spellings, look at leftover `allowed-tools`, redirected `rm`, or sandbox-equals — those are other URLs. If it prints nothing, file a missing owner, a missing log, or a different permission field.

Official docs still name the neighbor you must not collapse into this heading. You cannot add most UNC shares as working directories. Mapping the share to a drive letter, then passing that drive with `--add-dir`, is the documented Windows path. That mapped drive is still not a silent UNC spelling, and it is not a sandbox-bypass recipe. Print both. Split “we never added the drive” onto its own ticket. [Source: https://code.claude.com/docs/en/permissions]

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a Windows jump box, a share that holds uploaded brand assets, and a reviewer who approved `Read` on `C:\work\modoo-id\storage\app\public\logo.png` then watched auto mode open `\\assets\brand\logo.png`. I treat `CLAUDE_CODE_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) also owns “did we approve a local checkout file, or did we file always-ask-broken on a UNC read.” A coding agent does not close that ticket because the basename matched.
{{< /field-note >}}

## Neighbor fields that are not this ticket

Keep the heading small. Neighbor fires from the same week are other URLs.

| Neighbor | What it is | Why it is not this post |
| --- | --- | --- |
| Leftover `allowed-tools` | A skill grant that survived into a later turn after you left plan or auto | Grant lifetime versus path spelling, already shipped |
| Repeated reply ID | A phone yes that reused an ID | Channel verdict versus UNC read |
| Sandbox auto-allow on equals | An every-run prompt on `python3 -c` | Matcher versus network path |
| Redirected `rm` | A redirected remove treated as always-ask off | Shell rewrite, already shipped |
| Nested deny | A nested deny treated as a mod approval | Policy tree, already shipped |
| `/ultrareview` staged copies | Sandboxed commands reading staged uploads under `~/.claude/seed-admin` | Same-day leftover social, not this slug |

Do not steal those as a second heading. Do not clone [A Leftover Allowed-Tools Rule Is Not You Still in Plan Mode](/blog/leftover-allowed-tools-is-not-plan-mode-stuck/) or [Print the Redirect Before You File Always-Ask Off](/blog/print-the-redirect-before-you-file-always-ask-off/). GSC this week still has no striking-distance query that asks for another leftover-allowed-tools refresh. This unused URL is the UNC read.

![Neighbor fields: Leftover allowed-tools, Redirected rm, UNC path read marked this ticket](/img/unc-path-read-is-not-a-local-allow-4.png)

## What you must not do

Forbidden:

1. File “always-ask is off” or “the sandbox already allowed it” without printing the Read spelling, UNC versus local, and one human name.
2. Put `2.1.292`, `2.1.295`, or `6 October 2026` in the title as a version-style hook. The numbers are evidence after the decision.
3. Write a UNC-read or sandbox-bypass recipe: forging a local spelling over a share, stripping the network-path prompt, mapping a way around PreToolUse, or teaching auto mode to treat `\\server\share` as the working directory.
4. Recommend buying a plan, a 20X badge, or a seat because a share was read quiet. Official permissions page lists working directories and `--add-dir` as a path-shape rule, not a purchase ticket. [Source: https://code.claude.com/docs/en/permissions]
5. Treat leftover `allowed-tools`, redirected `rm`, nested deny, sandbox-equals, or `/ultrareview` staged copies as this field.
6. Mix this field with allowed-mail, `ghs_` length, lockfile, or a Copilot local-sandbox heading. Do not clone those shipped URLs.
7. Mount the production share, or start a live auto-mode session against it, to demo the miss.
8. Let a coding agent own `CLAUDE_CODE_OWNER`, or collapse a UNC read and a local allow into one ticket.

Allowed:

1. Print the Read spelling. Redact the host if a log leaked a share you cannot store.
2. Classify synthetic fixtures with `classify_path_shape.py`. Do not execute them against a live share.
3. Scan logs for `Read(` plus `\\`, `//`, or `/net/`.
4. Name one human as `CLAUDE_CODE_OWNER`.
5. Keep UNC reads, mapped-drive `--add-dir` misses, and leftover `allowed-tools` as separate tickets.
6. After the owner prints the four lines, treat the network-shaped quiet Read as this field. Official release: PreToolUse hook approvals and auto mode bypassing the prompt for network (UNC) path reads is the named miss. Official permissions docs: a UNC argument prompts; most UNC shares cannot be working directories. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.292] [Source: https://code.claude.com/docs/en/permissions]
7. Put one line in the agent instructions file you already own: when the agent reads a path, it prints the spelling class and refuses to treat a UNC Read as a local allow. Check the printed ticket. Do not trust the agent to follow the line.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about UNC reads is not permission to skip the four lines.

## What you should do Monday morning

1. Open the repo that actually runs Claude Code on a machine that can see a share. Export `CLAUDE_CODE_OWNER` to a human name. Run the ticket printer against yesterday’s agent log. Write `this_field=True` or `False` on the ticket next to that name.
2. For every `this_field=True` row, answer in one sentence: the approved path was local and the Read was UNC, or both were local, or both were UNC, or the log never printed a spelling. If you cannot answer, the ticket is “owner missing,” not “always-ask is off.”
3. Print UNC versus mapped drive versus local. If the path is a mapped drive, official docs still say pass that drive with `--add-dir`; that is not this slug. If the path is UNC or `/net/` after a local yes, or after auto mode, official release notes name that miss. Split those tickets. [Source: https://code.claude.com/docs/en/permissions] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.292]
4. Confirm coding-agent instructions on this desk name the same owner and forbid “always-ask is off” without the four lines. Forbid mounting a production share to demo. Forbid writing a hide path that turns a UNC Read into a local allow.
5. Confirm PreToolUse still uses the documented shape: a deny is a deny, silence is not an allow, the call then hits the normal permission flow. Do not invent a dashboard that mints network allows. Do not display a fake quiet-prompt screenshot as proof. [Source: https://code.claude.com/docs/en/hooks]
6. Leave leftover `allowed-tools`, repeated reply ID, sandbox-equals, redirected `rm`, nested deny, allowed-mail, `ghs_` length, lockfile, and `/ultrareview` staged copies off this ticket. Those are neighbor fields. Do not steal them as a second heading.

The question is not whether the changelog demos well. The question is whether the named owner can still tell a UNC path read from a local allow after handoff.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.292" label="GitHub — Claude Code v2.1.292 release notes" >}}

{{< source href="https://code.claude.com/docs/en/permissions" label="Claude Code Docs — Permissions (network / UNC paths)" >}}

{{< source href="https://code.claude.com/docs/en/hooks" label="Claude Code Docs — Hooks (PreToolUse is not a silent allow)" >}}
