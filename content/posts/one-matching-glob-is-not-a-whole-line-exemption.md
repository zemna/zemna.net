---
title: "One Matching Glob Is Not a Sandbox Exemption for the Rest of the Line"
date: 2026-09-23T07:00:00+07:00
draft: false
slug: "one-matching-glob-is-not-a-whole-line-exemption"
description: "A docker glob that matches one command is not a sandbox exemption for npm ci && docker build. Print the glob, split every part, and name who owns sandbox.excludedCommands before you file a hole."
topics: ["developer-tools"]
tags: ["claude-code", "sandbox", "excluded-commands", "coding-agents", "change-control"]
cover: /covers/one-matching-glob-is-not-a-whole-line-exemption.png
seo:
  primaryQuery: "Claude Code sandbox excludedCommands compound command"
  secondaryQueries:
    - "sandbox.excludedCommands every part must match"
    - "docker glob does not unsandbox npm ci"
    - "Claude Code compound Bash sandbox exemption"
---

The junior pastes a settings.json screenshot. `sandbox.excludedCommands` has `docker *`. The coding agent ran `npm ci && docker build .`. The first token looks like a match. They file a sandbox hole: “the whole line ran outside the box.”

I stop the run there. One matching glob is not a sandbox exemption for the rest of the line. Official settings docs are blunt: your entries take a Bash call out of the sandbox only when they cover every command in it. A `docker *` entry alone does not take `npm ci && docker build .` out of the sandbox. [Source: https://code.claude.com/docs/en/settings-reference]

I already refused to treat a failed local DNS lookup as a missing host in [Handing the Hostname to the Forward Proxy Is Not a Missing Host](/blog/hostname-handed-to-proxy-is-not-a-missing-host/). I already refused to treat a present `AGENTS.md` as the project instructions while `CLAUDE.md` exists in [A Present AGENTS.md Is Not the Project Instructions While CLAUDE.md Exists](/blog/agents-md-is-not-the-project-instructions/). I already refused to treat `ubuntu-latest` as a runner image I already tested in [Ubuntu-latest Is Not a Runner Image You Already Tested](/blog/ubuntu-latest-is-not-a-tested-runner-image/). This post is the same desk rule for compound Bash. Print the glob. Split the parts. Name who owns `sandbox.excludedCommands`.

The question is not whether `docker *` demos on a single command. The question is whether the named owner can prove every part of the line matched.

<!--more-->

![Two columns: one matching docker glob is not a whole-line sandbox exemption](/img/one-matching-glob-is-not-a-whole-line-exemption-1.png)

## The ticket that looks like a hole

Juniors treat `excludedCommands` the way they treat a shell alias. If the first token matches, the whole line is “allowed out.” That habit is correct for a personal `alias`. It is wrong for Claude Code’s sandbox.

Two jobs collide on that line.

1. **Run the tool that cannot live in the box.** Docker, a host builder, a binary that needs a device the sandbox does not give.
2. **Keep the rest of the line in the box.** Package install, file writes, network, anything that was not named.

The GitHub release that named this field says the product used to exempt an entire compound Bash command from the sandbox when only one part matched. Every part must now match. The official changelog repeats that sentence under 18 September 2026. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/changelog]

If you only screenshot `docker *` and the first token, you will file a hole. You will not file the line.

{{< note type="warning" title="Do not file a sandbox hole on a one-part match" >}}
If the agent ran a compound command and you think the glob unsandboxed the rest, print `sandbox.excludedCommands`, split the line on `&&`, `;`, `||`, and `|`, and write a human name on the list before you page security. One matching part is not a whole-line exemption.
{{< /note >}}

I do not invent a fake overnight breach. I use the public contract. The settings page is the ticket, not a version pin in the title.

## What excludedCommands actually grants

Official docs: `sandbox.excludedCommands` names commands Claude Code runs outside the sandbox, such as tools that do not work under it. Each entry uses the same syntax as the content of a `Bash(...)` permission rule: an exact command, a prefix such as `docker *`, or a wildcard pattern. [Source: https://code.claude.com/docs/en/settings-reference]

Read the next sentence twice. Your entries take a Bash call out of the sandbox **only when they cover every command in it**, and some call shapes stay sandboxed even then.

That is the field. Exclusion is a convenience, not a security boundary. Official docs say prefer `filesystem.allowWrite` when a tool only needs to write somewhere specific. Excluded commands still go through the regular permission flow. Claude Code merges entries across every settings scope the session loads, and there is no managed-only lock for this list, so keep a managed list narrow. [Source: https://code.claude.com/docs/en/settings-reference]

The example the docs publish is this shape. Copy it as a probe, not as a bypass recipe.

```json
{
  "sandbox": {
    "excludedCommands": ["docker *"]
  }
}
```

[Source: https://code.claude.com/docs/en/settings-reference]

`docker *` is not “anything that mentions docker.” It is one pattern. `npm ci` is a different command. A chain is more than one command.

{{< details summary="Pins are evidence, not the hook" >}}
The compound-glob fix needs Claude Code at or after the 18 September 2026 GitHub release that said every part of a compound Bash command must match `sandbox.excludedCommands`. This morning’s npm registry, 23 September 2026: `@anthropic-ai/claude-code` `latest` and `next` are 2.1.280 (published 22 September 2026). `stable` is still 2.1.267 (published 9 September 2026). Do not treat `stable` as the field. Do not put those numbers in the title. Changelog notes after 18 September cover other tickets. This post is the compound line. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/changelog] [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
{{< /details >}}

## Every part of the line has to match

I keep one table on the ticket.

| Line the agent ran | `excludedCommands` | Field |
| --- | --- | --- |
| `docker build .` | `docker *` | Pattern covers the only command. Exclusion can fire. Permission flow still runs. |
| `npm ci && docker build .` | `docker *` | `npm ci` is not covered. The call stays sandboxed. |
| `cd build && docker compose up` | `docker *` plus a `cd` entry | Official docs: still sandboxed. A `cd` anywhere in the call keeps the whole call in the box. |

[Source: https://code.claude.com/docs/en/settings-reference]

The middle row is the junior screenshot. They listed docker. They saw `&&`. They assumed the shell inherited the exemption. The product no longer does that. The GitHub body and the changelog both say the old glob exempted the entire compound command when only one part matched. That is the behavior you must not file as current. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/changelog]

The last row is the trap after you “fix” the middle row. You add `cd` to the list because the agent `cd`s into `build/`. Official docs still keep that call sandboxed. Adding a `cd` entry does not change it. [Source: https://code.claude.com/docs/en/settings-reference]

![Three rows: every part must match or the compound command stays sandboxed](/img/one-matching-glob-is-not-a-whole-line-exemption-2.png)

If you need write access for a build artifact, official docs point at `filesystem.allowWrite`, not at a wider glob. [Source: https://code.claude.com/docs/en/settings-reference]

## Shapes that stay sandboxed anyway

Even when every named part looks like a match, official docs keep a Bash call sandboxed for these shapes, among others:

- A command starting with `sudo`, `eval`, or `xargs`
- A `cd`, `pushd`, or `popd`, wherever it appears in the call
- A command substitution, a subshell, or a control-flow block such as `if` or `for`
- A redirection, such as `docker build . > build.log`, other than one that only duplicates a file descriptor, as `2>&1` does
- A command name that comes from a variable

[Source: https://code.claude.com/docs/en/settings-reference]

That list is why I refuse “we listed docker, so compose is out.” `docker build . > build.log` stays in. `cd build && docker compose up` stays in. A variable that expands to `docker` stays in.

Sandboxing docs also say content-scoped ask rules such as `Bash(git push *)` still force a prompt even for sandboxed commands. A bare `Bash` ask rule, or `Bash(*)`, is skipped for commands that run sandboxed, and still applies when the command falls back to the regular permission flow. Exclusion does not delete that flow. [Source: https://code.claude.com/docs/en/sandboxing]

Strict sandbox mode is a different switch. `sandbox.allowUnsandboxedCommands: false` makes Claude Code ignore `dangerouslyDisableSandbox`. Every command Claude runs must run sandboxed unless you listed it in `excludedCommands`. The `/sandbox` Overrides tab shows that as **Strict sandbox mode**. [Source: https://code.claude.com/docs/en/settings-reference] [Source: https://code.claude.com/docs/en/sandboxing]

Do not mix those tickets. Strict mode is “no escape hatch.” Compound glob is “one match is not the whole line.” File one.

{{< note type="note" title="Permission is not isolation" >}}
`permissions.allow` answers “may this run at all.” `sandbox.excludedCommands` answers “does this run outside the box.” Official settings text: excluded commands still go through the regular permission flow. Listing docker in one array and not the other is a different ticket than a compound line.
{{< /note >}}

## Probe the glob, not the feeling

I do not reconstruct a compound line in a live agent session to “prove” a hole. That is how you write an escape recipe. I print the list, split the line, require a human owner, and fail closed when the owner is unset.

```python {linenos=inline,hl_lines=[12,"36-41"]}
#!/usr/bin/env python3
"""Probe sandbox.excludedCommands coverage. Does not run the agent. Does not spawn a shell."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

OWNER_ENV = "SANDBOX_EXCLUSION_OWNER"
SPLIT = re.compile(r"\s*(?:&&|\|\||;|\|)\s*")


def load_patterns(settings_path: Path) -> list[str]:
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    sandbox = data.get("sandbox") or {}
    patterns = sandbox.get("excludedCommands") or []
    if not isinstance(patterns, list):
        raise SystemExit("FAIL=sandbox.excludedCommands is not a list")
    return [str(p) for p in patterns]


def split_parts(command: str) -> list[str]:
    return [part.strip() for part in SPLIT.split(command) if part.strip()]


def glob_to_re(pattern: str) -> re.Pattern[str]:
    return re.compile("^" + re.escape(pattern).replace(r"\*", ".*") + "$")


def covered(part: str, patterns: list[str]) -> bool:
    return any(glob_to_re(p).match(part) for p in patterns)


def main() -> int:
    owner = os.environ.get(OWNER_ENV, "UNSET")
    settings = Path(os.environ.get("CLAUDE_SETTINGS", ".claude/settings.json"))
    command = os.environ.get("AGENT_BASH_LINE", "")
    print(f"OWNER={owner}")
    print(f"SETTINGS={settings}")
    print(f"LINE={command}")
    if owner == "UNSET":
        print("FAIL=name SANDBOX_EXCLUSION_OWNER before you file the agent")
        return 1
    if not settings.is_file():
        print("FAIL=settings file missing")
        return 1
    if not command:
        print("FAIL=set AGENT_BASH_LINE to the exact command from the transcript")
        return 1
    patterns = load_patterns(settings)
    print("PATTERNS=" + json.dumps(patterns))
    parts = split_parts(command)
    print("PARTS=" + json.dumps(parts))
    hits = [covered(part, patterns) for part in parts]
    for part, hit in zip(parts, hits):
        print(f"PART_COVERED={hit} {part}")
    if len(parts) > 1 and not all(hits):
        print("VERDICT=COMPOUND_NOT_FULLY_COVERED")
        return 2
    if all(hits) and parts:
        print("VERDICT=EVERY_PART_MATCHED_PATTERN")
        print("NOTE=docs still keep sudo/eval/xargs/cd/redirection/subshell shapes sandboxed")
        return 0
    print("VERDICT=NO_PARTS")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it in the app root the coding agent uses, not in a docs folder on your laptop.

```bash
export SANDBOX_EXCLUSION_OWNER="shinjae"
export CLAUDE_SETTINGS=".claude/settings.json"
export AGENT_BASH_LINE='npm ci && docker build .'
python3 scripts/probe_excluded_commands.py
claude --version
```

The script does not talk to Anthropic. It does not start Docker. `VERDICT=COMPOUND_NOT_FULLY_COVERED` means you do not have a whole-line exemption. Then open `/sandbox`. Copy **Excluded commands**. Copy the transcript line. Put those four lines on the ticket: owner, patterns, parts, verdict.

A second probe is the session itself. Type `/sandbox`. Read the Overrides tab. If Strict sandbox mode is on, `dangerouslyDisableSandbox` is not an extra hatch. That is a different screenshot from the glob list. [Source: https://code.claude.com/docs/en/sandboxing]

![Probe checklist: named owner, printed patterns, split parts, verdict](/img/one-matching-glob-is-not-a-whole-line-exemption-3.png)

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous mix is ordinary: a coding agent with `sandbox.excludedCommands: ["docker *"]` because Sail or a host daemon cannot bind inside the box, and a default agent habit of `npm ci && docker build .` or `php artisan test && docker compose up`. The first token looks like docker. The rest is npm or artisan. I treat `SANDBOX_EXCLUSION_OWNER` the same way I treat a migration owner. The person who owns [/developer-tools/](/developer-tools/) on this desk also owns “did every part of this line match.” A coding agent does not get to skip `php artisan test --parallel` because docker was on the list. I already wrote the sibling rule for a present `AGENTS.md` that is not the brief. This is the sibling for a matching glob that is not a whole-line exemption.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File a “sandbox hole” ticket without printing `excludedCommands`, the split parts, `/sandbox` Excluded commands, and one human name on the list.
2. Put a Claude Code version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with a hostname-to-proxy DNS ticket, an `AGENTS.md` load ticket, or an `ubuntu-latest` runner label. Those are other posts.
4. Treat `stable` on npm as the field. This morning `stable` is still behind the compound-glob fix. [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
5. Reconstruct `cmd && other` in a live session to demonstrate an old whole-line exemption. That is an escape write-up. Print and split. Do not chain.
6. Add `cd` to `excludedCommands` and claim `cd build && docker compose up` is now out. Official docs keep that call sandboxed. [Source: https://code.claude.com/docs/en/settings-reference]
7. Widen the glob until `*` covers the rest of the line, then call that a security policy. Exclusion is a convenience. Prefer `filesystem.allowWrite` for a specific path. [Source: https://code.claude.com/docs/en/settings-reference]
8. Recommend buying a plan, a model, or a seat because a docker glob did not unsandbox `npm ci`.
9. Treat a permission allow rule as isolation. Allow answers “may it run.” Exclusion answers “does it leave the box.”

Allowed:

1. Print `sandbox.excludedCommands` from every settings scope the session loads.
2. Split the transcript line on `&&`, `;`, `||`, and `|`.
3. Open `/sandbox` and screenshot Excluded commands plus Strict sandbox mode.
4. Keep `filesystem.allowWrite` for the artifact directory instead of a wider glob.
5. Name one human as `SANDBOX_EXCLUSION_OWNER`.
6. Print `claude --version` after the decision, in a details block, not in the title.

GSC this week still has no striking-distance query on the hostname-to-proxy post, the AGENTS.md post, or the ubuntu-latest post. I am not refreshing those URLs. This is a new field, not a synonym of Monday’s proxy env or Sunday’s instruction file.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the agent is touching that stack. A first-week map is at [/start-here/](/start-here/).

A changelog bullet about a glob is not permission to skip the split.

![Forbidden vs allowed: file the line, not the feeling](/img/one-matching-glob-is-not-a-whole-line-exemption-4.png)

## What you should do Monday morning

1. Open the repo that actually ships. Export `SANDBOX_EXCLUSION_OWNER` to a human name. Run `probe_excluded_commands.py` against the exact `AGENT_BASH_LINE` from last week’s transcript. Write the verdict on the ticket next to that name.
2. Open Claude Code in that same directory. Type `/sandbox`. Copy **Excluded commands**. Copy whether Strict sandbox mode is on. If the panel has no such row, you are not looking at the session that ran the line.
3. If the list contains `docker *` and the transcript contains `npm ci && docker build .`, do not file a hole. File “npm ci was never covered.” Decide whether npm belongs in the box with `filesystem.allowWrite`, or whether the agent must run docker as its own command.
4. If the transcript contains `cd` anywhere, treat the whole call as sandboxed until a human proves otherwise. Do not add a `cd` entry and stop.
5. Print `claude --version`. If `stable` is what the laptop installed, do not treat that pin as the compound-glob field. Compare it to the GitHub release that said every part must match, then decide an upgrade as change control, not as a social post.
6. Confirm coding-agent instructions on this desk name the same owner and forbid “the glob unsandboxed the line” without the split. A prompt that says “docker is excluded” while the agent chains npm is a different ticket.

The question is not whether `docker *` demos on an empty line. The question is whether the exemption survives maintenance, handoff, and a junior who already chained two commands.

## Further reading

{{< source href="https://code.claude.com/docs/en/settings-reference" label="Claude Code Docs — settings reference (sandbox.excludedCommands)" >}}

{{< source href="https://code.claude.com/docs/en/sandboxing" label="Claude Code Docs — sandboxing" >}}

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.277" label="GitHub — Claude Code release that required every compound part to match" >}}
