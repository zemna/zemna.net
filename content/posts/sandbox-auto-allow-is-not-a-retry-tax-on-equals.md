---
title: "Sandbox Auto-Allow Is Not a Retry Tax on Equals in Inline Scripts"
date: 2026-10-01T07:00:00+07:00
draft: false
slug: "sandbox-auto-allow-is-not-a-retry-tax-on-equals"
description: "An every-run prompt on python3 -c is not proof that sandbox auto-allow is off. Print the equals matcher, the auto-allow setting, and the named Claude Code owner before you file an auto-allow-broken ticket."
topics: ["ai-agents"]
tags: ["claude-code", "sandbox", "auto-allow", "inline-scripts", "coding-agents", "change-control"]
cover: /covers/sandbox-auto-allow-is-not-a-retry-tax-on-equals.png
seo:
  primaryQuery: "Claude Code sandbox auto-allow equals inline script"
  secondaryQueries:
    - "python3 -c sandbox approval every run"
    - "inline script equals is not a missing allow"
    - "named owner for Claude Code sandbox auto-allow"
---

The junior pastes a terminal screenshot. Sandbox is on. Auto-allow is on. The coding agent ran `python3 -c "x=1"`. Claude Code asked for approval. They file the ticket: “auto-allow is off.”

I stop the run there. Sandbox auto-allow is not a retry tax on equals in inline scripts. The public Claude Code notes that named this field are blunt: sandbox auto-allow asked for approval on every run of many inline scripts (`python3 -c`, `node -e`) just because they contain `=`. That is a matcher on the equals sign, not a missing allow. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.285] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a NUL byte in a permission rule as a wildcard allow in [A NUL Byte in a Permission Rule Is Not a Wildcard Allow](/blog/a-nul-byte-in-a-permission-rule-is-not-a-wildcard/). I already refused to treat a present `AGENTS.md` as the project instructions while `CLAUDE.md` exists in [A Present AGENTS.md Is Not the Project Instructions While CLAUDE.md Exists](/blog/agents-md-is-not-the-project-instructions/). I already refused to treat Copilot’s ready-to-approve line as a required merge vote in [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/). This post is the same desk rule for sandbox auto-allow. Print the command. Print whether it contains `=`. Name who owns the auto-allow answers.

The question is not whether the prompt looks like a broken allow. The question is whether the named owner can tell an equals matcher from a setting that is actually off.

<!--more-->

![Three columns: every-run prompt, equals in inline script, named owner](/img/sandbox-auto-allow-is-not-a-retry-tax-on-equals-1.png)

## The ticket that looks like auto-allow is off

Juniors treat an every-run prompt the way they treat a broken firewall rule. The panel says auto-allow. The command still stops. They page the desk: “sandbox auto-allow is off, every `python3 -c` needs a click.”

Two jobs collide on that line.

1. **Keep sandboxed Bash from asking.** Official sandbox docs: auto-allow runs sandboxed commands without prompting. Regular permissions keep the regular prompts even when commands are sandboxed. [Source: https://code.claude.com/docs/en/sandboxing]
2. **Keep the matcher honest.** A prompt on `python3 -c` that contains `=` is not proof the first job failed. The public fix names the old matcher: many inline scripts asked on every run just because they contain `=`. [Source: https://code.claude.com/docs/en/changelog]

If you only screenshot “it asked again,” you will file auto-allow-broken. You will not file the equals sign.

{{< note type="warning" title="Do not file auto-allow-broken on an every-run prompt" >}}
If a coding agent or a junior says sandbox auto-allow is off, print the exact command, whether it is `python3 -c` or `node -e`, whether the payload contains `=`, the resolved `sandbox.autoAllowBashIfSandboxed` value, and one human name on the auto-allow answers before you page the desk. A prompt is not a setting.
{{< /note >}}

I do not invent a fake overnight policy flip. I use the public contract. The matcher field is the ticket, not a version pin in the title.

## What sandbox auto-allow actually is

Official sandbox docs: the Bash sandbox lets Claude run most shell commands without stopping to ask permission. You define which files and network domains commands can touch. The operating system enforces that boundary for every Bash, PowerShell, or Monitor command and its child processes. [Source: https://code.claude.com/docs/en/sandboxing]

The product gives two sandbox **modes**. In both, the sandbox enforces the same filesystem and network restrictions. The difference is only whether sandboxed commands are auto-approved or still require explicit permission. [Source: https://code.claude.com/docs/en/sandboxing]

**Auto-allow mode:** when a command can be sandboxed, Claude Code runs it inside the sandbox and approves it automatically, without asking. Commands that cannot be sandboxed, such as those needing network access to non-allowed hosts, fall back to the regular permission flow. [Source: https://code.claude.com/docs/en/sandboxing]

Even in auto-allow mode, the following still apply:

- Explicit deny rules are always respected.
- `rm` or `rmdir` that targets a critical path still goes through the regular permission flow.
- Content-scoped ask rules such as `Bash(git push *)` still force a prompt even for sandboxed commands.
- A bare `Bash` ask rule, or `Bash(*)`, is skipped for commands that run sandboxed. It still applies to commands that fall back to the regular flow. In plan mode the skip does not apply. [Source: https://code.claude.com/docs/en/sandboxing]

That list is the surviving prompt set. It is not “any `python3 -c` with an assignment.”

The setting that names the auto-approve switch is `sandbox.autoAllowBashIfSandboxed`. Official settings docs: auto-approve bash commands when sandboxed. Default: `true`. [Source: https://code.claude.com/docs/en/settings]

Copy the docs example as a probe of the lists, not as a bypass recipe.

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build"]
    },
    "network": {
      "allowedDomains": ["github.com", "registry.npmjs.org"]
    }
  }
}
```

[Source: https://code.claude.com/docs/en/settings]

That JSON is the allow switch and the box. It is not a matcher for the `=` character inside `python3 -c "x=1"`. If auto-allow is `true` and the command is sandboxed, a prompt on that assignment is the equals field, not proof the JSON is `false`.

Auto-allow is also **not** auto mode. Official sandbox docs: auto-allow approves Bash because the sandbox boundary contains the command. Auto mode uses a classifier to review actions. Mixing those two tickets produces “the classifier is broken” when the field was an inline `=`. [Source: https://code.claude.com/docs/en/sandboxing] [Source: https://code.claude.com/docs/en/permission-modes]

## The equals matcher is not a missing allow

The public changelog under 29 September 2026 names the field in one sentence: fixed sandbox auto-allow asking for approval on every run of many inline scripts (`python3 -c`, `node -e`) just because they contain `=`. The GitHub release that carries the same sentence is the 29 September 2026 tag. [Source: https://code.claude.com/docs/en/changelog] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.285]

Read that twice.

- **Before:** `python3 -c "x=1"` or `node -e "const x=1"` inside a sandboxed run asked every time. A junior then files “auto-allow is off.”
- **After:** that assignment is not itself a reason to ask. A prompt that remains is a surviving rule from the auto-allow list, an unsandboxed fallback, a deny, or a content-scoped ask. It is not the equals sign.

The junior screenshot is usually one of these four, and only the first is this ticket:

| What they paste | What the field is | Ticket |
| --- | --- | --- |
| `python3 -c "x=1"` asked every run, auto-allow on | `=` inside the inline script | equals matcher, not auto-allow-off |
| `python3 -c "print(1)"` asked, no `=` | surviving prompt, unsandboxed fallback, or deny | print the mode and the fallback title |
| Prompt titled “Bash command (unsandboxed)” | command left the box | not this matcher |
| `Bash(git push *)` still asked | content-scoped ask | documented, keep it |

[Source: https://code.claude.com/docs/en/sandboxing]

Do not “prove” the old matcher by stuffing `=` into a live command to force a prompt. The public notes already state the old ask and the fix. You do not need a live poison script.

![Equals in an inline script is a matcher, not auto-allow off](/img/sandbox-auto-allow-is-not-a-retry-tax-on-equals-2.png)

## Print three lines before you file skip

A desk that lives with coding agents already has a permission owner. Sandbox auto-allow needs the same name. I treat `SANDBOX_AUTO_ALLOW_OWNER` the way I treat a migration owner on a Laravel plus Vue SaaS: one human, one settings file, one verdict.

The probe below does not call the model. It does not toggle auto-allow. It does not disable the sandbox. It prints whether the command under review is an inline script with `=`.

```python
#!/usr/bin/env python3
"""Classify a pasted Bash line. Do not run the line. Do not skip a prompt."""
from __future__ import annotations

import json
import os
import shlex
import sys
from pathlib import Path


INLINE = {"python3", "python", "node"}
INLINE_FLAG = {"python3": "-c", "python": "-c", "node": "-e"}


def classify(command: str) -> dict:
    parts = shlex.split(command, posix=True)
    if not parts:
        return {"verdict": "EMPTY", "equals": False, "inline": False}
    bin_name = Path(parts[0]).name
    inline = bin_name in INLINE and len(parts) >= 3 and parts[1] == INLINE_FLAG.get(bin_name)
    payload = parts[2] if inline else ""
    equals = "=" in payload
    if inline and equals:
        verdict = "EQUALS_IN_INLINE_SCRIPT"
    elif inline:
        verdict = "INLINE_WITHOUT_EQUALS"
    else:
        verdict = "NOT_INLINE_SCRIPT"
    return {
        "verdict": verdict,
        "bin": bin_name,
        "inline": inline,
        "equals": equals,
        "owner": os.environ.get("SANDBOX_AUTO_ALLOW_OWNER", "UNSET"),
    }


def main() -> int:
    raw = sys.stdin.read().strip()
    row = classify(raw)
    print(json.dumps(row, indent=2))
    if row["verdict"] == "EQUALS_IN_INLINE_SCRIPT":
        print("TICKET=equals-matcher-not-auto-allow-off", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Save it as `scripts/probe_sandbox_equals.py`. Feed it the pasted command, not a live shell.

```bash
export SANDBOX_AUTO_ALLOW_OWNER="shinjae"
printf '%s\n' 'python3 -c "x=1"' | python3 scripts/probe_sandbox_equals.py
printf '%s\n' 'python3 -c "print(1)"' | python3 scripts/probe_sandbox_equals.py
python3 -c "import json,pathlib; p=pathlib.Path('.claude/settings.json'); print('settings', 'readable' if p.is_file() else 'missing')"
```

`TICKET=equals-matcher-not-auto-allow-off` means you do not have a broken allow. You have an inline script whose payload contains `=`. Then open `/sandbox`. Copy the mode. Copy whether the prompt title said unsandboxed. Put those four lines on the ticket: owner, command, equals verdict, mode.

A second probe is the settings file the session actually loaded. Print `sandbox.enabled` and `sandbox.autoAllowBashIfSandboxed`. Default auto-allow is `true` when the key is absent. [Source: https://code.claude.com/docs/en/settings]

```python
#!/usr/bin/env python3
"""Print sandbox auto-allow from a settings file. Do not rewrite policy."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: Path) -> dict:
    if not path.is_file():
        return {"path": str(path), "exists": False}
    data = json.loads(path.read_text(encoding="utf-8"))
    sandbox = data.get("sandbox") or {}
    auto = sandbox.get("autoAllowBashIfSandboxed", True)
    return {
        "path": str(path),
        "exists": True,
        "enabled": sandbox.get("enabled"),
        "autoAllowBashIfSandboxed": auto,
        "defaulted_auto_allow": "autoAllowBashIfSandboxed" not in sandbox,
    }


def main() -> int:
    paths = sys.argv[1:] or [".claude/settings.json", ".claude/settings.local.json"]
    rows = [load(Path(p)) for p in paths]
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If `autoAllowBashIfSandboxed` is `false`, the every-run prompt is the mode you chose. File that as a policy ticket, not as a matcher bug. If it is `true` or defaulted, and the command is `python3 -c` with `=`, file the equals matcher.

Print `claude --version` **after** the decision, in a details block, not in the title. A pin is evidence. It is not the hook.

{{< details summary="Where the public notes sit (not the title)" >}}
The equals-in-inline-script sentence lives in the 29 September 2026 changelog entry and in the matching GitHub release notes. Later npm `latest` moving forward does not erase that sentence. Compare the laptop pin after you name the owner and the command. Do not put a version in the heading. [Source: https://code.claude.com/docs/en/changelog] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.285]
{{< /details >}}

![Probe checklist: owner, command, equals verdict, sandbox mode](/img/sandbox-auto-allow-is-not-a-retry-tax-on-equals-3.png)

## What still prompts when auto-allow is on

Official docs already list the survivors. Print them on the ticket so a junior does not collapse every prompt into “allow is off.”

1. **Deny still wins.** Evaluation order is deny, then ask, then allow. A deny that matches the call still blocks. Auto-allow does not punch through deny. [Source: https://code.claude.com/docs/en/permissions] [Source: https://code.claude.com/docs/en/sandboxing]
2. **Critical-path `rm` still asks.** That is a separate field. Do not mix it with `python3 -c`. [Source: https://code.claude.com/docs/en/sandboxing]
3. **Content-scoped ask still asks.** `Bash(git push *)` still prompts for a sandboxed `git push`. Keep that. [Source: https://code.claude.com/docs/en/sandboxing]
4. **Unsandboxed fallback still asks.** Claude Code titles those prompts “Bash command (unsandboxed)” instead of “Bash command.” If the screenshot shows that title, the command left the box. The equals matcher is the wrong ticket. [Source: https://code.claude.com/docs/en/sandboxing]
5. **New network hosts still ask** the first time, unless auto mode names the hosts on the command for the classifier. That is network policy, not `=`. [Source: https://code.claude.com/docs/en/sandboxing]
6. **Plan mode still asks** for a bare `Bash` ask rule even on sandboxed commands. [Source: https://code.claude.com/docs/en/sandboxing]

If the prompt is one of those six, write that name on the ticket. Do not write “auto-allow is off.”

I already wrote the sibling for a matching glob that is not a whole-line sandbox exemption. `sandbox.excludedCommands` is that post. This post is the auto-allow matcher. Do not merge them. [Source: https://zemna.net/blog/one-matching-glob-is-not-a-whole-line-exemption/]

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a committed `.claude/settings.json` with sandbox enabled, a gitignored `.claude/settings.local.json` that set auto-allow on one laptop, and a coding agent that pastes “auto-allow is off” because `python3 -c` with an assignment stopped the run. I treat `SANDBOX_AUTO_ALLOW_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “did this payload contain equals.” A coding agent does not get to set `autoAllowBashIfSandboxed` to a new value, or to add `--dangerously-skip-permissions`, because an inline assignment prompted. I already wrote the sibling rule for a NUL byte that is not a wildcard allow, and for Copilot’s ready-to-approve line that is not a merge vote. This is the sibling for an equals sign that is not a missing allow.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File an “auto-allow is off” ticket without printing the settings path, `autoAllowBashIfSandboxed`, the exact command, the equals verdict, and one human name on the auto-allow answers.
2. Put a Claude Code version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with a compound-glob sandbox ticket, a NUL-in-rule ticket, an `AGENTS.md` brief ticket, or a Copilot-approve ticket. Those are other posts.
4. Write a live `python3 -c` with `=` to “demo” the old every-run prompt. The public notes already state the old ask. You do not need a live poison script. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.285]
5. Flip `sandbox.autoAllowBashIfSandboxed` to “fix” a prompt. If the JSON is already `true`, the flip is theater.
6. Recommend buying a plan, a seat, or a gateway because one inline script prompted.
7. Treat `/sandbox` showing auto-allow as proof the matcher used it on this command.
8. Treat an unsandboxed prompt title as this matcher. Official docs: unsandboxed fallback uses a different prompt title. [Source: https://code.claude.com/docs/en/sandboxing]
9. Confuse sandbox auto-allow with auto mode. Auto mode is a classifier. Auto-allow is the sandbox boundary. [Source: https://code.claude.com/docs/en/permission-modes]
10. Paste `--dangerously-skip-permissions`, `IS_SANDBOX=1`, or any skip-permissions flag because an inline script asked. That is a bypass recipe. This post does not write one.
11. Widen `sandbox.excludedCommands` to unsandbox `python3 *` because of an equals prompt. That is a policy change, not a matcher repair. [Source: https://code.claude.com/docs/en/sandboxing]
12. Clone the auto-start post, the runner-deadline post, or the 2,500+ inventory post as a synonym. Those URLs already shipped. GSC this week has no striking-distance query that asks for another copy.

Allowed:

1. Print `sandbox.enabled` and `sandbox.autoAllowBashIfSandboxed` from the file the session actually loaded.
2. Classify a pasted command with `probe_sandbox_equals.py`. Do not execute the pasted command as a demo.
3. Keep documented survivors: deny, critical-path `rm`, content-scoped ask, unsandboxed fallback, first-time network hosts, plan-mode ask. [Source: https://code.claude.com/docs/en/sandboxing]
4. Name one human as `SANDBOX_AUTO_ALLOW_OWNER`.
5. Print `claude --version` after the decision, in a details block, not in the title.
6. Leave auto-allow `true` when the named owner wants sandboxed Bash to run without a click, and file equals-matcher when the payload contains `=`.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about a matcher is not permission to skip the prompt without the four lines.

![Auto-allow is not off: print equals then owner](/img/sandbox-auto-allow-is-not-a-retry-tax-on-equals-4.png)

## What you should do Monday morning

1. Open the repo that actually ships. Export `SANDBOX_AUTO_ALLOW_OWNER` to a human name. Run `probe_sandbox_equals.py` against the pasted command from the ticket. Run the settings probe against `.claude/settings.json` and, if it exists, `.claude/settings.local.json`. Write the verdict on the ticket next to that name.
2. Open `/sandbox`. Copy the mode. Copy the prompt title. If the title says unsandboxed, file fallback, not equals. If the mode is regular permissions, file the mode you chose, not a matcher bug.
3. If a `python3 -c` or `node -e` line asked and the payload contains `=`, file “equals in inline script,” not “auto-allow is off.” If the payload has no `=`, walk the surviving-prompt list before you touch JSON.
4. If someone pastes a skip-permissions flag or an `excludedCommands` widen as the fix, reject the review until the named owner can show the four lines: owner, command, equals verdict, auto-allow value.
5. Print `claude --version`. If the laptop is behind the 29 September 2026 notes that named the matcher change, do not treat the local pin as those fields. Compare, then decide an upgrade as change control, not as a social post. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.285] [Source: https://code.claude.com/docs/en/changelog]
6. Confirm coding-agent instructions on this desk name the same owner and forbid “auto-allow is off” without the four lines.

The question is not whether auto-allow demos well in a gist. The question is whether the named owner can still tell an equals matcher from a setting that is actually off after handoff.

## Further reading

{{< source href="https://code.claude.com/docs/en/sandboxing" label="Claude Code Docs — configure the sandboxed Bash tool" >}}

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.285" label="GitHub — Claude Code release notes that name the equals matcher" >}}

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code Docs — changelog" >}}
