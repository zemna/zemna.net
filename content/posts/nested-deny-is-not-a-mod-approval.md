---
title: "A Nested Deny Is Not a Mod Approval"
date: 2026-10-05T07:00:00+07:00
draft: false
slug: "nested-deny-is-not-a-mod-approval"
description: "A user-installed mod that approves one nested piece of a compound shell is not proof deny is off. Print the nested rule, the approval source, and the named Claude Code owner before you file allow-broken."
topics: ["ai-agents"]
tags: ["claude-code", "permissions", "nested-deny", "coding-agents", "change-control", "managed-settings"]
cover: /covers/nested-deny-is-not-a-mod-approval.png
seo:
  primaryQuery: "Claude Code nested deny vs plugin approval compound shell"
  secondaryQueries:
    - "deny ask rule nested compound command managed machine"
    - "user-installed mod approval vs managed deny Claude Code"
    - "named owner for Claude Code permission ticket"
---

The junior pastes a session log. The managed machine has `Bash(git clean *)` on deny, or `Bash(rm *)` on ask. The agent ran `cd /tmp && git clean -fd`. A user-installed mod printed Approved on the inner command. They file the ticket: “deny is off. The managed allow won.”

I stop the run there. A nested deny is not a mod approval. Anthropic’s public notes that named this field are blunt: a deny or ask rule on a nested part of a compound shell command did not hold over a user-installed mod’s approval on managed machines. The inner command still had a rule. The approval source was a user-installed mod, not the named owner of Claude Code answers. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.289] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a 40-character `ghs_` check as a valid App token in [A 40-Character ghs_ Check Is Not a Valid App Token](/blog/ghs-length-is-not-a-valid-app-token/). I already refused to treat a redirected dangerous `rm` as always-ask off in [Print the Redirect Before You File Always-Ask Off](/blog/print-the-redirect-before-you-file-always-ask-off/). This post is the same desk rule for a compound shell. Print the nested rule. Print the approval source. Name who owns the Claude Code answers.

The question is not whether the inner command ran. The question is whether the named owner can still tell a nested deny from a plugin that approved the inner piece.

<!--more-->

![Three columns: Nested deny, Plugin approval, Named owner](/img/nested-deny-is-not-a-mod-approval-1.png)

## The ticket that looks like deny-is-off

Juniors treat a compound shell the way they treat a single button. Yesterday `git clean -fd` prompted. Today `cd /tmp && git clean -fd` ran after a mod said Approved. They page the desk: “managed settings died” or “sandbox auto-allow ate the deny.”

Two jobs collide on that line.

1. **Keep the nested rule honest.** Official docs: Claude Code is aware of shell operators. A rule like `Bash(safe-cmd *)` does not give permission to run `safe-cmd && other-cmd`. Recognized separators are `&&`, `||`, `;`, `|`, `|&`, `&`, and newlines. A rule must match each subcommand independently. Deny and ask rules apply when any subcommand matches them, including a command nested inside a subshell, a command substitution, or a control-flow body such as a `for` loop. An ask rule like `Bash(git clean *)` still prompts for `cd /tmp && git clean -f` or `echo "$(git clean -f)"`, even in auto mode. [Source: https://code.claude.com/docs/en/permissions]
2. **Keep the approval source named.** The 3 October 2026 changelog: a deny or ask rule on a nested part of a compound shell command did not hold over a user-installed mod’s approval on managed machines. That is the field. It is not “deny is off.” It is not “the managed machine allow won.” [Source: https://code.claude.com/docs/en/changelog] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.289]

If you only screenshot “Approved,” you will file allow-broken. You will not file the nested rule.

{{< note type="warning" title="Do not file deny-is-off on a nested approval" >}}
If a coding agent or a junior says deny is off because a user-installed mod approved one nested piece of a compound shell, print the nested subcommand, the deny or ask rule that names it, the approval source (user-installed mod versus managed settings versus a human click), and one human name on the Claude Code answers. A nested deny is not a mod approval.
{{< /note >}}

I do not invent a fake overnight outage of every managed machine. I use the public contract. The nested field is the ticket, not a version pin in the title.

## What Anthropic actually named

Read the 3 October 2026 changelog, then the permissions page on compound commands, then the settings page that still evaluates deny before ask before allow. Do not trust a social recap. Do not trust this post without those pages.

The named field, published 3 October 2026:

> Fixed a deny or ask rule on a nested part of a compound shell command not holding over a user-installed mod's approval on managed machines

That sentence has three parts. Print all three on the ticket.

| Part | What it is | What it is not |
| --- | --- | --- |
| Nested deny or ask | A rule that matches one subcommand inside `&&`, `\|\|`, `;`, a pipe, a subshell, or a substitution | Proof the whole compound string is allowed |
| User-installed mod approval | An installed mod that approved the inner tool call | A managed-settings allow, a human “Yes”, or sandbox auto-allow |
| Managed machine | The machine still has managed settings | Proof managed deny was deleted |

Official evaluation order does not change because a plugin liked the inner command. Claude Code evaluates deny rules first, then ask, then allow. The first match decides regardless of how specific each rule is. An allow rule cannot carve an exception out of a deny rule. The same precedence applies between ask and allow: a matching ask rule prompts even when a more specific allow rule also matches the same call. [Source: https://code.claude.com/docs/en/permissions] [Source: https://code.claude.com/docs/en/settings-reference]

On managed machines, deny rules and managed hooks take precedence where the guard loads. A user’s mod cannot approve a call that a deny rule refuses, unless an admin explicitly sets `allowModsToOverrideDenyRules`. Other permission checks can be overridden: a user’s mod that approves tool calls can approve a call that an ask rule would prompt for. That is why the changelog names deny **or ask** on the nested part. Print which list held the rule. [Source: https://code.claude.com/docs/en/plugins/mods/admin] [Source: https://code.claude.com/docs/en/changelog]

{{< details summary="Where the pin sits after the decision, not in the title" >}}
The GitHub release tag that published this line is dated 2026-10-03T23:07:17Z, prerelease false, Latest at the time this desk read the API. The docs changelog lists the same bullet under 2.1.289, October 3, 2026. npm `latest` for `@anthropic-ai/claude-code` moved with that tag. npm `stable` at 2.1.285 is not this field. Do not put the tag in the title. Do not treat `stable` as the nested-deny field. Neighbor bullets in the same release (Read deny through a symlink, plugin rewrite of org MCP sign-in copy, env-prefix Bash) are other tickets. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.289] [Source: https://code.claude.com/docs/en/changelog]
{{< /details >}}

## Four checks before you file

A mid-senior screenshots this list. A junior who only has the log still has a ticket they can close.

1. **Print the nested subcommand, not the whole paste.** If the log shows `cd /tmp && git clean -fd`, the ticket is `git clean -fd`, not “the compound ran.” Official docs: each subcommand matches independently. [Source: https://code.claude.com/docs/en/permissions]
2. **Print deny versus ask.** If the rule is on `deny`, a user-installed mod is not supposed to approve it where the managed guard loads. If the rule is on `ask`, a user-installed mod can approve a call that would have prompted. Those are different tickets. [Source: https://code.claude.com/docs/en/plugins/mods/admin]
3. **Print the approval source.** User-installed mod, managed settings, human click, or sandbox auto-allow. Do not collapse them into “the agent said yes.”
4. **Write one human name.** `CLAUDE_CODE_PERMISSION_OWNER`. A coding agent does not own the permission answers. A Slack channel does not own them.

![Four checks: Nested subcommand, Deny vs ask, Approval source, Named owner](/img/nested-deny-is-not-a-mod-approval-2.png)

Those four lines are the whole post. Everything below is how you print them without turning this page into a deny-bypass recipe.

## Print the nested piece without running the command

Do not paste a live `git clean -fd` into production to “prove” the nested field. Do not write a recipe that hides `rm` behind `&&`. The public changelog already states the field. You need a classifier on a logged command string, plus synthetic fixtures.

Copy this probe. It classifies a string. It never runs a shell. It never approves a tool.

```python
#!/usr/bin/env python3
"""Classify a compound Bash line. Never execute. Never approve."""
from __future__ import annotations

import re
import sys

SEPARATORS = re.compile(r"&&|\|\||;|\|&|\||&")
DENY_NEEDLES = ("git clean", "rm -", "rmdir ", "dd if=", "mkfs")
ASK_NEEDLES = ("git push", "git reset --hard", "kubectl delete")


def split_subcommands(line: str) -> list[str]:
    parts = SEPARATORS.split(line)
    return [p.strip() for p in parts if p.strip()]


def classify_piece(piece: str) -> str:
    low = piece.lower()
    if any(n in low for n in DENY_NEEDLES):
        return "deny_candidate"
    if any(n in low for n in ASK_NEEDLES):
        return "ask_candidate"
    return "other"


def classify(line: str) -> dict[str, object]:
    pieces = split_subcommands(line)
    rows = [{"piece": p, "class": classify_piece(p)} for p in pieces]
    nested = [r for r in rows if r["class"] != "other"]
    return {
        "raw_len": len(line),
        "piece_count": len(pieces),
        "nested_hits": nested,
        "this_field": bool(nested) and len(pieces) > 1,
    }


def main() -> int:
    line = sys.stdin.read().strip()
    result = classify(line)
    print(f"piece_count={result['piece_count']} this_field={result['this_field']}")
    for row in result["nested_hits"]:
        print(f"{row['class']}: {row['piece'][:120]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Feed it a log line, not a live command:

```bash
printf '%s\n' 'cd /tmp && git clean -fd' | python3 probe_nested_deny.py
# piece_count=2 this_field=True
# deny_candidate: git clean -fd
```

If `this_field=False`, do not file this post’s ticket. File a single-command deny, sandbox auto-allow, or a different prefix.

The probe’s needle lists are **desk examples**. They are not your production deny file. Replace them with the rules the named owner already shipped. Do not add a needle that teaches a hide path.

## Print deny, ask, and owner in settings you already own

Official settings still look like this. This is the documented shape. It is not a bypass. Fill the patterns your owner already named. Do not add a nested hide.

```json
{
  "permissions": {
    "deny": ["Bash(git clean *)", "Bash(rm *)"],
    "ask": ["Bash(git push *)"],
    "allow": ["Bash(git diff *)"]
  }
}
```

[Source: https://code.claude.com/docs/en/settings-reference]

Rules are evaluated deny, then ask, then allow. `--allowedTools` adds allow rules for one session, and a deny rule from any settings file still blocks a tool it names. Claude Code applies allow rules from a project’s `.claude/settings.json` only after you accept the workspace trust dialog for that folder. [Source: https://code.claude.com/docs/en/settings-reference]

On the ticket, paste **which file** held the nested rule: managed settings, project settings, or user settings. If a tool is denied at any level, no other level can allow it. A managed settings deny cannot be overridden by `--allowedTools`. That precedence is between settings files and command line arguments. For whether a deny rule holds over a mod you install, the permissions page points at the mods admin notes. [Source: https://code.claude.com/docs/en/permissions]

Write the owner next to the file path:

```python
#!/usr/bin/env python3
"""Print a nested-deny ticket. Never execute the command. Never approve."""
from __future__ import annotations

import json
import os
from pathlib import Path

OWNER_ENV = "CLAUDE_CODE_PERMISSION_OWNER"


def load_permissions(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    perms = data.get("permissions") or {}
    return {
        "deny": list(perms.get("deny") or []),
        "ask": list(perms.get("ask") or []),
        "allow": list(perms.get("allow") or []),
    }


def main() -> int:
    owner = os.environ.get(OWNER_ENV, "").strip()
    settings = Path(os.environ.get("CLAUDE_SETTINGS_PATH", "settings.json"))
    nested = os.environ.get("NESTED_SUBCOMMAND", "").strip()
    approval_source = os.environ.get("APPROVAL_SOURCE", "unknown").strip()
    perms = load_permissions(settings) if settings.is_file() else {"deny": [], "ask": [], "allow": []}
    print(f"owner={owner or 'MISSING'}")
    print(f"settings={settings}")
    print(f"nested={nested[:160]}")
    print(f"approval_source={approval_source}")
    print(f"deny_count={len(perms['deny'])} ask_count={len(perms['ask'])}")
    if not owner:
        print("ticket=owner_missing")
        return 2
    if not nested:
        print("ticket=nested_missing")
        return 2
    print("ticket=print_nested_vs_mod_then_owner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If `owner` is empty, the ticket is “owner missing,” not “deny is off.” If `nested` is empty, the ticket is “paste the inner command,” not “managed allow won.”

![Flow: Split line, Nested hit, Deny or ask, Owner](/img/nested-deny-is-not-a-mod-approval-3.png)

## Neighbor tickets that are not this field

Print these so a junior does not collapse every Claude Code permission headline into nested deny.

1. **Read deny through a symlink.** Same release, different field: `Read` deny rules not applying to files @-mentioned, changed, or selected in the IDE through a symlink. That is a path spelling ticket. It is not a compound shell. Sunday social already used that field. Do not clone it here. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.289]
2. **Env prefix in front of a denied command.** Same release: Bash deny and ask rules missing a command behind an environment variable prefix with an expanded value (example in the notes: `TZ="$HOME" rm -rf build`) when the sandbox auto-allows commands. That is sandbox auto-allow plus a prefix, not a nested `&&` piece. [Source: https://code.claude.com/docs/en/changelog]
3. **Plugin rewrite of org MCP sign-in copy.** Same release: a user-installed plugin being able to rewrite the descriptions of an organization-managed MCP server’s sign-in tools. That is login copy, not a nested Bash deny. Leave it for the leftover social slot. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.289]
4. **Sandbox auto-allow on inline `python3 -c`.** Already a post. [Source: https://zemna.net/blog/sandbox-auto-allow-is-not-a-retry-tax-on-equals/]
5. **Redirected `rm`, `ghs_` length, Copilot approve.** Already posts. Do not fold them into this ticket. [Source: https://zemna.net/blog/print-the-redirect-before-you-file-always-ask-off/] [Source: https://zemna.net/blog/ghs-length-is-not-a-valid-app-token/] [Source: https://zemna.net/blog/leave-copilot-approve-off/]

If the log says the inner `git clean` matched a deny rule and a **user-installed mod** printed Approved on a **managed** box, you are on this field. If the log says a symlink @-mention read a denied file, you are on neighbor 1.

Scan the repo for compound separators next to deny needles. Do not execute the hits.

```python
#!/usr/bin/env python3
"""Find logged compound lines near deny needles. Never execute hits."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(".")
NEEDLES = ("git clean", "&& rm ", "; rm ", "| rm ")
SEPARATOR_HINTS = ("&&", "||", ";", "|")


def main() -> int:
    hits = 0
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".log", ".md", ".txt", ".json"}:
            continue
        if any(part in {".git", "node_modules", "vendor"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if not any(s in line for s in SEPARATOR_HINTS):
                continue
            if any(n in line.lower() for n in NEEDLES):
                print(f"{path}:{i}:{line.strip()[:160]}")
                hits += 1
    print(f"hits={hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If the scan prints nothing, do not file this post’s ticket. File a missing owner, a missing settings path, or a neighbor field.

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a managed Claude Code box for the desk, a junior who installed a quality-of-life mod that auto-approves “safe looking” Bash, and a deploy script that still contains `cd storage && git clean -fd` in a comment the agent copied into a real command. I treat `CLAUDE_CODE_PERMISSION_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “did a user-installed mod approve a nested piece that deny or ask already named.” A coding agent does not get to close an allow-broken ticket because the inner command ran. I already wrote the sibling rule for a redirect that is not always-ask off, and for a length check that is not a valid App token. This is the sibling for a nested deny that is not a mod approval.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File “deny is off” without printing the nested subcommand, deny versus ask, the approval source, and one human name.
2. Put the release tag, `2.1.289`, or `3 October 2026` in the title as a version-style hook. The numbers are evidence after the decision.
3. Write a deny-bypass or mod-bypass recipe: hiding `rm` behind `&&`, wrapping a denied command in `bash -c`, forging an approval, or setting `allowModsToOverrideDenyRules` because a junior was annoyed.
4. Recommend buying a scanner, a seat, or a plan because a nested piece ran.
5. Treat npm `stable` as this field. The public Latest notes that named the nested line are not the `stable` dist-tag.
6. Mix this field with symlink Read, env-prefix sandbox, MCP sign-in copy, sandbox-equals, redirected `rm`, or `ghs_` length. Those are other posts.
7. Clone the lockfile, redirected-rm, sandbox-equals, runner-deadline, or ghs_ posts as a synonym. Those URLs already shipped.
8. Paste a live production command that deletes files in order to demo the classifier.
9. Let a coding agent own `CLAUDE_CODE_PERMISSION_OWNER`, or collapse ask and deny into one ticket.

Allowed:

1. Print the inner subcommand, redacted if it holds a path you do not want in Slack.
2. Classify synthetic fixtures with `probe_nested_deny.py`. Do not execute them.
3. Scan logs for compound separators next to deny needles.
4. Name one human as `CLAUDE_CODE_PERMISSION_OWNER`.
5. Keep deny, ask, and allow in the documented order. Do not invent a fourth list.
6. Keep symlink Read, env-prefix, and MCP sign-in copy as separate tickets.
7. After the owner prints the four lines, update the managed settings file they already own. Do not add a hide path.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about nested deny is not permission to skip the four lines.

![Print four lines: Nested subcommand, Deny or ask, Approval source, Owner](/img/nested-deny-is-not-a-mod-approval-4.png)

## What you should do Monday morning

1. Open the repo that actually runs Claude Code on a managed machine. Export `CLAUDE_CODE_PERMISSION_OWNER` to a human name. Export `CLAUDE_SETTINGS_PATH` to the managed settings file. Run the ticket printer. Write `this_field=True` or `False` on the ticket next to that name.
2. For every `this_field=True` row, answer in one sentence: a user-installed mod approved a nested subcommand that deny or ask already named, or the inner command ran for another reason. If you cannot answer, the ticket is “owner missing,” not “deny is off.”
3. Print deny versus ask for that inner command. If it is deny, the mods admin notes say a user-installed mod is not supposed to approve it where the guard loads, unless an admin set `allowModsToOverrideDenyRules`. If it is ask, a user-installed mod can approve a call that would have prompted. Split those tickets. [Source: https://code.claude.com/docs/en/plugins/mods/admin]
4. Confirm coding-agent instructions on this desk name the same owner and forbid “deny is off” without the four lines. Forbid executing a live `git clean` or `rm` to demo. Forbid writing a hide path behind `&&`.
5. Confirm compound matching still uses the documented separators (`&&`, `||`, `;`, `|`, `|&`, `&`, newlines) and that each subcommand matches independently. Do not invent a parser that “fixes” deny by joining the string back together. [Source: https://code.claude.com/docs/en/permissions]
6. Leave symlink Read, env-prefix sandbox, and MCP sign-in copy off this ticket. Those are neighbor fields from the same public notes. Do not steal them as a second heading.

The question is not whether the changelog demos well in a gist. The question is whether the named owner can still tell a nested deny from a plugin that approved the inner piece after handoff.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.289" label="GitHub — Claude Code v2.1.289 release notes" >}}

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code Docs — Changelog" >}}

{{< source href="https://code.claude.com/docs/en/permissions" label="Claude Code Docs — Configure permissions" >}}
