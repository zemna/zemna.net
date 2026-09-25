---
title: "A NUL Byte in a Permission Rule Is Not a Wildcard Allow"
date: 2026-09-25T07:00:00+07:00
draft: false
slug: "a-nul-byte-in-a-permission-rule-is-not-a-wildcard"
description: "A permission rule that contains a NUL byte is not a wildcard allow. Print the rule bytes, the match-nothing result, and the named permission-rule owner before you file an allow-all ticket."
topics: ["ai-agents"]
tags: ["claude-code", "permissions", "settings-json", "coding-agents", "change-control"]
cover: /covers/a-nul-byte-in-a-permission-rule-is-not-a-wildcard.png
seo:
  primaryQuery: "Claude Code permission rule NUL byte not a wildcard"
  secondaryQueries:
    - "permission rule containing NUL matches nothing"
    - "Claude Code settings.json deny miss vs wildcard allow"
    - "named owner for coding agent permission rules"
---

The junior pastes a `/permissions` screenshot. A deny rule is in the list. The coding agent still ran the tool. They file an allow-all ticket: “the rule allowed everything.”

I stop the run there. A NUL byte in a permission rule is not a wildcard allow. The public Claude Code release that named this field is blunt: a permission rule containing a NUL byte was expanded into a wildcard match; such a rule now matches nothing. That is a matcher bug, not proof that deny lost. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.281] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a timed-out job as a killed worker in [A Timed-Out Job Is Not a Killed Worker](/blog/a-timed-out-job-is-not-a-killed-worker/). I already refused to treat one matching glob as a sandbox exemption for the rest of the line in [One Matching Glob Is Not a Sandbox Exemption for the Rest of the Line](/blog/one-matching-glob-is-not-a-whole-line-exemption/). I already refused to treat a present `AGENTS.md` as the project instructions while `CLAUDE.md` exists in [A Present AGENTS.md Is Not the Project Instructions While CLAUDE.md Exists](/blog/agents-md-is-not-the-project-instructions/). This post is the same desk rule for permission bytes. Print the bytes. Print the match. Name who owns the permission list.

The question is not whether a deny line looks present in JSON. The question is whether the named owner can tell a wildcard from a rule that matches nothing.

<!--more-->

![Three columns: rule bytes, match nothing, named owner](/img/a-nul-byte-in-a-permission-rule-is-not-a-wildcard-1.png)

## The ticket that looks like allow-all

Juniors treat a deny miss the way they treat a firewall hole. The line is in `settings.json`. The tool still ran. They page security: “deny is broken, everything is allowed.”

Two jobs collide on that line.

1. **Stop a tool the team named.** Official docs: deny rules prevent Claude Code from using the specified tool. Rules are evaluated deny, then ask, then allow. The first match in that order wins. [Source: https://code.claude.com/docs/en/permissions]
2. **Keep the matcher honest.** A rule that does not match is not a deny. A rule that used to expand into a wildcard is also not the deny you thought you wrote.

If you only screenshot “the deny is listed,” you will file allow-all. You will not file the bytes.

{{< note type="warning" title="Do not file allow-all on a deny miss" >}}
If a coding agent or a junior says the permission list allowed everything, print the rule bytes, whether the rule now matches nothing, and one human name on the permission list before you page security. A listed rule is not a matching rule.
{{< /note >}}

I do not invent a fake overnight breach. I use the public contract. The matcher field is the ticket, not a version pin in the title.

## What a permission rule actually is

Official permissions docs: rules follow `Tool` or `Tool(specifier)`. A rule that is only the tool name matches every use of that tool. Adding `Bash` to the allow list lets Claude Code use Bash without a prompt. Adding `Bash` to the deny list removes Bash from Claude’s context. A scoped rule such as `Bash(rm *)` leaves the tool available and blocks matching calls. [Source: https://code.claude.com/docs/en/permissions]

Wildcards are a separate field. A `*` in a Bash rule matches any text, including spaces. A rule with no `*` matches one exact command. Official docs: `Bash(*)` is treated as equivalent to `Bash`. [Source: https://code.claude.com/docs/en/permissions] [Source: https://github.com/anthropics/claude-code/issues/21140]

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

That JSON is readable UTF-8. Every character you see is the character the matcher sees. A NUL byte is not a character you see in a paste. It is byte `0x00`. It does not print. It does not survive every editor. It does survive a bad copy from a binary dump, a Windows device name mix-up, or an agent that wrote a path with an embedded null.

The public fix names the old matcher: a permission rule containing a NUL byte was expanded into a wildcard match. After the fix, such a rule matches nothing. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.281] [Source: https://code.claude.com/docs/en/changelog]

Read that twice.

- **Before:** NUL in the rule → treated like `*`. A deny that looked narrow could match like a wildcard. A junior then files “deny allowed everything.”
- **After:** NUL in the rule → matches nothing. The same deny is now a no-op. A junior then files “deny is ignored.” Both tickets skip the bytes.

Neither ticket is allow-all until you print the bytes.

{{< details summary="Pins are evidence, not the hook" >}}
The matcher change shipped in Claude Code v2.1.281 on 23 September 2026 (`published_at` 2026-09-23T19:19:15Z, prerelease false). The GitHub release and the official changelog use the same sentence: a permission rule containing a NUL byte being expanded into a wildcard match; such a rule now matches nothing. The same release also says Read, Write, Edit, and NotebookEdit fail a file path that contains a null byte with a clear error instead of ending the whole turn. Do not put those numbers in the title. This post is the matcher field, not a patch table. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.281] [Source: https://code.claude.com/docs/en/changelog]
{{< /details >}}

![Listed deny, hidden byte, then match nothing](/img/a-nul-byte-in-a-permission-rule-is-not-a-wildcard-2.png)

## Three columns on the ticket

I keep one table on the ticket.

| What you saw | What it is | What it is not |
| --- | --- | --- |
| Deny line in `/permissions` | A listed rule | Proof the matcher used that rule |
| Tool still ran | No matching deny, or the rule matches nothing | Allow-all forever |
| NUL byte in the rule string | Old: expanded to wildcard. Now: matches nothing | A `*` you typed on purpose |
| Visible `*` in `Bash(npm run *)` | Documented wildcard | A hidden `0x00` |
| Empty match after the fix | The rule is a no-op | The permission system is off |

The junior screenshot is the first row. They want the third column. Print the second column first.

Name the owner. I use `PERMISSION_RULE_OWNER` the same way I use a migration owner. The person who owns `.claude/settings.json` on this desk also owns “did this rule contain a NUL, did it match nothing, or did a real wildcard fire.” A coding agent does not get to file allow-all because a listed deny missed.

Official evaluation order stays on the same ticket. Deny, then ask, then allow. A broad deny such as `Bash(aws *)` blocks every matching call, including a narrower allow such as `Bash(aws s3 ls)`. An allow rule cannot carve an exception out of a deny rule. [Source: https://code.claude.com/docs/en/permissions]

That order only runs on rules the matcher actually matches. A NUL rule that matches nothing never enters deny. It never enters allow. It is dead text in the file.

Do not heading-clone the compound-glob post. That post is `sandbox.excludedCommands` on a compound Bash line. This post is permission-rule bytes. Do not heading-clone the `AGENTS.md` post. That post is which brief the agent reads. This post is which bytes the matcher reads.

## Probe the bytes, do not write a NUL rule

I keep a probe in the repo the coding agent uses, not in a gist on a laptop. It does not insert a NUL. It does not craft a wildcard. It classifies existing settings files.

```python
#!/usr/bin/env python3
"""Classify permission-rule bytes. Not a NUL-rule recipe."""

from __future__ import annotations

import json
import os
from pathlib import Path

NUL = b"\x00"


def load_bytes(path: Path) -> bytes:
    return path.read_bytes() if path.is_file() else b""


def rule_strings(raw: bytes) -> list[str]:
    if not raw or NUL in raw:
        return []
    data = json.loads(raw.decode("utf-8"))
    perms = data.get("permissions") or {}
    out: list[str] = []
    for key in ("allow", "deny", "ask"):
        for item in perms.get(key) or []:
            if isinstance(item, str):
                out.append(item)
    return out


def main() -> int:
    owner = os.environ.get("PERMISSION_RULE_OWNER", "").strip()
    path = Path(os.environ.get("CLAUDE_SETTINGS", ".claude/settings.json"))
    raw = load_bytes(path)

    print(f"PERMISSION_RULE_OWNER={owner or 'MISSING'}")
    print(f"SETTINGS={path}")
    print(f"BYTES={len(raw)}")
    print(f"NUL_COUNT={raw.count(NUL)}")

    if not owner:
        print("VERDICT=NO_OWNER")
        return 2
    if not path.is_file():
        print("VERDICT=NO_SETTINGS_FILE")
        return 2
    if NUL in raw:
        print("VERDICT=NUL_IN_FILE_MATCHER_MUST_BE_REBUILT")
        return 1

    rules = rule_strings(raw)
    print(f"RULE_COUNT={len(rules)}")
    wildcards = [r for r in rules if "*" in r]
    print(f"VISIBLE_WILDCARD_COUNT={len(wildcards)}")
    print("VERDICT=NO_NUL_PRINT_VISIBLE_RULES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it in the app that actually ships.

```bash
export PERMISSION_RULE_OWNER="shinjae"
export CLAUDE_SETTINGS=".claude/settings.json"
python3 scripts/probe_permission_nul.py
python3 -c "import json,pathlib; p=pathlib.Path('.claude/settings.json'); print('readable' if p.is_file() else 'missing')"
```

The script does not call the model. It does not toggle auto mode. `VERDICT=NUL_IN_FILE_MATCHER_MUST_BE_REBUILT` means you do not have an allow-all policy. You have a file whose matcher used to treat `0x00` as `*`, and now treats it as match-nothing. Then open `/permissions`. Copy the listed deny. Put those four lines on the ticket: owner, path, NUL count, verdict.

A second probe is the official lists themselves. Print `allow`, `deny`, and `ask` as UTF-8. If a rule looks like `Bash(git push *)`, that `*` is a documented wildcard. If the file contains `0x00`, that is not a `*` you typed. Do not “fix” it by pasting a broader `Bash(*)`. Official docs already say `Bash(*)` matches every Bash call. That is a policy change, not a byte repair. [Source: https://code.claude.com/docs/en/permissions]

The same release also fails Read, Write, Edit, and NotebookEdit when the **file path** contains a null byte, with a clear error, instead of ending the whole turn. That is a sibling field: path bytes, not permission-rule bytes. Keep it on a second ticket. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.281] [Source: https://code.claude.com/docs/en/changelog]

![Probe checklist: owner, path, NUL count, verdict](/img/a-nul-byte-in-a-permission-rule-is-not-a-wildcard-3.png)

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a committed `.claude/settings.json` with `Read(./.env)` on deny, a gitignored `.claude/settings.local.json` for one laptop, and a coding agent that pastes “deny allowed everything” because a tool still ran. I treat `PERMISSION_RULE_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “did this rule contain a NUL.” A coding agent does not get to widen `Bash(*)` because a listed deny missed. I already wrote the sibling rule for a matching glob that is not a whole-line exemption, and for a timed-out job that is not a killed worker. This is the sibling for a NUL byte that is not a wildcard allow.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File an “allow-all” ticket without printing the settings path, the NUL count, the listed deny, and one human name on the permission list.
2. Put a Claude Code version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with a compound-glob sandbox ticket, an `AGENTS.md` brief ticket, or a timed-out job ticket. Those are other posts.
4. Write a NUL into a permission rule to “demo” the old wildcard. The public notes already state the old expansion and the new match-nothing. You do not need a live poison rule. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.281]
5. Replace a broken rule with `Bash(*)` or a bare `Bash` deny because the bytes were dirty. Bare `Bash` on deny removes the tool from context. That is a different policy. [Source: https://code.claude.com/docs/en/permissions]
6. Recommend buying a plan, a seat, or a gateway because one rule missed.
7. Treat `/permissions` listing the rule as proof the matcher used it.
8. Treat “matches nothing” as “permission system off.” Official docs: Claude Code enforces rules, not the model. A dead rule is dead text. The rest of the list still runs. [Source: https://code.claude.com/docs/en/permissions]
9. Confuse a Windows file named `nul` with a NUL byte inside a JSON string. Those are different bugs. This post is the permission-rule matcher.
10. Paste `CLAUDE_CODE_DISABLE_SUBSTITUTION_RM_PROMPT=1` or any rm bypass because this release also named a substitution-only `rm` prompt. That is a different field. Do not write an rm recipe here.

Allowed:

1. Print `allow`, `deny`, and `ask` from the file the session actually loaded.
2. Count `0x00` in that file with a probe. Do not insert `0x00`.
3. Keep documented wildcards such as `Bash(npm run *)` when the named owner wants that family. [Source: https://code.claude.com/docs/en/permissions]
4. Name one human as `PERMISSION_RULE_OWNER`.
5. Print `claude --version` after the decision, in a details block, not in the title.
6. Rebuild a dirty settings file as UTF-8 JSON with only the visible rules the owner still wants.

GSC this week still has no striking-distance query on the timed-out-job post, the compound-glob post, or the `AGENTS.md` post. I am not refreshing those URLs. This is a new field, not a synonym of Thursday’s queue clock or Wednesday’s glob.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about a matcher is not permission to skip the bytes.

## What you should do Monday morning

1. Open the repo that actually ships. Export `PERMISSION_RULE_OWNER` to a human name. Run `probe_permission_nul.py` against `.claude/settings.json` and, if it exists, `.claude/settings.local.json`. Write the verdict on the ticket next to that name.
2. Open `/permissions`. Copy every deny line. For each line, write whether the matcher has a visible `*` or a hidden `0x00`. If NUL count is greater than zero, rebuild the file as UTF-8. Do not add a broader wildcard to “make deny work.”
3. If a tool ran that a listed deny should have stopped, file “this rule did not match.” Decide whether the rule was dead (match-nothing), the call used a different tool name, or evaluation order never saw that rule. Official order is deny, then ask, then allow. [Source: https://code.claude.com/docs/en/permissions]
4. If someone pastes a settings snippet with an unprintable character, reject the review until the named owner can show `NUL_COUNT=0` and a JSON parse of the same file.
5. Print `claude --version`. If the laptop is behind the 23 September 2026 release that named the matcher change, do not treat the local pin as those fields. Compare, then decide an upgrade as change control, not as a social post. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.281] [Source: https://code.claude.com/docs/en/changelog]
6. Confirm coding-agent instructions on this desk name the same owner and forbid “the rule allowed everything” without the four lines: owner, settings path, NUL count, listed deny.

The question is not whether a deny line demos well in a gist. The question is whether the named owner can still tell a wildcard from a rule that matches nothing after handoff.

## Further reading

{{< source href="https://code.claude.com/docs/en/permissions" label="Claude Code Docs — configure permissions" >}}

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.281" label="GitHub — Claude Code v2.1.281 release notes" >}}

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code Docs — changelog" >}}
