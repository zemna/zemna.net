---
title: "A Repeated Reply ID Is Not a Second Approval"
date: 2026-10-07T07:00:00+07:00
draft: false
slug: "repeated-reply-id-is-not-a-second-approval"
description: "A phone yes that reuses a reply ID is not a second human allow. Print the ID, the open request, and the named Claude Code owner before you file always-ask-broken."
topics: ["developer-tools"]
tags: ["claude-code", "channels", "permission-relay", "reply-id", "coding-agents", "change-control"]
cover: /covers/repeated-reply-id-is-not-a-second-approval.png
seo:
  primaryQuery: "claude code channels repeated reply ID not a second approval"
  secondaryQueries:
    - "channels permission relay duplicate request_id"
    - "yes id approving a different prompt"
    - "named owner for claude code channel approvals"
---

The junior pastes a phone screenshot. They already answered `yes kqmpw` on Telegram. A second Bash row ran. Chat files the ticket: “always-ask is off. I never approved that command.”

I stop the run there. A repeated reply ID is not a second approval. Claude Code’s public notes that named this field are blunt: permission relay on `--channels` used to treat a reply ID that repeats inside one session as a verdict on a different prompt. The field now ignores that repeat. The human still answered one ID. The second tool is not a second allow. [Source: https://code.claude.com/docs/en/changelog] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.290]

I already refused to treat an allowed-mail list as a Cloudflare account in [An Allowed-Mail List Is Not a Cloudflare Account](/blog/allowed-mail-is-not-a-cloudflare-account/), a nested deny as a mod approval in [A Nested Deny Is Not a Mod Approval](/blog/nested-deny-is-not-a-mod-approval/), and a 40-character `ghs_` check as a valid App token in [A 40-Character ghs_ Check Is Not a Valid App Token](/blog/ghs-length-is-not-a-valid-app-token/). This post is the same desk rule for a channel yes. Print the reply ID. Print whether that ID is still an open request. Name who owns the Claude Code answers.

The question is not whether the phone said yes. The question is whether the named owner can still tell a repeated reply ID from a second approval.

<!--more-->

![Three columns: Repeated reply ID, Second approval, Named Claude Code owner](/img/repeated-reply-id-is-not-a-second-approval-1.png)

## The ticket that looks like always-ask-is-off

Juniors treat a second tool row the way they treat a skipped prompt. Yesterday they approved one Bash from the phone. Today another Bash ran with the same five-letter code in the chat. They page the desk: “always-ask broke” or “the channel auto-approved.”

Two jobs collide on that yes.

1. **Keep the open request honest.** Official channels reference: Claude Code generates a short request ID, the channel server forwards the prompt and that ID, the remote user answers yes or no with that ID, and Claude Code applies the verdict only if the ID matches an open request. The local terminal dialog stays open the whole time. [Source: https://code.claude.com/docs/en/channels-reference]
2. **Keep the ID one-shot.** Official changelog, 5 October 2026: a reply ID that repeats within a session is now ignored instead of approving a different prompt. A reused ID is a replay. It is not a second human allow. [Source: https://code.claude.com/docs/en/changelog] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.290]

If you only screenshot “I already said yes,” you will file always-ask-broken. You will not file the reply ID.

{{< note type="warning" title="Do not file always-ask-broken on a repeated reply ID" >}}
If a coding agent or a junior says always-ask is off because a second tool ran after a phone yes, print the reply ID, whether that ID still matched an open request, and one human name on the Claude Code answers. A repeated reply ID is not a second approval.
{{< /note >}}

I do not invent a fake overnight outage of every Telegram bot. I use the public contract. The reply ID is the ticket, not a version pin in the title.

## What Claude Code actually named

Read the 5 October 2026 changelog, then the GitHub release body, then the channels reference that names the four-step relay. Do not trust a social recap. Do not trust this post without those pages.

The named field, published 5 October 2026:

> Fixed `--channels` permission relay: a reply ID that repeats within a session is now ignored instead of approving a different prompt.

That sentence has three parts. Print all three on the ticket.

| Part | What it is | What it is not |
| --- | --- | --- |
| Reply ID | The five-letter `request_id` Claude Code issued for one open prompt | Proof always-ask is off |
| Open request | A prompt still waiting in that session for that ID | A second tool that reused the same ID |
| Named owner | The human who answers Claude Code permission rows | A Telegram bot, a Discord webhook, or a coding agent |

Official docs keep the ID shape small. `request_id` is five lowercase letters drawn from `a`–`z` without `l`, so it never reads as a `1` or `I` on a phone. Include it in the outgoing prompt so the reply can echo it. Claude Code only accepts a verdict that carries an ID it issued. The local terminal dialog does not display this ID. Your outbound handler is the only way to learn it. [Source: https://code.claude.com/docs/en/channels-reference]

The verdict the server sends back is `notifications/claude/channel/permission` with two fields: `request_id` echoing that ID, and `behavior` set to `allow` or `deny`. Allow lets that tool call proceed. Deny rejects it. Neither verdict affects future calls. [Source: https://code.claude.com/docs/en/channels-reference]

Official docs also name the miss that looks like this ticket. Right format, wrong ID: your server emits a verdict, Claude Code finds no open request with that ID, and drops it silently. After 5 October 2026, a repeated ID inside one session is that miss, not a second allow. [Source: https://code.claude.com/docs/en/channels-reference] [Source: https://code.claude.com/docs/en/changelog]

{{< details summary="Where the pin sits after the decision, not in the title" >}}
Claude Code’s public changelog dates this field 5 October 2026 under the 2.1.290 heading. GitHub’s `anthropics/claude-code` tag `v2.1.290` carries the same sentence in its release body (`e8ae451`, 05 Oct 23:33). The next day’s 2.1.291 notes a different field: cloud sessions dropping answers to permission prompts. Do not put those tags in the title. Do not mix compacted `/loop`, plan-mode classifier, extra-scope, or yes-but-ask-again into this heading. [Source: https://code.claude.com/docs/en/changelog] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.290]
{{< /details >}}

## Four checks before you file

A mid-senior screenshots this list. A junior who only has the agent log still has a ticket they can close.

1. **Print the reply ID.** Official docs: five lowercase letters, no `l`. If the chat line is a bare `yes` with no ID, official docs say that text falls through as a normal message to Claude. That is not this field. [Source: https://code.claude.com/docs/en/channels-reference]
2. **Print open request versus replay.** If this is the first time the session saw that ID, and a prompt with that ID is still open, the field is a real verdict. If the same ID already produced a verdict in this session, the field is a replay. After 5 October 2026 the replay is ignored. It does not approve a different prompt. [Source: https://code.claude.com/docs/en/changelog]
3. **Print who owns the session.** Official channels page: events only arrive while the session is open. `--channels` names the server. A Slack thread does not own the answers. A coding agent does not own them. [Source: https://code.claude.com/docs/en/channels]
4. **Write one human name.** `CLAUDE_CODE_OWNER`. That name answers “is this a repeated reply ID, or did we file always-ask-broken on a second tool.”

![Four checks: Print the reply ID, Open request versus replay, Session owner, Named human](/img/repeated-reply-id-is-not-a-second-approval-2.png)

## Probe the ID before you file the ticket

Do not replay a live permission prompt to “see if it still fires.” Classify the log line. The probe below never talks to Claude Code. It never sends `yes`. It never opens a channel.

```python
#!/usr/bin/env python3
"""Classify a channel permission reply. Never send a verdict."""
from __future__ import annotations

import re
from typing import Any

ID_RE = re.compile(r"\b([a-km-z]{5})\b")
YES_NO = re.compile(r"^\s*(yes|no)\s+([a-km-z]{5})\s*$", re.I)


def classify(line: str, seen: set[str]) -> dict[str, Any]:
    text = line.strip()
    match = YES_NO.match(text)
    if not match:
        bare = text.lower() in {"yes", "no"}
        return {
            "this_field": False,
            "bare_yes_no": bare,
            "reply_id": None,
            "replay": False,
            "reason": "not yes/no plus five-letter id",
        }
    reply_id = match.group(2).lower()
    replay = reply_id in seen
    seen.add(reply_id)
    return {
        "this_field": True,
        "bare_yes_no": False,
        "reply_id": reply_id,
        "replay": replay,
        "behavior": match.group(1).lower(),
        "reason": "replay ignored after 5 Oct 2026" if replay else "open-request verdict",
    }


def main() -> None:
    seen: set[str] = set()
    samples = [
        "yes kqmpw",
        "yes kqmpw",
        "yes",
        "approve it",
        "no hrtvx",
    ]
    for row in samples:
        print(row, classify(row, seen))


if __name__ == "__main__":
    main()
```

The first `yes kqmpw` prints `replay=False`. The second prints `replay=True`. That second line is this post. `yes` with no ID is the official miss: the inbound regex never matches, so the text is a normal message. `approve it` is the same miss. Do not file always-ask-broken on either of those. [Source: https://code.claude.com/docs/en/channels-reference]

{{< note type="note" title="The probe is a classifier, not a channel" >}}
Run it against fixtures and redacted logs. Do not point it at a live `--channels` session. Do not emit `notifications/claude/channel/permission`. Do not teach a junior how to reuse an ID against a different prompt.
{{< /note >}}

## Print the three lines on the ticket

The printer below is the whole close-out. It never calls the network. It never mints an ID.

```python
#!/usr/bin/env python3
"""Print reply-id vs second-approval vs named owner. Never send yes."""
from __future__ import annotations

import json
import os
from pathlib import Path

from classify_reply_id import classify


def load_seen(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("seen_ids") or [])


def main() -> int:
    owner = os.environ.get("CLAUDE_CODE_OWNER", "").strip()
    line = os.environ.get("CHANNEL_REPLY_LINE", "").strip()
    seen_path = Path(os.environ.get("SEEN_IDS_PATH", "seen-reply-ids.json"))
    seen = load_seen(seen_path)
    row = classify(line, seen)
    print(f"CLAUDE_CODE_OWNER={owner or 'MISSING'}")
    print(f"reply_id={row.get('reply_id')}")
    print(f"replay={row.get('replay')}")
    print(f"this_field={row.get('this_field')}")
    print(f"reason={row.get('reason')}")
    if not owner:
        print("ticket=owner-missing")
        return 2
    if row.get("replay"):
        print("ticket=repeated-reply-id-not-second-approval")
        return 0
    if row.get("this_field"):
        print("ticket=open-request-verdict")
        return 0
    print("ticket=not-this-field")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

Export `CLAUDE_CODE_OWNER=Shinjae`. Export `CHANNEL_REPLY_LINE='yes kqmpw'`. If the printer says `replay=True`, close always-ask-broken. Open this field. If it says `owner-missing`, the ticket is a missing name, not a skipped prompt.

![Ticket card: CLAUDE_CODE_OWNER, reply_id, replay true, not a second approval](/img/repeated-reply-id-is-not-a-second-approval-3.png)

## Scan the log. Do not send yes.

You do not need to sit on Telegram. You need to know whether the agent log already used that ID. Scan text. Do not start `claude --channels` from the scanner.

```python
#!/usr/bin/env python3
"""Scan text logs for channel permission replies. Never execute them."""
from __future__ import annotations

from pathlib import Path

from classify_reply_id import classify

ROOT = Path("logs")
NEEDLES = ("yes ", "no ", "request_id", "permission relay", "--channels")


def main() -> int:
    hits = 0
    seen: set[str] = set()
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
            row = classify(line, seen)
            if not row["this_field"] and "request_id" not in low:
                continue
            print(
                f"{path}:{i}:this_field={row.get('this_field')} "
                f"replay={row.get('replay')} id={row.get('reply_id')}"
            )
            hits += 1
    print(f"hits={hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If the scan prints `replay=True`, the ticket is this post. If it prints `this_field=True` once, the ticket is an open-request verdict. If it prints nothing, file a missing owner, a missing log, or a different permission field.

Official docs still name the race you must not collapse into this heading. Both the terminal dialog and the phone stay live. Whichever answer arrives first wins. The other is dropped. A local yes that closed the prompt before the phone yes arrived is not a repeated ID. Print both timestamps. Split that race onto its own ticket. [Source: https://code.claude.com/docs/en/channels-reference]

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: Vite on `localhost:5173`, a coding agent that already knows `claude --channels plugin:telegram@claude-plugins-official`, and a reviewer on a phone who answers `yes kqmpw` while walking to lunch. I treat `CLAUDE_CODE_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) also owns “did we apply one open-request verdict, or did we file always-ask-broken on a repeated reply ID.” A coding agent does not close that ticket because a second Bash row showed up in the transcript.
{{< /field-note >}}

## Neighbor fields that are not this ticket

Keep the heading small. Neighbor fires from the same week are other URLs.

| Neighbor | What it is | Why it is not this post |
| --- | --- | --- |
| Compacted `/loop` | Scheduled tasks silently not returning after compaction | Reminder versus cancelled cron, not a reply ID |
| Plan-mode classifier | Auto classifier approving a non-read-only connector | Read-only pass versus plan mode, not a phone yes |
| Extra scope | A token that asked for more than the job | Scope versus allow, not a repeated ID |
| Yes-but-ask-again | A prompt that returned after you already answered | Ask-again versus replay of the same ID |
| Allowed-mail | Email OTP on a Quick Tunnel | Cloudflare guest list, already shipped |

Do not steal those as a second heading. Do not clone [An Allowed-Mail List Is Not a Cloudflare Account](/blog/allowed-mail-is-not-a-cloudflare-account/) or [A Nested Deny Is Not a Mod Approval](/blog/nested-deny-is-not-a-mod-approval/). GSC this week still has no striking-distance query that asks for another auto-start, green-deploy, `/readyz`, 2,500+, runner, sandbox-equals, lockfile, redirected-rm, `ghs_`, nested-deny, or allowed-mail refresh. This unused URL is the reply ID.

![Neighbor fields: Compacted loop, Plan-mode classifier, Repeated reply ID marked this ticket](/img/repeated-reply-id-is-not-a-second-approval-4.png)

## What you must not do

Forbidden:

1. File “always-ask is off” without printing the reply ID, open request versus replay, and one human name.
2. Put `2.1.290`, `2.1.291`, or `5 October 2026` in the title as a version-style hook. The numbers are evidence after the decision.
3. Write a channels-approval-bypass recipe: replaying `yes <id>` against a later prompt, forging `notifications/claude/channel/permission`, stripping `--channels`, or mapping a way around the local dialog.
4. Recommend buying a plan, a 20X badge, or a seat because a phone yes reused an ID. Official channels page: channels are a research preview. That is not a purchase ticket. [Source: https://code.claude.com/docs/en/channels]
5. Treat compacted `/loop`, plan-mode classifier, extra-scope, or yes-but-ask-again as this field.
6. Mix this field with allowed-mail, nested deny, `ghs_` length, redirected `rm`, or lockfile. Do not clone those shipped URLs.
7. Start a live `--channels` session in front of production data to demo the classifier.
8. Let a coding agent own `CLAUDE_CODE_OWNER`, or collapse a repeated reply ID and a second approval into one ticket.

Allowed:

1. Print the ID. Redact the rest of the chat if a log leaked a command.
2. Classify synthetic fixtures with `classify_reply_id.py`. Do not execute them against a live session.
3. Scan logs for `yes ` / `no ` / `request_id` / `--channels`.
4. Name one human as `CLAUDE_CODE_OWNER`.
5. Keep open-request verdict, repeated-ID ignore, and terminal-versus-phone race as separate tickets.
6. After the owner prints the four lines, ignore the replay. Official changelog: a repeated ID is ignored. It does not approve a different prompt. [Source: https://code.claude.com/docs/en/changelog]
7. Put one line in the agent instructions file you already own: when the agent relays a permission prompt, it prints the `request_id` and refuses to treat a second `yes` with the same ID as a new allow. Check the printed seen-set. Do not trust the agent to follow the line.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about `--channels` permission relay is not permission to skip the four lines.

## What you should do Monday morning

1. Open the repo that actually runs Claude Code with `--channels`. Export `CLAUDE_CODE_OWNER` to a human name. Run the ticket printer against yesterday’s agent log. Write `this_field=True` or `False` on the ticket next to that name.
2. For every `this_field=True` row, answer in one sentence: the phone yes matched an open request, or it reused an ID this session already spent, or it was a bare `yes` with no ID. If you cannot answer, the ticket is “owner missing,” not “always-ask is off.”
3. Print open request versus replay. If the ID is new and still open, official docs still say Claude Code applies the verdict only when the ID matches. If the ID already produced a verdict, official changelog says the repeat is ignored. Split those tickets. [Source: https://code.claude.com/docs/en/channels-reference] [Source: https://code.claude.com/docs/en/changelog]
4. Confirm coding-agent instructions on this desk name the same owner and forbid “always-ask is off” without the four lines. Forbid starting a live channel in front of production data to demo. Forbid writing a hide path that reuses an ID against a later prompt.
5. Confirm the ID still uses the documented shape: five lowercase letters, no `l`. Do not invent a dashboard that mints IDs. Do not display the ID on a fake terminal screenshot. The local dialog does not show it. [Source: https://code.claude.com/docs/en/channels-reference]
6. Leave compacted `/loop`, plan-mode classifier, extra-scope, allowed-mail, nested deny, `ghs_` length, redirected `rm`, and lockfile off this ticket. Those are neighbor fields. Do not steal them as a second heading.

The question is not whether the changelog demos well. The question is whether the named owner can still tell a repeated reply ID from a second approval after handoff.

## Further reading

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code Docs — Changelog" >}}

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.290" label="GitHub — claude-code v2.1.290 release notes" >}}

{{< source href="https://code.claude.com/docs/en/channels-reference" label="Claude Code Docs — Channels reference (permission relay)" >}}
