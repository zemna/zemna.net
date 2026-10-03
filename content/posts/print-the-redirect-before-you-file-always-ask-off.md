---
title: "Print the Redirect Before You File Always-Ask Off"
date: 2026-10-03T07:00:00+07:00
draft: false
slug: "print-the-redirect-before-you-file-always-ask-off"
description: "A missing always-ask prompt on a dangerous rm is not proof always-ask is off. Print the redirect, the prompt, and the named Claude Code owner before you file the ticket."
topics: ["software-engineering"]
tags: ["claude-code", "always-ask", "rm", "permissions", "coding-agents", "change-control"]
cover: /covers/print-the-redirect-before-you-file-always-ask-off.png
seo:
  primaryQuery: "Claude Code redirected rm always-ask"
  secondaryQueries:
    - "dangerous rm tilde redirect permission"
    - "always-ask dropped on wildcard redirect"
    - "named owner for Claude Code always-ask"
---

The junior pastes a terminal screenshot. The coding agent ran a delete. There was no always-ask prompt. They file the ticket: “always-ask is off, so this rm is allowed.”

I stop the run there. Print the full command, including the redirect, before you file always-ask off. The public Claude Code notes that named this field are blunt: a dangerous `rm` on `/` or the home directory lost its always-ask safeguard when the same command also redirected output to a `~` or wildcard path. That is a redirect on the same line, not a named allow and not a missing setting. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.287] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a NUL byte in a permission rule as a wildcard allow in [A NUL Byte in a Permission Rule Is Not a Wildcard Allow](/blog/a-nul-byte-in-a-permission-rule-is-not-a-wildcard/). I already refused to treat sandbox auto-allow as a retry tax on equals in [Sandbox Auto-Allow Is Not a Retry Tax on Equals in Inline Scripts](/blog/sandbox-auto-allow-is-not-a-retry-tax-on-equals/). I already refused to treat Copilot’s ready-to-approve line as a required merge vote in [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/). This post is the same desk rule for always-ask on a dangerous delete. Print the redirect. Print whether always-ask still fired. Name who owns the always-ask answers.

The question is not whether the prompt appeared. The question is whether the named owner can still tell a tilde redirect from a setting that is actually off.

<!--more-->

![Three columns: Redirect, Always-ask, Named owner](/img/print-the-redirect-before-you-file-always-ask-off-1.png)

## The ticket that looks like always-ask is off

Juniors treat a missing prompt the way they treat a broken lock. Yesterday the same `rm` stopped and asked. Today the agent appended `> ~/agent.log` or `2> *.log`. The prompt vanished. They page the desk: “always-ask is off.”

Two jobs collide on that line.

1. **Stop a dangerous delete long enough for a human.** Official permission-mode docs: removals targeting a critical path still prompt as a circuit breaker. Root and home directory removals such as `rm -rf /` still prompt even when other permission prompts are skipped. [Source: https://code.claude.com/docs/en/permissions] [Source: https://code.claude.com/docs/en/permission-modes]
2. **Keep the safeguard honest when the same line also writes a file.** The public fix names the old matcher: always-ask dropped when that dangerous `rm` also redirected output to a `~` or wildcard path. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.287]

If you only screenshot “it did not ask,” you will file always-ask-broken. You will not file the redirect.

{{< note type="warning" title="Do not file always-ask off on a missing prompt" >}}
If a coding agent or a junior says always-ask is off because a delete ran, print the full command including `>` `>>` and `2>`, whether the path used `~` or a wildcard, whether always-ask still fires on the same `rm` without that redirect, and one human name on the always-ask answers. A missing prompt is not a named allow.
{{< /note >}}

I do not invent a fake overnight wipe of `/`. I use the public contract. The redirect field is the ticket, not a version pin in the title.

## What the public notes actually named

Read the GitHub release body for the tag that named this field, then read the same line on the official changelog. Do not trust a social recap. Do not trust this post without those two pages.

The named field, published 1 October 2026, prerelease false:

> Fixed a dangerous `rm` (such as one on `/` or the home directory) losing its always-ask safeguard when the same command also redirected output to a `~` or wildcard path.

[Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.287] [Source: https://code.claude.com/docs/en/changelog]

That sentence has three parts. Print all three on the ticket.

| Part | What it is | What it is not |
| --- | --- | --- |
| Dangerous `rm` | A delete aimed at `/` or the home directory | Every `rm` in a build script |
| Always-ask safeguard | The circuit-breaker prompt on that class of delete | A `permissions.allow` line you thought you wrote |
| Redirect to `~` or wildcard | `>` `>>` `2>` into a home path or a glob | A second command on a later line |

The junior ticket collapses those three parts into one: “always-ask is off.” That collapse is the bug in the ticket, not a setting you then turn back on.

Official permissions docs still say permission rules are enforced by Claude Code, not by the model. Instructions in a prompt or `CLAUDE.md` shape what Claude tries. They do not change what Claude Code allows. [Source: https://code.claude.com/docs/en/permissions]

So a `CLAUDE.md` line that says “always ask before rm” is not this field. A missing prompt on a redirected dangerous `rm` is this field.

{{< details summary="Where the pin sits after the decision, not in the title" >}}
The GitHub tag that named the redirect field is v2.1.287, published 2026-10-01T18:00:22Z, prerelease false. npm dist-tags on the morning of this post: `latest` 2.1.288, `stable` 2.1.285, `next` 2.1.288. The later tag names a different field: a dangerous `rm` inside `bash -c` or `sh -c` running without a prompt in bypassPermissions mode or under a shell allow rule. Do not merge those two fields. Do not put either pin in the title. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.287] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.288] [Source: https://registry.npmjs.org/@anthropic-ai/claude-code]
{{< /details >}}

## Four checks before you file

A mid-senior screenshots this list. A junior who only has the screenshot still has a ticket they can close.

1. **Print the full command as one string.** Include every redirect. If the log truncates at the first `|` or `>`, the log is the ticket, not always-ask.
2. **Mark `~` or a wildcard on the redirect target.** Home expansion and globs are the named field. A redirect into `./build/agent.log` is a different ticket until you prove otherwise.
3. **Replay the same `rm` as a string compare, without the redirect, in a dry log.** If always-ask still fires on the dry form and vanished on the redirected form, you have this field. If always-ask is absent on both, you have a mode or allow-rule ticket.
4. **Write one human name.** `CLAUDE_CODE_ALWAYS_ASK_OWNER`. A coding agent does not own the always-ask answers. A Slack channel does not own them.

![Four checks: Full command, Tilde or glob, Dry compare, Named owner](/img/print-the-redirect-before-you-file-always-ask-off-2.png)

Those four lines are the whole post. Everything below is how you print them without turning this page into a delete recipe.

## Print the redirect without running the delete

Do not run `rm -rf /` to “prove” the old matcher. Do not run `rm -rf ~`. The public release already states the old matcher. You need a parser on a logged command string.

Copy this probe. It classifies a string. It does not call `rm`.

```python
#!/usr/bin/env python3
"""Classify a logged shell string. Never execute it."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REDIRECT = re.compile(r"(?:^|\s)(?:[0-9]*)>>?\s*(\S+)|(?:^|\s)(?:[0-9]*)>\s*(\S+)")
DANGEROUS_RM = re.compile(r"\brm\b.*(?:\s/|\s~(?:/|\s|$)|\$HOME)", re.I)


def classify(command: str) -> dict[str, bool | str]:
    targets = [t for pair in REDIRECT.findall(command) for t in pair if t]
    tilde_or_glob = any(
        t.startswith("~") or "*" in t or "?" in t or t.startswith("$HOME")
        for t in targets
    )
    return {
        "dangerous_rm": bool(DANGEROUS_RM.search(command)),
        "has_redirect": bool(targets),
        "redirect_targets": " ".join(targets),
        "tilde_or_glob_redirect": tilde_or_glob,
        "this_field": bool(DANGEROUS_RM.search(command) and tilde_or_glob),
    }


def main() -> int:
    raw = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else sys.stdin.read()
    row = classify(raw.strip())
    for key, value in row.items():
        print(f"{key}={value}")
    if row["this_field"]:
        print("ticket=redirect_dropped_always_ask")
        return 2
    if row["dangerous_rm"] and not row["has_redirect"]:
        print("ticket=dangerous_rm_without_redirect")
        return 1
    print("ticket=not_this_field")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

A fixture file is enough. Put the logged command in `logged-command.txt`. Run the probe against the file. Paste the four printed keys onto the ticket next to the owner name.

```python
# tests/test_redirect_always_ask_probe.py
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location(
    "probe", Path(__file__).resolve().parents[1] / "scripts" / "probe_redirect_always_ask.py"
)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def test_tilde_redirect_is_this_field():
    row = probe.classify("rm -rf / > ~/agent.log")
    assert row["dangerous_rm"] is True
    assert row["tilde_or_glob_redirect"] is True
    assert row["this_field"] is True


def test_wildcard_redirect_is_this_field():
    row = probe.classify("rm -rf $HOME 2> /tmp/*.log")
    assert row["this_field"] is True


def test_plain_build_rm_is_not_this_field():
    row = probe.classify("rm -rf ./build")
    assert row["this_field"] is False
    assert row["dangerous_rm"] is False
```

Those tests never delete a file. They pin the classifier. If a junior changes the regex to “any `rm`,” the build_rm test fails. That is the point.

{{< note type="danger" title="This page is not a delete recipe" >}}
Do not paste a live `rm` against `/` or the home directory to reproduce the old matcher. Do not write a bypass. Do not set an environment variable to silence a dangerous-rm prompt as a demo. Classify the logged string. Leave the filesystem alone.
{{< /note >}}

## Ask rules, permission modes, and critical-path rm

Always-ask on a dangerous delete sits next to ordinary permission rules. Do not pretend they are the same list.

Official permissions docs: rules follow `Tool` or `Tool(specifier)`. A scoped rule such as `Bash(rm *)` leaves the tool available and blocks matching calls. Deny, then ask, then allow. The first match in that order wins. [Source: https://code.claude.com/docs/en/permissions]

Copy the docs example as a probe of the lists, not as a bypass recipe.

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)"
    ],
    "deny": [
      "Bash(git push *)",
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  }
}
```

[Source: https://code.claude.com/docs/en/permissions] [Source: https://code.claude.com/docs/en/settings]

That JSON is not this field. A `Bash(rm *)` deny is a deny. An ask rule that names `git clean` is an ask rule. Official docs: an ask rule like `Bash(git clean *)` still prompts for `cd /tmp && git clean -f` even in auto mode. [Source: https://code.claude.com/docs/en/permissions]

The redirect field is the circuit breaker on a dangerous `rm` that still has to ask after those lists. Official permission-mode docs: `rm` and `rmdir` removals targeting a critical path, which no allow rule or PreToolUse hook `"allow"` approves. In `bypassPermissions`, root and home directory removals still prompt as a circuit breaker. [Source: https://code.claude.com/docs/en/permission-modes] [Source: https://code.claude.com/docs/en/permissions]

Print the mode. Print the lists. Then print the redirect. If you only print the mode, you will file “bypassPermissions ate always-ask.” BypassPermissions is documented to keep the critical-path prompt. The named bug was that prompt dropping when a `~` or wildcard redirect sat on the same line. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.287]

![Flow: Lists, then circuit breaker, then redirect on the same line](/img/print-the-redirect-before-you-file-always-ask-off-3.png)

Permission modes in one table, from the official page, so a junior does not invent a fifth mode.

| Mode | Ordinary shell | Critical-path `rm` |
| --- | --- | --- |
| default / acceptEdits | Asks on most shell | Asks |
| auto | Classifier, fewer prompts | Still a circuit breaker, with a timed prompt in a terminal |
| dontAsk | Denies what would have prompted | Denies |
| bypassPermissions | Skips most prompts | Still asks on root and home removals |

[Source: https://code.claude.com/docs/en/permission-modes]

If the screenshot is auto mode and the command has no redirect, do not file this post’s ticket. If the screenshot is bypassPermissions and the command has a tilde redirect, file this field first, then the mode.

## Neighbor tickets that are not this field

Print these so a junior does not collapse every `rm` headline into this redirect.

1. **Command-substitution `rm`.** A recursive `rm` whose target is only command-substitution output, such as `rm -rf "$(pwd)"`, is a different public fix. After that fix the command asks even with a Bash allow rule unless `CLAUDE_CODE_DISABLE_SUBSTITUTION_RM_PROMPT=1`. That is substitution, not a tilde redirect. Do not clone it. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.281] [Source: https://code.claude.com/docs/en/changelog]
2. **`bash -c` / `sh -c`.** A later public note names a dangerous `rm` inside `bash -c` or `sh -c` running without a prompt in bypassPermissions mode or under a shell allow rule. Different wrapper. Different ticket. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.288] [Source: https://code.claude.com/docs/en/changelog]
3. **A NUL byte in a permission rule.** Matcher bytes, not redirects. Already a post. [Source: https://zemna.net/blog/a-nul-byte-in-a-permission-rule-is-not-a-wildcard/]
4. **Sandbox auto-allow on `python3 -c`.** Equals matcher, not always-ask on `rm`. Already a post. [Source: https://zemna.net/blog/sandbox-auto-allow-is-not-a-retry-tax-on-equals/]
5. **A laravel/ai lockfile line.** Fetch client, not a shell redirect. Already a post. [Source: https://zemna.net/blog/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client/]
6. **Copilot approve.** A ready-to-approve line is not a merge vote. Already a post. [Source: https://zemna.net/blog/leave-copilot-approve-off/]

If the logged command is `rm -rf "$(pwd)"` with no redirect, you are on neighbor 1. If the logged command is `bash -c 'rm -rf /'` with no `> ~`, you are on neighbor 2. If the logged command is `rm -rf / > ~/agent.log`, you are on this field.

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a coding agent cleaning `storage/logs` or a Vite build folder, a junior who added `> ~/agent.log` so the transcript survives the next compact, and a missing always-ask prompt that then looks like “the agent is allowed to delete.” I treat `CLAUDE_CODE_ALWAYS_ASK_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “did this `rm` line also write a home path.” A coding agent does not get to close an always-ask-off ticket because the prompt was absent. I already wrote the sibling rule for a NUL byte that is not a wildcard allow, and for sandbox auto-allow that is not a retry tax on equals. This is the sibling for a redirect that dropped always-ask.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File “always-ask is off” without printing the full command, the redirect target, the dry compare, and one human name.
2. Put `2.1.287` or `2.1.288` in the title or the first line. The pin is evidence after the decision.
3. Mix this field with substitution-rm, `bash -c` wrapping, a NUL permission rule, sandbox equals, or a laravel/ai lockfile line. Those are other posts.
4. Write a live `rm` against `/` or the home directory to “demo” the old matcher. The public release already states the old matcher. You do not need a live wipe.
5. Treat npm `latest` as this deploy. Print the installed Claude Code line the same way you print a lockfile.
6. Treat `stable` 2.1.285 as “this field is absent.” Dist-tags are not the logged command.
7. Set `CLAUDE_CODE_DISABLE_SUBSTITUTION_RM_PROMPT=1` or `CLAUDE_CODE_DISABLE_DANGEROUS_RM_TIMEOUT=1` as a demo. Those flags belong to neighbor tickets. This page does not turn them on. [Source: https://code.claude.com/docs/en/changelog]
8. Recommend buying a plan, a seat, or a scanner because a prompt was missing.
9. Clone the auto-start post, the green-deploy post, the /readyz post, the runner-deadline post, the 2,500+ inventory post, the sandbox-equals post, or the lockfile post as a synonym. Those URLs already shipped. GSC this week has no striking-distance query that asks for another copy.
10. File “every rm” or “every redirect” as this field. The public notes name a dangerous `rm` on `/` or the home directory plus a `~` or wildcard redirect.

Allowed:

1. Print the logged command as one string.
2. Classify it with `probe_redirect_always_ask.py`. Do not execute it.
3. Answer dry-compare always-ask yes/no in one sentence owned by a human.
4. Name one human as `CLAUDE_CODE_ALWAYS_ASK_OWNER`.
5. Print the installed Claude Code version after the decision, in a details block, not in the title.
6. Schedule the client update as change control when the logged command matches this field and the installed line predates the public fix.
7. Keep substitution-rm and `bash -c` wrapping as separate tickets, not as fake all-clears.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about a missing always-ask prompt is not permission to skip the four lines.

![Print four lines: Command, Redirect, Dry compare, Owner](/img/print-the-redirect-before-you-file-always-ask-off-4.png)

## What you should do Monday morning

1. Open the repo that actually ships. Export `CLAUDE_CODE_ALWAYS_ASK_OWNER` to a human name. Collect the last coding-agent shell logs that contain `rm`. Run `probe_redirect_always_ask.py` against each logged string. Write `this_field=True` or `False` on the ticket next to that name.
2. For every `this_field=True` row, answer dry-compare in one sentence: the same `rm` without the redirect still prompts, or it does not. If you cannot answer, the ticket is “owner missing,” not “always-ask off.”
3. If the logged command matches this field and the installed Claude Code line predates the public fix, file “redirect dropped always-ask,” not “always-ask is off.” If there is no redirect, file no-redirect. If the wrapper is `bash -c`, file the wrapper ticket. If the target is only `"$(pwd)"`, file substitution.
4. If someone pastes a single `npm i -g @anthropic-ai/claude-code` as the close of substitution-rm, redirect-rm, and `bash -c` wrapping, split the ticket. Print three logged strings. Close each field on its own evidence. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.281] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.288]
5. Print `claude --version` from the machine that ran the agent, not from a laptop that did not. If the laptop line is not the CI line, do not treat the laptop as production.
6. Confirm coding-agent instructions on this desk name the same owner and forbid “always-ask is off” without the four lines. Forbid any live `rm` against `/` or the home directory as a demo.

The question is not whether the changelog demos well in a gist. The question is whether the named owner can still tell a tilde redirect from a setting that is actually off after handoff.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.287" label="GitHub — Claude Code v2.1.287 release notes" >}}

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code docs — changelog" >}}

{{< source href="https://code.claude.com/docs/en/permissions" label="Claude Code docs — configure permissions" >}}
