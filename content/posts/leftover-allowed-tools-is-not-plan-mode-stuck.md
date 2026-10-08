---
title: "A Leftover Allowed-Tools Rule Is Not You Still in Plan Mode"
date: 2026-10-08T07:00:00+07:00
draft: false
slug: "leftover-allowed-tools-is-not-plan-mode-stuck"
description: "A skill tool that still runs after you leave plan or auto is not proof the mode never changed. Print leftover allowed-tools, the current mode, and the named Claude Code owner before you file always-ask-broken."
topics: ["software-engineering"]
tags: ["claude-code", "allowed-tools", "plan-mode", "auto-mode", "coding-agents", "change-control"]
cover: /covers/leftover-allowed-tools-is-not-plan-mode-stuck.png
seo:
  primaryQuery: "claude code leftover allowed-tools after leaving plan mode"
  secondaryQueries:
    - "skill allowed-tools grant clears next message"
    - "leave auto mode leftover tool pass"
    - "named owner for claude code plan mode stuck tickets"
---

The junior hits Shift+Tab. The status bar leaves plan mode. The next turn still runs `Bash` from a skill with no prompt. Chat files the ticket: “plan mode is still on. always-ask is off.”

I stop the run there. A leftover `allowed-tools` rule is not you still in plan mode. Claude Code’s public notes that named this field are blunt: a skill’s or slash command’s `allowed-tools` rule used to come back in a later turn when you leave auto mode or plan mode partway through that turn. Official skills docs already say the grant is for the invoking turn and clears when you send the next message. The human left the mode. The second turn is not a stuck plan. [Source: https://code.claude.com/docs/en/changelog] [Source: https://code.claude.com/docs/en/skills]

I already refused to treat a repeated reply ID as a second approval in [A Repeated Reply ID Is Not a Second Approval](/blog/repeated-reply-id-is-not-a-second-approval/), a nested deny as a mod approval in [A Nested Deny Is Not a Mod Approval](/blog/nested-deny-is-not-a-mod-approval/), and an allowed-mail list as a Cloudflare account in [An Allowed-Mail List Is Not a Cloudflare Account](/blog/allowed-mail-is-not-a-cloudflare-account/). This post is the same desk rule for a leftover skill pass. Print the `allowed-tools` line. Print whether the session already left plan or auto. Name who owns the Claude Code answers.

The question is not whether the status bar looked quiet. The question is whether the named owner can still tell a leftover `allowed-tools` rule from a stuck plan.

<!--more-->

![Three columns: Leftover allowed-tools, Still in plan mode, Named Claude Code owner](/img/leftover-allowed-tools-is-not-plan-mode-stuck-1.png)

## The ticket that looks like plan-mode-is-stuck

Juniors treat a quiet prompt the way they treat a skipped always-ask. Yesterday they invoked `/deploy` in auto mode. Today they left auto, then a later turn ran `Bash` from that skill with no dialog. They page the desk: “plan mode never dropped” or “always-ask broke.”

Two jobs collide on that row.

1. **Keep the grant one-turn.** Official skills page: `allowed-tools` lists tools Claude can use without asking during the turn that invokes the skill. The grant clears when you send your next message, even though the skill body stays in context. Invoking the skill again re-applies the grant for that new turn. [Source: https://code.claude.com/docs/en/skills]
2. **Keep the leftover from riding a mode change.** Official changelog, 6 October 2026: a skill’s or slash command’s `allowed-tools` rule coming back in a later turn when you leave auto mode or plan mode partway through that turn is the named miss. After that date the leftover is the field. It is not proof the human is still in plan mode. [Source: https://code.claude.com/docs/en/changelog]

If you only screenshot “I already left plan,” you will file always-ask-broken. You will not file the leftover rule.

{{< note type="warning" title="Do not file always-ask-broken on a leftover allowed-tools rule" >}}
If a coding agent or a junior says plan mode is still on because a skill tool ran without a prompt after Shift+Tab, print the `allowed-tools` line, whether the session already left auto or plan, and one human name on the Claude Code answers. A leftover `allowed-tools` rule is not you still in plan mode.
{{< /note >}}

I do not invent a fake overnight outage of every plan-mode session. I use the public contract. The leftover rule is the ticket, not a version pin in the title.

## What Claude Code actually named

Read the 6 October 2026 changelog, then the skills frontmatter, then the permission-modes page that names how you leave plan. Do not trust a social recap. Do not trust this post without those pages.

The named field, published 6 October 2026:

> Fixed a skill’s or slash command’s allowed-tools rule coming back in a later turn when you leave auto mode or plan mode partway through that turn

That sentence has three parts. Print all three on the ticket.

| Part | What it is | What it is not |
| --- | --- | --- |
| Leftover `allowed-tools` | A skill or slash-command grant that survived into a later turn | Proof always-ask is off |
| Mode already left | Status bar no longer shows plan or auto after Shift+Tab or an approved plan | The human still sitting in plan mode |
| Named owner | The human who answers Claude Code permission rows | A coding agent, a skill file, or a slash command |

Official skills docs keep the grant small. The field is optional. It accepts a space- or comma-separated string, or a YAML list. The grant is for the invoking turn. Sending the next message clears it. Skill content stays in context; the permission grant does not. [Source: https://code.claude.com/docs/en/skills]

Official permission-modes docs name the leave path. Enter plan with Shift+Tab, `/plan`, or `claude --permission-mode plan`. Press Shift+Tab again to leave plan without approving a plan. Approving a plan exits plan and switches to the mode each approve option describes. From auto, the first Shift+Tab goes to Manual (`default`). [Source: https://code.claude.com/docs/en/permission-modes]

The leftover is the miss that looks like this ticket. Right mode change, wrong grant lifetime. After 6 October 2026, a skill pass that returns on a later turn after you left auto or plan mid-turn is that miss, not a stuck plan. [Source: https://code.claude.com/docs/en/changelog] [Source: https://code.claude.com/docs/en/skills]

{{< details summary="Where the pin sits after the decision, not in the title" >}}
Claude Code’s public changelog dates this field 6 October 2026 under the 2.1.292 heading. The same day’s notes also name first-run plugin install versus managed settings, UNC path reads, and `/ultrareview` staged copies. Do not put those tags in the title. Do not mix plan-mode classifier, extra-scope, redirected `rm`, nested deny, or repeated reply ID into this heading. [Source: https://code.claude.com/docs/en/changelog]
{{< /details >}}

## Four checks before you file

A mid-senior screenshots this list. A junior who only has the agent log still has a ticket they can close.

1. **Print the `allowed-tools` line.** Official docs: frontmatter on the skill or slash command. If the file has no `allowed-tools`, this is not the field. The session is using the normal permission mode. [Source: https://code.claude.com/docs/en/skills]
2. **Print leftover versus still-in-plan.** If the status bar still says plan, and you never left, the field is a live plan session. If you already left auto or plan mid-turn and a later turn still ran the skill tools with no prompt, the field is leftover. After 6 October 2026 that leftover is the named miss. [Source: https://code.claude.com/docs/en/changelog]
3. **Print who owns the session.** Official permission-modes page: you change a running session’s mode at any time. A skill file does not own the answers. A coding agent does not own them. [Source: https://code.claude.com/docs/en/permission-modes]
4. **Write one human name.** `CLAUDE_CODE_OWNER`. That name answers “is this a leftover `allowed-tools` rule, or did we file plan-mode-stuck on a later turn.”

![Four checks: Print allowed-tools, Leftover versus still in plan, Session owner, Named human](/img/leftover-allowed-tools-is-not-plan-mode-stuck-2.png)

## Probe the frontmatter before you file the ticket

Do not leave plan mode in production to “see if the grant still fires.” Classify the skill file. The probe below never talks to Claude Code. It never sends Shift+Tab. It never runs the skill.

```python
#!/usr/bin/env python3
"""Classify a skill or slash-command allowed-tools line. Never invoke the skill."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1]) or {}
    return data if isinstance(data, dict) else {}


def classify(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    raw = meta.get("allowed-tools")
    has_grant = raw not in (None, "", [], ())
    return {
        "path": str(path),
        "this_field": has_grant,
        "allowed_tools": raw,
        "reason": (
            "skill grant exists — leftover is this ticket"
            if has_grant
            else "no allowed-tools — not this field"
        ),
    }


def main() -> None:
    samples = [
        Path("fixtures/deploy-skill.md"),
        Path("fixtures/readme-only.md"),
    ]
    for row in samples:
        if not row.is_file():
            print(row, {"this_field": False, "reason": "missing fixture"})
            continue
        print(row, classify(row))


if __name__ == "__main__":
    main()
```

A fixture with `allowed-tools: Bash(git status *)` prints `this_field=True`. A file with no frontmatter grant prints `this_field=False`. That second file is not this post. Do not file plan-mode-stuck on a skill that never had a grant. [Source: https://code.claude.com/docs/en/skills]

{{< note type="note" title="The probe is a classifier, not a mode switch" >}}
Run it against fixtures and redacted `SKILL.md` copies. Do not point it at a live Claude Code session. Do not emit Shift+Tab. Do not teach a junior how to keep a grant alive after the next message.
{{< /note >}}

## Print the three lines on the ticket

The printer below is the whole close-out. It never calls the network. It never changes permission mode.

```python
#!/usr/bin/env python3
"""Print leftover allowed-tools vs still-in-plan vs named owner. Never switch modes."""
from __future__ import annotations

import os
from pathlib import Path

from classify_allowed_tools import classify


def main() -> int:
    owner = os.environ.get("CLAUDE_CODE_OWNER", "").strip()
    skill = Path(os.environ.get("SKILL_PATH", "SKILL.md"))
    mode_now = os.environ.get("PERMISSION_MODE_NOW", "").strip().lower()
    mode_when_invoked = os.environ.get("PERMISSION_MODE_WHEN_INVOKED", "").strip().lower()
    later_turn = os.environ.get("LATER_TURN", "false").strip().lower() == "true"
    row = classify(skill) if skill.is_file() else {"this_field": False, "reason": "missing skill file"}
    left_auto_or_plan = (
        mode_when_invoked in {"auto", "plan"}
        and mode_now not in {"auto", "plan"}
        and later_turn
    )
    print(f"CLAUDE_CODE_OWNER={owner or 'MISSING'}")
    print(f"this_field={row.get('this_field')}")
    print(f"mode_when_invoked={mode_when_invoked or 'MISSING'}")
    print(f"mode_now={mode_now or 'MISSING'}")
    print(f"later_turn={later_turn}")
    print(f"left_auto_or_plan={left_auto_or_plan}")
    print(f"reason={row.get('reason')}")
    if not owner:
        print("ticket=owner-missing")
        return 2
    if row.get("this_field") and left_auto_or_plan:
        print("ticket=leftover-allowed-tools-not-still-in-plan")
        return 0
    if mode_now == "plan":
        print("ticket=still-in-plan-mode")
        return 0
    print("ticket=not-this-field")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

Export `CLAUDE_CODE_OWNER=Shinjae`. Export `SKILL_PATH=fixtures/deploy-skill.md`. Export `PERMISSION_MODE_WHEN_INVOKED=plan`. Export `PERMISSION_MODE_NOW=default`. Export `LATER_TURN=true`. If the printer says `ticket=leftover-allowed-tools-not-still-in-plan`, close always-ask-broken. Open this field. If it says `owner-missing`, the ticket is a missing name, not a stuck plan.

![Ticket card: CLAUDE_CODE_OWNER, leftover true, mode now default](/img/leftover-allowed-tools-is-not-plan-mode-stuck-3.png)

## Scan the log. Do not leave plan in production.

You do not need to sit on Shift+Tab. You need to know whether the agent log already left auto or plan, then ran a skill tool with no prompt. Scan text. Do not start `claude --permission-mode plan` from the scanner.

```python
#!/usr/bin/env python3
"""Scan text logs for leftover allowed-tools after a mode leave. Never execute them."""
from __future__ import annotations

from pathlib import Path

ROOT = Path("logs")
NEEDLES = (
    "allowed-tools",
    "plan mode",
    "auto mode",
    "shift+tab",
    "permission mode",
    "/plan",
)


def main() -> int:
    hits = 0
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".log", ".md", ".txt", ".jsonl"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            if not any(n in low for n in NEEDLES):
                continue
            leftover = "allowed-tools" in low and (
                "later turn" in low or "leave auto" in low or "leave plan" in low
            )
            print(f"{path}:{i}:leftover={leftover} {line[:120]}")
            hits += 1
    print(f"hits={hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If the scan prints `leftover=True`, the ticket is this post. If it only prints `plan mode on` with no later-turn grant, the ticket is still-in-plan. If it prints nothing, file a missing owner, a missing log, or a different permission field.

Official docs still name the neighbor you must not collapse into this heading. Skill content stays in context across later turns. That persistence is instructions, not permissions. A later turn that still “knows” the skill is not a leftover grant. Print both. Split instruction persistence onto its own ticket. [Source: https://code.claude.com/docs/en/skills]

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a project skill at `.claude/skills/deploy/SKILL.md` with `allowed-tools: Bash(php artisan *)`, a reviewer who starts in plan, then leaves mid-turn because lunch started. I treat `CLAUDE_CODE_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) also owns “did the skill grant die with the next message, or did we file plan-mode-stuck on a leftover pass.” A coding agent does not close that ticket because `php artisan` ran quiet after Shift+Tab.
{{< /field-note >}}

## Neighbor fields that are not this ticket

Keep the heading small. Neighbor fires from the same week are other URLs.

| Neighbor | What it is | Why it is not this post |
| --- | --- | --- |
| Plan-mode classifier | Auto classifier approving a non-read-only connector while planning | Read-only pass versus plan, already a LinkedIn leftover |
| First-run plugin | Plugin install before managed settings loaded | Marketplace versus managed settings, already X and Threads |
| Repeated reply ID | A phone yes that reused an ID | Channel verdict versus leftover grant |
| Nested deny | A nested deny treated as a mod approval | Policy tree, already shipped |
| Redirected `rm` | A redirected remove treated as always-ask off | Shell rewrite, already shipped |
| UNC path read | Network path treated as a local allow | Sandbox versus local, leftover social |

Do not steal those as a second heading. Do not clone [A Repeated Reply ID Is Not a Second Approval](/blog/repeated-reply-id-is-not-a-second-approval/) or [A Nested Deny Is Not a Mod Approval](/blog/nested-deny-is-not-a-mod-approval/). GSC this week still has no striking-distance query that asks for another auto-start, green-deploy, `/readyz`, 2,500+, runner, sandbox-equals, lockfile, redirected-rm, `ghs_`, nested-deny, allowed-mail, or repeated-reply-ID refresh. This unused URL is the leftover grant.

![Neighbor fields: Plan-mode classifier, First-run plugin, Leftover allowed-tools marked this ticket](/img/leftover-allowed-tools-is-not-plan-mode-stuck-4.png)

## What you must not do

Forbidden:

1. File “plan mode is still on” or “always-ask is off” without printing the `allowed-tools` line, leftover versus still-in-plan, and one human name.
2. Put `2.1.292`, `2.1.293`, or `6 October 2026` in the title as a version-style hook. The numbers are evidence after the decision.
3. Write an allowed-tools-bypass or plan-mode-bypass recipe: keeping a grant after the next message, forging Shift+Tab, stripping permission mode, or mapping a way around the prompt.
4. Recommend buying a plan, a 20X badge, or a seat because a skill tool ran quiet after you left plan. Official permission-modes page lists modes as a tradeoff, not a purchase ticket. [Source: https://code.claude.com/docs/en/permission-modes]
5. Treat plan-mode classifier, first-run plugin, extra-scope, redirected `rm`, nested deny, or repeated reply ID as this field.
6. Mix this field with allowed-mail, `ghs_` length, lockfile, or sandbox-equals. Do not clone those shipped URLs.
7. Start a live plan-mode session in front of production data to demo the leftover.
8. Let a coding agent own `CLAUDE_CODE_OWNER`, or collapse a leftover grant and a stuck plan into one ticket.

Allowed:

1. Print the `allowed-tools` line. Redact the rest of the skill if a log leaked a command.
2. Classify synthetic fixtures with `classify_allowed_tools.py`. Do not execute them against a live session.
3. Scan logs for `allowed-tools` / `plan mode` / `auto mode` / `Shift+Tab`.
4. Name one human as `CLAUDE_CODE_OWNER`.
5. Keep leftover grant, still-in-plan, and skill-content persistence as separate tickets.
6. After the owner prints the four lines, treat the leftover as this field. Official changelog: the grant coming back after you leave auto or plan mid-turn is the named miss. Official skills docs: the grant clears on the next message. [Source: https://code.claude.com/docs/en/changelog] [Source: https://code.claude.com/docs/en/skills]
7. Put one line in the agent instructions file you already own: when the agent leaves plan or auto mid-turn, it prints `allowed-tools` and refuses to treat a later quiet tool as plan-mode-stuck. Check the printed ticket. Do not trust the agent to follow the line.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about leftover `allowed-tools` is not permission to skip the four lines.

## What you should do Monday morning

1. Open the repo that actually runs Claude Code with a project skill. Export `CLAUDE_CODE_OWNER` to a human name. Run the ticket printer against yesterday’s agent log and the skill file. Write `this_field=True` or `False` on the ticket next to that name.
2. For every `this_field=True` row, answer in one sentence: the session was still in plan, or it already left auto or plan and a later turn reused the grant, or the skill never had `allowed-tools`. If you cannot answer, the ticket is “owner missing,” not “always-ask is off.”
3. Print leftover versus still-in-plan. If the status bar still says plan, official docs still say you are exploring before you edit. If you already left and a later turn ran the skill tools with no prompt, official changelog names that leftover. Split those tickets. [Source: https://code.claude.com/docs/en/permission-modes] [Source: https://code.claude.com/docs/en/changelog]
4. Confirm coding-agent instructions on this desk name the same owner and forbid “plan mode is still on” without the four lines. Forbid starting a live plan session in front of production data to demo. Forbid writing a hide path that keeps a grant after the next message.
5. Confirm the grant still uses the documented shape: frontmatter `allowed-tools`, one invoking turn, clear on the next message. Do not invent a dashboard that mints grants. Do not display a fake status-bar screenshot as proof. [Source: https://code.claude.com/docs/en/skills]
6. Leave plan-mode classifier, first-run plugin, extra-scope, allowed-mail, nested deny, `ghs_` length, redirected `rm`, lockfile, repeated reply ID, and UNC path off this ticket. Those are neighbor fields. Do not steal them as a second heading.

The question is not whether the changelog demos well. The question is whether the named owner can still tell a leftover `allowed-tools` rule from a stuck plan after handoff.

## Further reading

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code Docs — Changelog" >}}

{{< source href="https://code.claude.com/docs/en/skills" label="Claude Code Docs — Skills (allowed-tools grant)" >}}

{{< source href="https://code.claude.com/docs/en/permission-modes" label="Claude Code Docs — Permission modes" >}}
