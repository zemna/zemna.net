---
title: "A Present AGENTS.md Is Not the Project Instructions While CLAUDE.md Exists"
date: 2026-09-20T07:00:00+07:00
draft: false
slug: "agents-md-is-not-the-project-instructions"
description: "A repo-root AGENTS.md is not Claude Code’s project instructions while CLAUDE.md or CLAUDE.local.md exists. Print the load line, open /config, and name who owns the instruction file."
topics: ["ai-agents"]
tags: ["claude-code", "agents-md", "claude-md", "project-instructions", "coding-agents", "change-control"]
cover: /covers/agents-md-is-not-the-project-instructions.png
seo:
  primaryQuery: "Claude Code AGENTS.md not loaded when CLAUDE.md exists"
  secondaryQueries:
    - "Claude Code Project instructions /config AGENTS.md"
    - "CLAUDE.local.md blocks AGENTS.md fallback"
    - "Claude Code AGENTS.md Bedrock Vertex Foundry"
---

The junior opens the repo root. `AGENTS.md` is there. Codex already reads it. Copilot already reads it. They added Claude Code last week. The agent still ships a Laravel migration without the test command they wrote in that file. Standup calls it a model miss.

I stop the run there. A present `AGENTS.md` is not the project instructions while `CLAUDE.md` exists. Default load is the Claude files only when `CLAUDE.md` or `CLAUDE.local.md` sits in the working directory or above it. The shared file stays on disk. The session never treats it as the brief.

Official memory docs put that in one table. An `AGENTS.md` with no Claude file in the tree loads. An `AGENTS.md` next to a `CLAUDE.md` or `CLAUDE.local.md` does not. Change the mix under **Project instructions** in `/config`. [Source: https://code.claude.com/docs/en/memory]

I already refused to treat `ubuntu-latest` as a runner image I already tested in [Ubuntu-latest Is Not a Runner Image You Already Tested](/blog/ubuntu-latest-is-not-a-tested-runner-image/). I already refused to treat a missing Wrangler `previews` block as production bindings in [A Missing Previews Block Is Not a License to Reuse Production Bindings](/blog/missing-previews-block-is-not-production-bindings/). This post is the same desk rule for an instruction file. Print the load line. Open `/config`. Name who owns the file Claude actually read.

The question is not whether `AGENTS.md` exists on disk. The question is whether the named owner can prove which file this session loaded.

<!--more-->

![Two columns: AGENTS.md on disk is not the brief while CLAUDE.md is present](/img/agents-md-is-not-the-project-instructions-1.png)

## The file that looks loaded

Juniors treat a repo-root markdown file the way they treat a README. If the name matches the tool, the tool must have read it. `AGENTS.md` is the shared name. The file is committed. The PR description says “agent instructions updated.” The session still ignores the test command.

That miss has two jobs, and they collide on a desk that already has a Claude file.

1. **Shared brief.** Other coding agents read `AGENTS.md`. The team wants one file.
2. **Claude brief.** Claude Code still counts `CLAUDE.md`, `.claude/CLAUDE.md`, and `CLAUDE.local.md` first. Those files win the default fallback.

Official docs say Claude can read `AGENTS.md` as project instructions so a repository already set up for other agents works without adding a `CLAUDE.md`, an import, or a setting. That sentence is the empty-tree case. It is not the case where a Claude file already exists. [Source: https://code.claude.com/docs/en/memory]

If you only `ls` the root and see `AGENTS.md`, you will file the model. You will not file the load order.

{{< note type="warning" title="Do not file the model on a present AGENTS.md" >}}
If the agent ignored a rule you wrote only in `AGENTS.md`, print the files that count, open `/config`, and copy the load line before you page the model. A present file is not a loaded brief.
{{< /note >}}

I do not invent a fake overnight outage. I use the public contract. The GitHub release that added the fallback says: in a project with no `CLAUDE.md`, Claude Code reads `AGENTS.md` instead; change it under “Project instructions” in `/config`. The same bullet says the fallback is not yet on Bedrock, Vertex, or Foundry. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/changelog]

## What Claude actually reads by default

I do not invent a merge. Official memory docs give three rows.

| Your repository has | Claude reads |
| --- | --- |
| `AGENTS.md`, and no `CLAUDE.md` or `CLAUDE.local.md` in the working directory or above it | Your `AGENTS.md` |
| `AGENTS.md` and a `CLAUDE.md` or `CLAUDE.local.md` in the working directory or above it | Your `CLAUDE.md` files only |
| A `CLAUDE.md` that already imports `AGENTS.md` | Your `CLAUDE.md`, with `AGENTS.md` included through the import |

[Source: https://code.claude.com/docs/en/memory]

That middle row is the ticket on this desk. Most Laravel plus Vue repos already have a `CLAUDE.md` from last year’s `/init`. The junior then adds `AGENTS.md` so Codex and Copilot share one file. Default Claude Code still reads the Claude files only.

Files that **count**, so Claude reads them instead of `AGENTS.md`:

- `CLAUDE.md`
- `.claude/CLAUDE.md`
- `CLAUDE.local.md`

in the working directory or any directory above it.

Files that **do not count**, and keep loading alongside `AGENTS.md` when the fallback fires:

- `~/.claude/CLAUDE.md`
- the organization’s managed `CLAUDE.md`
- `.claude/rules/` files

[Source: https://code.claude.com/docs/en/memory]

When none of the counting files exist, an interactive session prints a line such as `no CLAUDE.md found; AGENTS.md loaded: /home/you/repo/AGENTS.md`. That line is the artifact. A missing line is not “it must have loaded because the file is in git.”

Subdirectory `AGENTS.md` files load later, when Claude opens a file there with the Read tool and that subdirectory has none of the three Claude files of its own. `AGENTS.local.md`, `AGENTS.override.md`, and anything under `.agents/` are not read. [Source: https://code.claude.com/docs/en/memory]

{{< details summary="Pins are evidence, not the hook" >}}
Direct `AGENTS.md` load needs Claude Code at or after the 18 September 2026 GitHub release that named the fallback. This morning’s npm registry, 20 September 2026: `@anthropic-ai/claude-code` `latest` and `next` are 2.1.278 (published 19 September 2026). `stable` is still 2.1.267 (published 9 September 2026). Do not treat `stable` as the field. Do not put those numbers in the title. Changelog notes for 2.1.278 are an auto-mode classifier change. That is a different ticket. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/changelog] [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
{{< /details >}}

## The local file that steals the fallback

The trap I see on review is not the committed `CLAUDE.md`. It is `CLAUDE.local.md`.

Official docs say that file is for private per-project preferences. It loads alongside `CLAUDE.md`. Add it to `.gitignore`. Because it **counts**, adding one to keep your own uncommitted instructions in a project that relies on `AGENTS.md` **stops** Claude from reading `AGENTS.md` for you. [Source: https://code.claude.com/docs/en/memory]

The junior did the “right” thing. They gitignored a local file so personal sandbox URLs never hit the remote. The shared `AGENTS.md` still sits at the root. Codex still reads it. Claude Code on that laptop does not.

To keep `CLAUDE.local.md` and still have Claude read `AGENTS.md`, set **Project instructions** to `claude-md-and-agents-md`. Do not delete the local file in panic and call that a model fix. [Source: https://code.claude.com/docs/en/memory]

A user-level `~/.claude/CLAUDE.md` does not steal the fallback. An org managed file does not steal the fallback. A `.claude/rules/` file does not steal the fallback. Those three still load. They do not count as “a Claude file exists, skip `AGENTS.md`.” Mix those facts on a ticket and you will “fix” the wrong layer.

![CLAUDE.local.md counts and leaves AGENTS.md unread](/img/agents-md-is-not-the-project-instructions-2.png)

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous mix is ordinary: a committed `CLAUDE.md` from `/init`, a new `AGENTS.md` so other agents share the test command, and a gitignored `CLAUDE.local.md` with one person’s sandbox URL. I treat the instruction-file owner the same way I treat a migration owner. The person who owns [/ai-agent-operations/](/ai-agent-operations/) on this desk also owns “which file this session loaded.” A coding agent does not get to skip `php artisan test --parallel` because the rule lived only in `AGENTS.md` while `CLAUDE.md` still said “use your judgment.” I already wrote the sibling rule for a client that still sends `initialize`. This is the sibling for a present `AGENTS.md` that is not the brief.
{{< /field-note >}}

## `/config` is the screenshot

I do not guess the mix from the repo tree. Official docs say: type `/config` in a Claude Code session, then set **Project instructions**.

| Value | What Claude reads |
| --- | --- |
| `claude-md-or-agents-md` | Claude files, or `AGENTS.md` when no `CLAUDE.md` or `CLAUDE.local.md` is in the working directory or above it. This is the default. |
| `claude-md-and-agents-md` | Both. Each directory’s Claude files first, then its `AGENTS.md`. An `AGENTS.md` already imported or symlinked is not read twice. |
| `claude-md` | Claude files only. |
| `managed-only` | Only the organization’s managed `CLAUDE.md` and auto memory at launch. Project, local, and user Claude files, `.claude/rules/`, and every `AGENTS.md` are left out of that launch set. |

[Source: https://code.claude.com/docs/en/memory]

You can also set the value in a settings file under the built-in `agents-md` plugin ID in `pluginConfigs`. Official docs put that in `~/.claude/settings.json`, a `--settings` file, or managed settings. Claude Code **ignores** it in project and local settings files. The change applies from the next message you send and in every new session. [Source: https://code.claude.com/docs/en/memory]

```json
{
  "pluginConfigs": {
    "agents-md@builtin": {
      "options": {
        "instructionFiles": "claude-md-and-agents-md"
      }
    }
  }
}
```

That JSON is the user or managed settings shape from the public docs. It is not a project-root file you commit and expect every clone to honor. If the junior drops it in `.claude/settings.json` inside the app, the setting does not apply. File that as a settings-layer miss, not a plugin bug.

`/memory` lists `CLAUDE.md` and `CLAUDE.local.md`. An `AGENTS.md` loaded through the setting is **not** listed there. Confirm with the `AGENTS.md loaded` line under the default value, or ask Claude what its project instructions say. `InstructionsLoaded` hooks fire for Claude files. They do not fire for an `AGENTS.md` loaded through the setting. They do fire for an `AGENTS.md` that a `CLAUDE.md` imports or symlinks to. [Source: https://code.claude.com/docs/en/memory]

![Project instructions live in /config, not in a guess](/img/agents-md-is-not-the-project-instructions-3.png)

## Sessions that never load AGENTS.md

Some sessions never show **Project instructions** in `/config`. Official docs list them. Claude reads Claude files only:

1. The installed Claude Code is older than the release that added the fallback.
2. The session does not fetch feature flags from Anthropic — Amazon Bedrock, another third-party provider, or telemetry disabled. The env-vars page has the full list.
3. It is the first session after you install or upgrade to a version with `AGENTS.md` support. Claude reads `AGENTS.md` from the **next** session on.
4. You or your organization set `disableAllHooks` or `allowManagedHooksOnly`, or you disabled the built-in `agents-md` plugin in `/plugin`.

[Source: https://code.claude.com/docs/en/memory]

The GitHub release bullet matches the provider row: not yet on Bedrock, Vertex, or Foundry. I do not turn that into a production claim on this desk. I treat it as a session class. If the host is on Bedrock, import `@AGENTS.md` from a `CLAUDE.md`. Do not wait for the fallback to appear in `/config`. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277]

A first session after upgrade is a time bomb for a junior who “just updated.” They open Claude Code, paste the ticket, and the fallback is still off until the next session. Print `claude --version`. Close. Open again. Then look for the load line.

When Claude is not reading `AGENTS.md` directly, keep one shared file with an import:

```markdown
@AGENTS.md

## Claude Code

Use plan mode for changes under `app/Billing`.
```

Official docs use that import shape. Claude reads the imported file first, then the rest. A symlink also works on Unix. Edit and Write refuse to write through a symlink and send Claude to the target instead. On Windows, use the import. Creating a symlink there needs Administrator privileges or Developer Mode, and Git checks a committed symlink out as a plain text file unless `core.symlinks` is enabled, which leaves that clone with a one-line `CLAUDE.md`. [Source: https://code.claude.com/docs/en/memory]

Leave an existing `@AGENTS.md` import in place if some sessions cannot load `AGENTS.md` directly. Keeping the import never makes Claude read `AGENTS.md` twice. A `CLAUDE.md` that only *tells Claude in words* to read `AGENTS.md` is not an import. Claude sees the file only if it decides to open it. Replace the sentence with `@AGENTS.md` or delete the Claude file so the fallback can fire. A `SessionStart` hook that prints `AGENTS.md` becomes a second copy once Claude reads the file directly. Remove the hook. [Source: https://code.claude.com/docs/en/memory]

I already refused to treat a client that still sends `initialize` as a broken Laravel MCP server in [A Client That Still Sends Initialize Is Not a Broken Laravel MCP Server](/blog/initialize-is-not-a-broken-laravel-mcp-server/). Same habit here. An old session class is not a dead product.

## A probe you run before you file the agent

I do not invent a dashboard. I read the files Git will ship and the files Git ignores.

```python
#!/usr/bin/env python3
"""Print instruction files Claude Code counts from this working directory."""

from __future__ import annotations

import os
from pathlib import Path

CWD = Path.cwd().resolve()
COUNTING = ("CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md")
AGENTS = ("AGENTS.md", ".claude/AGENTS.md")
NOT_READ = ("AGENTS.local.md", "AGENTS.override.md")


def walk_up(start: Path):
    current = start
    while True:
        yield current
        if current.parent == current:
            break
        current = current.parent


def existing(root: Path, relative: str) -> Path | None:
    path = root / relative
    return path if path.is_file() else None


def main() -> int:
    owner = os.environ.get("INSTRUCTION_FILE_OWNER", "UNSET")
    print(f"CWD={CWD}")
    print(f"OWNER={owner}")
    counting: list[str] = []
    agents: list[str] = []
    skipped: list[str] = []
    for root in walk_up(CWD):
        for name in COUNTING:
            hit = existing(root, name)
            if hit:
                counting.append(str(hit))
        for name in AGENTS:
            hit = existing(root, name)
            if hit:
                agents.append(str(hit))
        for name in NOT_READ:
            hit = existing(root, name)
            if hit:
                skipped.append(str(hit))
        agents_dir = root / ".agents"
        if agents_dir.is_dir():
            skipped.append(str(agents_dir) + "/ (not read)")
    print("--- counting files (block AGENTS.md fallback) ---")
    print("\n".join(counting) if counting else "(none)")
    print("--- AGENTS.md files on disk ---")
    print("\n".join(agents) if agents else "(none)")
    print("--- not read as AGENTS.md ---")
    print("\n".join(skipped) if skipped else "(none)")
    if counting and agents:
        print("VERDICT=CLAUDE_FILES_WIN_DEFAULT")
    elif agents and not counting:
        print("VERDICT=AGENTS_MD_FALLBACK_ELIGIBLE")
    elif counting and not agents:
        print("VERDICT=CLAUDE_ONLY")
    else:
        print("VERDICT=NO_PROJECT_INSTRUCTION_FILE")
    if owner == "UNSET":
        print("FAIL=name INSTRUCTION_FILE_OWNER before you file the agent")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it in the app root the coding agent uses, not in a docs folder on your laptop.

```bash
export INSTRUCTION_FILE_OWNER="shinjae"
python3 scripts/probe_instruction_files.py
claude --version
```

The script does not talk to Anthropic. It reads the tree. `VERDICT=CLAUDE_FILES_WIN_DEFAULT` means the shared `AGENTS.md` is not the default brief. Then open `/config`. Copy **Project instructions**. Copy the load line from the session. Put those four lines on the ticket: owner, verdict, setting, load line.

`find` on those names is evidence of presence. It is not evidence of load.

![Probe the tree: named owner required, CLAUDE_FILES_WIN_DEFAULT](/img/agents-md-is-not-the-project-instructions-4.png)

## What you must not do

Forbidden:

1. File a “Claude ignored AGENTS.md” ticket without printing the counting files, `/config` **Project instructions**, the load line, and one human name on the instruction file.
2. Put a Claude Code version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with an older bundled CLI that is not a logout, a Copilot picker name, or an `ubuntu-latest` runner label. Those are other tickets.
4. Treat `stable` on npm as the field. This morning `stable` is still behind the fallback release. [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
5. Drop `pluginConfigs` into project or local settings and expect Claude Code to honor it. Official docs say it ignores that key there. [Source: https://code.claude.com/docs/en/memory]
6. Add `CLAUDE.local.md` for personal URLs and then claim `AGENTS.md` is the brief. The local file counts. It steals the fallback.
7. Trust `/memory` as proof that `AGENTS.md` loaded. Official docs say that file is not listed there when it loaded through the setting.
8. Recommend buying a plan, a model, or a seat because a test command lived only in `AGENTS.md`.
9. Treat the first session after an upgrade as a loaded fallback. Official docs say the next session is the one that reads `AGENTS.md`.

Allowed:

1. Print every counting Claude file from the working directory up.
2. Print every `AGENTS.md` on disk, including `.claude/AGENTS.md`.
3. Open `/config` and screenshot **Project instructions**.
4. Copy the `AGENTS.md loaded` line when the fallback actually fired.
5. Keep `@AGENTS.md` in `CLAUDE.md` when some hosts cannot load the fallback.
6. Name one human as `INSTRUCTION_FILE_OWNER`.

GSC this week still has no striking-distance query on the ubuntu-latest post, the previews-block post, or the initialize post. I am not refreshing those URLs. This is a new field, not a synonym of Saturday’s runner label or Friday’s bindings warning.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the agent is touching that stack. A first-week map is at [/start-here/](/start-here/).

A changelog bullet about `AGENTS.md` is not permission to skip `/config`.

## What you should do Monday morning

1. Open the repo that actually ships. Export `INSTRUCTION_FILE_OWNER` to a human name. Run `probe_instruction_files.py` in the app root the coding agent uses. Write the verdict on the ticket next to that name.
2. Open Claude Code in that same directory. Type `/config`. Copy **Project instructions**. If the panel has no such row, you are in a session class that never loads `AGENTS.md` directly. Import `@AGENTS.md` from `CLAUDE.md` on that host.
3. If both files exist and the setting is still the default, pick one owner decision: delete the unused Claude file so the fallback can fire, import `@AGENTS.md`, or set `claude-md-and-agents-md` in user or managed settings. Do not leave two files and one hope.
4. If `CLAUDE.local.md` exists, treat it as a counting file. Either keep it and set `claude-md-and-agents-md`, or move personal URLs out of a file that steals the brief.
5. Print `claude --version`. If you upgraded this morning, close the first session and open a second before you claim the fallback loaded.
6. Confirm coding-agent instructions on this desk name the same owner and forbid “the agent ignored AGENTS.md” without the load line. A prompt that says “follow AGENTS.md” while `CLAUDE.md` still wins is a different ticket.

The question is not whether `AGENTS.md` demos in an empty tree. The question is whether the load order survives maintenance, handoff, and a junior who already committed a Claude file.

## Further reading

{{< source href="https://code.claude.com/docs/en/memory" label="Claude Code Docs — How Claude remembers your project (AGENTS.md load table)" >}}

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.277" label="GitHub — Claude Code release that added AGENTS.md fallback" >}}

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code Docs — Changelog (18–19 September 2026 notes)" >}}
