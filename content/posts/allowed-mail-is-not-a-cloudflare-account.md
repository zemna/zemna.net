---
title: "An Allowed-Mail List Is Not a Cloudflare Account"
date: 2026-10-06T07:00:00+07:00
draft: false
slug: "allowed-mail-is-not-a-cloudflare-account"
description: "A trycloudflare.com URL with --allowed-mail is email OTP on a Quick Tunnel, not a Cloudflare account on either side. Print allowed-mail, account, and the named Tunnel owner before you file Access-broken."
topics: ["tutorials"]
tags: ["cloudflare", "cloudflared", "quick-tunnels", "allowed-mail", "coding-agents", "change-control"]
cover: /covers/allowed-mail-is-not-a-cloudflare-account.png
seo:
  primaryQuery: "cloudflare allowed-mail quick tunnel"
  secondaryQueries:
    - "trycloudflare allowed-mail not an account"
    - "protected quick tunnels email otp"
    - "named owner for cloudflared allowed-mail ticket"
---

The junior pastes a screenshot. The coding agent shared a `trycloudflare.com` URL. The visitor typed an email, hit a Cloudflare Access page, and stalled. Chat files the ticket: “the visitor needs a Cloudflare account. Access is misconfigured.”

I stop the run there. An allowed-mail list is not a Cloudflare account. Cloudflare’s public notes that named this field are blunt: `--allowed-mail` on `cloudflared` restricts a Quick Tunnel to the email addresses and domains you list. Visitors authenticate with a one-time PIN. Nobody on either side needs a Cloudflare account. Access ends when you stop the process. That is email OTP on a Quick Tunnel. It is not production Access on a named Tunnel. It is not a dashboard login. [Source: https://blog.cloudflare.com/protected-quick-tunnels/] [Source: https://developers.cloudflare.com/changelog/post/2026-10-02-protected-quick-tunnels/]

I already refused to treat a nested deny as a mod approval in [A Nested Deny Is Not a Mod Approval](/blog/nested-deny-is-not-a-mod-approval/), a 40-character `ghs_` check as a valid App token in [A 40-Character ghs_ Check Is Not a Valid App Token](/blog/ghs-length-is-not-a-valid-app-token/), and a redirected dangerous `rm` as always-ask off in [Print the Redirect Before You File Always-Ask Off](/blog/print-the-redirect-before-you-file-always-ask-off/). This post is the same desk rule for a shared preview URL. Print the guest list. Print whether a Cloudflare account exists. Name who owns the tunnel answers.

The question is not whether the Access page looked official. The question is whether the named owner can still tell an allowed-mail list from a Cloudflare account.

<!--more-->

![Three columns: Allowed-mail list, Cloudflare account, Named Tunnel owner](/img/allowed-mail-is-not-a-cloudflare-account-1.png)

## The ticket that looks like Access-is-broken

Juniors treat a Cloudflare Access page the way they treat a login wall. Yesterday anyone with the `trycloudflare.com` link opened the local Vue preview. Today the same kind of URL asks for an email and a PIN. They page the desk: “someone turned on Zero Trust” or “the visitor must create a Cloudflare account.”

Two jobs collide on that URL.

1. **Keep the guest list honest.** Official changelog, 2 October 2026: use `--allowed-mail` so visitors authenticate with a one-time PIN sent to their email before they reach the local service. You can allow one address, several addresses, or every address on a domain. Visitors do not need a Cloudflare account. Access ends for everyone when you stop `cloudflared`. [Source: https://developers.cloudflare.com/changelog/post/2026-10-02-protected-quick-tunnels/]
2. **Keep the product named.** Official Quick Tunnels docs: a Quick Tunnel is a temporary `trycloudflare.com` URL for a local service. You do not need a Cloudflare account or a domain. A named Cloudflare Tunnel with Cloudflare Access is a different product: stable hostname, account, richer identity-provider rules. [Source: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/] [Source: https://blog.cloudflare.com/protected-quick-tunnels/]

If you only screenshot “Cloudflare Access,” you will file Access-broken. You will not file the guest list.

{{< note type="warning" title="Do not file Access-broken on an allowed-mail preview" >}}
If a coding agent or a junior says the visitor needs a Cloudflare account because a `trycloudflare.com` URL showed an Access page, print whether `--allowed-mail` was on the command, whether any Cloudflare account exists on either side, and one human name on the tunnel answers. An allowed-mail list is not a Cloudflare account.
{{< /note >}}

I do not invent a fake overnight outage of every named Tunnel. I use the public contract. The guest-list field is the ticket, not a version pin in the title.

## What Cloudflare actually named

Read the 2 October 2026 changelog, then the Quick Tunnels page, then the blog post that explains why the guest list lives on your machine. Do not trust a social recap. Do not trust this post without those pages.

The named field, published 2 October 2026:

> Use the new `--allowed-mail` flag in `cloudflared` to require visitors to authenticate with a one-time PIN sent to their email before they reach your local service.

That sentence has three parts. Print all three on the ticket.

| Part | What it is | What it is not |
| --- | --- | --- |
| Allowed-mail list | Email addresses or a domain pattern you passed to `--allowed-mail` | Proof the visitor has a Cloudflare login |
| Email OTP | A one-time PIN sent to that mailbox through Cloudflare Access | Production Access on a named hostname |
| Quick Tunnel | A temporary `trycloudflare.com` URL that dies when the process exits | A named Tunnel in an account, with DNS and an SLA |

Official docs keep the flag shapes small. A single address: `--allowed-mail alice@example.com`. Several addresses: repeat the flag, or pass a comma-separated list. A whole domain: `--allowed-mail '*@example.com'` with quotes so the shell does not expand the star. [Source: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/]

The blog is equally blunt on what this is not. If you leave out `--allowed-mail`, public Quick Tunnels behave as they always have: anyone with the link can open it. To change who can get in, stop `cloudflared` and start a new tunnel. For a stable hostname or richer rules such as identity-provider groups, use Cloudflare Tunnel with Cloudflare Access. [Source: https://blog.cloudflare.com/protected-quick-tunnels/]

{{< details summary="Where the pin sits after the decision, not in the title" >}}
Cloudflare’s blog says the flag starts with `cloudflared` 2026.9.3. The public changelog that named the field is dated 2 October 2026. GitHub’s `cloudflare/cloudflared` tag `2026.9.3` is dated 2026-09-24. This desk’s GitHub read on 6 October 2026 also showed a later tag `2026.10.0` dated 2026-10-05. Do not put any of those tags in the title. Do not treat a checksum-only GitHub body as the feature notes. Neighbor products in the same week (named Tunnel plus Access, Cloudflare Mesh, workers.dev cutover) are other tickets. [Source: https://blog.cloudflare.com/protected-quick-tunnels/] [Source: https://github.com/cloudflare/cloudflared/releases/tag/2026.9.3] [Source: https://github.com/cloudflare/cloudflared/releases/tag/2026.10.0]
{{< /details >}}

## Four checks before you file

A mid-senior screenshots this list. A junior who only has the agent log still has a ticket they can close.

1. **Print whether `--allowed-mail` was on the command.** If the log is a bare `cloudflared tunnel --url http://localhost:5173`, the field is a public Quick Tunnel. Anyone with the URL can open it. If the log holds `--allowed-mail`, the field is a guest list plus email OTP. [Source: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/]
2. **Print Cloudflare account versus guest list.** Official changelog: visitors do not need a Cloudflare account. The blog: nobody on either side needs a Cloudflare account. A named Tunnel with Access lives in an account. Those are different tickets. [Source: https://developers.cloudflare.com/changelog/post/2026-10-02-protected-quick-tunnels/] [Source: https://blog.cloudflare.com/protected-quick-tunnels/]
3. **Print who owns the process.** Access ends when you stop `cloudflared`. The person who started the process owns the guest list. A Slack channel does not own it. A coding agent does not own it.
4. **Write one human name.** `TUNNEL_PREVIEW_OWNER`. That name answers “is this allowed-mail, or did we file Access-broken on a Quick Tunnel.”

![Four checks: Flag on command, Account vs guest list, Process owner, Named human](/img/allowed-mail-is-not-a-cloudflare-account-2.png)

Those four lines are the whole post. Everything below is how you print them without turning this page into a tunnel-bypass recipe.

## Print the guest list without printing the emails

Do not paste a live production app behind a public Quick Tunnel to “prove” the field. Do not write a recipe that strips `--allowed-mail` so a reviewer can skip the PIN. The public changelog already states the field. You need a classifier on a logged command string, plus synthetic fixtures.

Copy this probe. It classifies a string. It never starts `cloudflared`. It never prints the addresses.

```python
#!/usr/bin/env python3
"""Classify a cloudflared argv line. Never execute. Never print emails."""
from __future__ import annotations

import shlex
import sys


def _is_mail_flag(token: str) -> bool:
    return token in {"--allowed-mail", "-allowed-mail"}


def classify(line: str) -> dict[str, object]:
    try:
        tokens = shlex.split(line, posix=True)
    except ValueError:
        return {
            "ok": False,
            "reason": "unparsed_argv",
            "has_allowed_mail": False,
            "rule_count": 0,
            "has_url": False,
            "looks_like_quick_tunnel": False,
        }

    has_url = "--url" in tokens or "quick-start" in tokens
    looks_quick = "tunnel" in tokens and has_url and "create" not in tokens
    rule_count = 0
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if _is_mail_flag(tok):
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                chunk = tokens[i + 1]
                rule_count += max(1, len([p for p in chunk.split(",") if p.strip()]))
                i += 2
                continue
            rule_count += 1
        elif tok.startswith("--allowed-mail="):
            chunk = tok.split("=", 1)[1]
            rule_count += max(1, len([p for p in chunk.split(",") if p.strip()]))
        i += 1

    return {
        "ok": True,
        "has_allowed_mail": rule_count > 0,
        "rule_count": rule_count,
        "has_url": has_url,
        "looks_like_quick_tunnel": looks_quick,
        "this_field": bool(looks_quick and rule_count > 0),
        "public_quick_tunnel": bool(looks_quick and rule_count == 0),
    }


def main() -> int:
    line = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    row = classify(line.strip())
    print(
        "this_field={this_field} public_quick_tunnel={public_quick_tunnel} "
        "rule_count={rule_count} looks_like_quick_tunnel={looks_like_quick_tunnel}".format(
            **row
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it against fixtures. Do not feed it a live token. Do not start a tunnel.

```bash
python3 probe_allowed_mail.py 'cloudflared tunnel --url http://localhost:5173'
python3 probe_allowed_mail.py "cloudflared tunnel --url http://localhost:8080 --allowed-mail alice@example.com"
python3 probe_allowed_mail.py "cloudflared tunnel --url http://localhost:8080 --allowed-mail 'alice@example.com,bob@example.com'"
python3 probe_allowed_mail.py "npx wrangler tunnel quick-start http://localhost:8080 --allowed-mail alice@example.com"
```

Expected shape on this desk:

| Fixture | `this_field` | `public_quick_tunnel` | `rule_count` |
| --- | --- | --- | --- |
| Bare `--url` | False | True | 0 |
| One `--allowed-mail` | True | False | 1 |
| Comma list | True | False | 2 |
| Wrangler quick-start with the flag | True | False | 1 |

The Wrangler line is in the public blog: `npx wrangler tunnel quick-start http://localhost:8080 --allowed-mail alice@example.com`. Treat it as the same guest-list field, not a workers.dev cutover. [Source: https://blog.cloudflare.com/protected-quick-tunnels/]

Then print the ticket. Still no emails.

```python
#!/usr/bin/env python3
"""Print an allowed-mail ticket. Never start a tunnel. Never print addresses."""
from __future__ import annotations

import json
import os

from probe_allowed_mail import classify


def ticket(command: str) -> dict[str, object]:
    row = classify(command)
    owner = os.environ.get("TUNNEL_PREVIEW_OWNER", "").strip()
    account = os.environ.get("CLOUDFLARE_ACCOUNT_PRESENT", "unknown").strip()
    return {
        "owner": owner or "MISSING",
        "cloudflare_account_present": account,
        "this_field": row.get("this_field"),
        "public_quick_tunnel": row.get("public_quick_tunnel"),
        "rule_count": row.get("rule_count"),
        "wrong_ticket": "visitor_needs_cloudflare_account",
        "right_ticket": "allowed_mail_vs_account_vs_named_owner",
        "file_access_broken": False,
    }


if __name__ == "__main__":
    sample = (
        "cloudflared tunnel --url http://localhost:5173 "
        "--allowed-mail reviewer@example.com"
    )
    print(json.dumps(ticket(sample), indent=2, sort_keys=True))
```

If `owner` is `MISSING`, the ticket is “owner missing,” not “Access is broken.” If `this_field` is true and `cloudflare_account_present` is `no`, the visitor does not need a Cloudflare account. Official changelog: visitors do not need one. [Source: https://developers.cloudflare.com/changelog/post/2026-10-02-protected-quick-tunnels/]

![Logged command with redacted emails mapping to this_field, rule_count, named owner](/img/allowed-mail-is-not-a-cloudflare-account-3.png)

### What the Access page is doing

Juniors see `login.trycloudflare.com` and file “we enabled Zero Trust on the zone.” The blog splits the two questions the page answers.

1. **Authentication.** Cloudflare Access sends a one-time PIN and verifies the mailbox. That step answers only: does this person control this email address.
2. **Authorization.** `cloudflared` on your machine compares the verified address with the rules you typed. There is no Cloudflare account holding the policy. The guest list lives in the process you started. [Source: https://blog.cloudflare.com/protected-quick-tunnels/]

The same blog names the session bounds as evidence, not as a tuning guide: a single-use browser state valid for 10 minutes, then a local session for up to four hours or until you stop `cloudflared`. A protected tunnel does not fall back to public mode. `cloudflared` prints whether email authentication is on and how many rules it holds, without printing the addresses. [Source: https://blog.cloudflare.com/protected-quick-tunnels/]

The Access screenshot is the OTP half. The guest list half is still on the laptop that ran the command.

{{< note type="note" title="Named Tunnel is a different ticket" >}}
If the URL is not `trycloudflare.com`, stop. A named hostname on your zone, Cloudflare Access groups, and a dashboard application are the named-Tunnel product. Official blog: use Cloudflare Tunnel with Cloudflare Access for a stable hostname or richer rules. Do not file this post’s ticket on that hostname. Do not “fix” a named Tunnel by adding `--allowed-mail` to a Quick Tunnel command.
{{< /note >}}

Quick Tunnels also carry hard limits that do not belong on a production cutover ticket. Official docs: no uptime guarantee, at most 200 in-flight requests (extra requests return 429), and no Server-Sent Events. [Source: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/]

### Scan the agent log, then stop

You do not need to open the preview. You need to know whether the agent started a public Quick Tunnel or an allowed-mail Quick Tunnel. Scan logs. Do not start `cloudflared` from the scanner.

```python
#!/usr/bin/env python3
"""Scan text logs for Quick Tunnel commands. Never execute them."""
from __future__ import annotations

from pathlib import Path

from probe_allowed_mail import classify

ROOT = Path("logs")
NEEDLES = ("cloudflared", "trycloudflare.com", "wrangler tunnel quick-start")


def main() -> int:
    hits = 0
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".log", ".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if not any(n in line.lower() for n in NEEDLES):
                continue
            row = classify(line)
            print(
                f"{path}:{i}:this_field={row.get('this_field')} "
                f"public={row.get('public_quick_tunnel')} "
                f"rules={row.get('rule_count')}"
            )
            hits += 1
    print(f"hits={hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If the scan prints `public=True`, the ticket is a public Quick Tunnel, not Access-misconfigured. If it prints `this_field=True`, the ticket is this post. If it prints nothing, file a missing owner, a missing log, or a named-Tunnel ticket.

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: Vite on `localhost:5173`, a coding agent that already knows `cloudflared tunnel --url`, and a reviewer on a phone who only has email. I treat `TUNNEL_PREVIEW_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) also owns “did we share a public Quick Tunnel, an allowed-mail Quick Tunnel, or a named Tunnel.” A coding agent does not close an Access-broken ticket because the visitor saw a Cloudflare page.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File “the visitor needs a Cloudflare account” without printing `--allowed-mail` versus public Quick Tunnel, account versus guest list, and one human name.
2. Put `2026.9.3`, `2026.10.0`, or `2 October 2026` in the title as a version-style hook. The numbers are evidence after the decision.
3. Write a tunnel-bypass recipe: stripping `--allowed-mail`, sharing the PIN, forging the Access assertion, or mapping a way around `login.trycloudflare.com`.
4. Recommend buying Access, a Zero Trust seat, or a plan because a Quick Tunnel showed an OTP page. Official blog: email protection for Quick Tunnels is free, like Quick Tunnels themselves. [Source: https://blog.cloudflare.com/protected-quick-tunnels/]
5. Treat a named Tunnel, Cloudflare Mesh, or a workers.dev deploy as this field.
6. Mix this field with nested deny, `ghs_` length, redirected `rm`, lockfile, or sandbox-equals. Do not clone those shipped URLs.
7. Start a live public Quick Tunnel in front of production data to demo the classifier.
8. Let a coding agent own `TUNNEL_PREVIEW_OWNER`, or collapse allowed-mail and Cloudflare account into one ticket.

Allowed:

1. Print whether the flag was present. Redact addresses if a log leaked them.
2. Classify synthetic fixtures with `probe_allowed_mail.py`. Do not execute them.
3. Scan logs for `cloudflared` / `trycloudflare.com` / Wrangler quick-start.
4. Name one human as `TUNNEL_PREVIEW_OWNER`.
5. Keep Quick Tunnel, named Tunnel plus Access, and Mesh as separate tickets.
6. After the owner prints the four lines, stop the process they started if the guest list is wrong. Start a new Quick Tunnel with a new list. Official docs: you cannot edit the list in place. [Source: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/]
7. Put one line in the agent instructions file you already own: when the agent starts a Quick Tunnel, it adds `--allowed-mail` for the reviewer. The blog suggests that pattern. Check the printed rule count. Do not trust the agent to follow the line. [Source: https://blog.cloudflare.com/protected-quick-tunnels/]

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about `--allowed-mail` is not permission to skip the four lines.

## What you should do Monday morning

1. Open the repo that actually shares local previews. Export `TUNNEL_PREVIEW_OWNER` to a human name. Export `CLOUDFLARE_ACCOUNT_PRESENT` to `yes`, `no`, or `unknown`. Run the ticket printer against yesterday’s agent log. Write `this_field=True` or `False` on the ticket next to that name.
2. For every `this_field=True` row, answer in one sentence: the visitor hit email OTP on a Quick Tunnel, or they hit a named Tunnel Access policy, or they hit a public Quick Tunnel. If you cannot answer, the ticket is “owner missing,” not “Access is broken.”
3. Print public versus allowed-mail. If the command has no `--allowed-mail`, official docs still say anyone with the URL can access the local service. That is a public-share ticket. If the command has the flag, official docs say the visitor does not need a Cloudflare account. Split those tickets. [Source: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/]
4. Confirm coding-agent instructions on this desk name the same owner and forbid “visitor needs a Cloudflare account” without the four lines. Forbid starting a live public tunnel in front of production data to demo. Forbid writing a hide path around the PIN page.
5. Confirm the guest list still uses the documented shapes: one address, repeated flags, comma-separated list, or `'*@example.com'` in quotes. Do not invent a dashboard to edit the list while the process runs. Stop and start. [Source: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/]
6. Leave nested deny, `ghs_` length, redirected `rm`, named Durable Object cutover, and workers.dev off this ticket. Those are neighbor fields. Do not steal them as a second heading.

The question is not whether the changelog demos well. The question is whether the named owner can still tell an allowed-mail list from a Cloudflare account after handoff.

## Further reading

{{< source href="https://blog.cloudflare.com/protected-quick-tunnels/" label="Cloudflare Blog — Protected Quick Tunnels" >}}

{{< source href="https://developers.cloudflare.com/changelog/post/2026-10-02-protected-quick-tunnels/" label="Cloudflare Changelog — Protect Quick Tunnels with email authentication" >}}

{{< source href="https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/" label="Cloudflare Docs — Quick Tunnels" >}}
