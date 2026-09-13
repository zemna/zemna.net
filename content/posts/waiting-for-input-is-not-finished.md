---
title: "Waiting for Your Input Is Not a Finished Background Agent"
date: 2026-09-13T07:00:00+07:00
draft: false
slug: "waiting-for-input-is-not-finished"
description: "A remote or headless row that says waiting for your input is not done. Open the agent list, split Needs input from Working, and name who owns the CLI pin."
topics: ["ai-agents"]
tags: ["claude-code", "background-agents", "headless", "remote-control", "coding-agents", "change-control"]
cover: /covers/waiting-for-input-is-not-finished.png
seo:
  primaryQuery: "Claude Code waiting for your input while background agents running"
  secondaryQueries:
    - "headless Claude Code background agent still running"
    - "claude agents Needs input vs Working"
    - "who owns remote headless Claude Code CLI pin"
---

Standup hears “the agent is waiting.” Someone pasted a remote or headless screenshot. The line says waiting for your input. The junior treats that as a stop. They close the laptop. They tell the chat the overnight job is done.

I stop the run there. A wait line is not a finished background agent. On a remote or headless host, that sentence used to print while other agents were still running. The work was live. The status lied.

Official notes from 11 September 2026 name the split. Remote and headless sessions reported “waiting for your input” while background agents were still running. Status now reports those tasks as running. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.269] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a Node API miss as a new module registry in [Node.js APIs On Is Not the New Module Registry](/blog/nodejs-apis-on-is-not-the-new-module-registry/). I already refused to treat an unreadable managed allow-list as a company lockdown in [Treat Unreadable Managed Settings as Empty](/blog/treat-unreadable-managed-settings-as-empty/). This post is the same desk rule for a wait line. Read the agent list. Split Needs input from Working. Name who owns the remote-headless host and the CLI pin.

The question is not whether chat printed a polite pause. The question is whether the named owner can still see the work that is running.

<!--more-->

![Wait line versus still-running rows, with a named owner](/img/waiting-for-input-is-not-finished-1.png)

## The wait line that looks like a stop

Juniors read “waiting for your input” the way they read a CI badge. The words sound finished. Nobody is typing. The prompt is empty. They assume the machine is idle.

That sentence has two jobs, and they used to collide on remote and headless hosts.

1. **Needs input.** A person has to answer. Permission, a question, a choice. The session is blocked on you.
2. **Working.** A background agent, a subagent, or a workflow is still running. The parent row can look quiet. The child is not.

Official agent view puts those rows in different buckets: Needs input, Working, and Completed. You open it with `claude agents`. You do not guess from a pasted screenshot. [Source: https://code.claude.com/docs/en/agent-view]

If you only read the parent wait line, you will kill a live child, or you will walk away from a job that is still spending tokens.

{{< note type="warning" title="Do not close the host on a wait line" >}}
If a remote or headless session says waiting for your input, open the agent list before you call the job done. Copy the Working rows. Do not treat the parent pause as a green exit.
{{< /note >}}

I do not invent a fake overnight outage. I use the public contract. The 11 September release names the old lie in one bullet: remote and headless sessions reported waiting for your input while background agents were still running. The new line reports those tasks as running. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.269]

## Three buckets, one owner

Laravel and Vue work on this desk still runs coding agents next to cron: a remote session on a small host, a headless `-p` job in CI, a background review while I write a field note. Mixing “needs a keypress,” “still running,” and “chat said done” into one “the agent is waiting” thread is how a junior turns a live child into a closed laptop.

| Bucket | What it means | What you do | Owner |
| --- | --- | --- | --- |
| Needs input | A person must answer | Stay. Reply. Or name who will | Named human on the host |
| Working | A background session is live | Do not call it done. Open logs | Named human who pinned the CLI |
| Completed | The session ended | Then check the file on disk | Named human who owns the artifact |

Do not paste one screenshot and call every row done. If the line names a question, you are on Needs input. If a child is still in Working, you are not done. If chat said done and the shipping file is yesterday’s version, you already have a different ticket: recovered means a file, a log, and one fail-once restart. See [Building a Background Agent Recovery CLI: The Three-Gate Check](/blog/building-a-background-agent-recovery-cli-the-three-gate-check/).

{{< details summary="Pins are evidence, not the hook" >}}
The wait-line fix landed in the 11 September 2026 GitHub release, published 19:17 UTC, not a prerelease. This morning’s npm registry, 13 September 2026: `@anthropic-ai/claude-code` `latest` and `next` are 2.1.270 (published 12 September 2026). `stable` is still 2.1.236. Changelog for 2.1.270 is a follow-up: read-only git commands in Bash were asking for permission after a long session, a regression from the 11 September line. Pin what you run. Do not treat `latest` as `stable`. Do not put those numbers in the title. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.269] [Source: https://code.claude.com/docs/en/changelog] [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous host is ordinary: a remote Claude session left open on a small box, a headless review in CI, and a junior who reads “waiting for your input” as permission to shut the lid. I treat the CLI pin as a named owner’s artifact, the same way I treat a migration. The person who owns [/ai-agent-operations/](/ai-agent-operations/) on this desk also owns “which host loaded which CLI.” A coding agent does not get to hide a Working row so standup looks quiet. I already wrote the sibling rule for a requested-scope list that is not a status page. This is the sibling for a wait line that is not a finished child.
{{< /field-note >}}

## What the agent list actually shows

I do not invent a fake dashboard. I use the public commands.

Agent view is one screen for background sessions: what is running, what needs your input, and what is done. Dispatch a new session from the shell. Watch state without scrolling a transcript. Step in only when a row needs you. Each background session is a full conversation that keeps running without a terminal attached. [Source: https://code.claude.com/docs/en/agent-view]

From your shell:

```bash
claude agents
```

Dispatch a review as a background session, then keep the parent free:

```bash
claude --agent code-reviewer --bg "address review comments on PR 1234"
```

The CLI prints a session id and the follow-up commands. Official docs show the same pattern for resume:

```bash
claude --resume 1f0e2c9a-6d0b-4c11-9f39-2a77c1d4e8b5 --bg "pick up where you left off and finish the migration"
```

Then you manage the child with the commands the launch line already named: `claude attach <id>` to open it in this terminal, `claude logs <id>` for recent output, `claude stop <id>` to stop it. [Source: https://code.claude.com/docs/en/agent-view]

The footer in a regular session counts background agents waiting on you, such as `← 2 agents`. Row summaries show the session’s own one-line report. For a session waiting on you, the peek panel shows the exact question above the reply input. A turn with no readable text keeps the session’s previous state instead of flipping it back to Working. [Source: https://code.claude.com/docs/en/agent-view]

Write three sentences on the ticket, in this order:

1. What the parent printed: waiting, running, or completed.
2. What `claude agents` actually lists: Needs input count, Working count, Completed count.
3. Who owns the host and the CLI pin, and whether that owner will leave Working rows alive.

If you skip sentence two, you will file a “stuck waiting” ticket for a child that is still compiling.

## Headless is a different machine

Juniors glue remote, headless, and interactive into one “background Claude.” They are not the same pin.

Interactive and remote sessions can show agent view. Headless `-p` is a script. Official headless docs reject `--bg` with `-p`. The conflict is named in the error. Do not paste `--bg` onto a CI line and call it the same as a remote child. [Source: https://code.claude.com/docs/en/headless]

A one-off print run:

```bash
claude -p "What does the auth module do?"
```

Claude Code exits 0 on success and non-zero on failure. Scripts branch on that status. That exit is not a background-agent list. It is a process result.

If Claude starts a background Bash task during `claude -p`, for example a dev server or a watch build, that shell is terminated about five seconds after Claude has returned its final result and stdin has closed. If Claude starts a background subagent or workflow, `claude -p` stays open until that work completes, because the result is part of the final output. By default the wait ends after 10 minutes of continuous idle waiting. At that point Claude Code stops whatever is still running and drops its partial result. [Source: https://code.claude.com/docs/en/headless]

That 10-minute ceiling is a safety valve, not a “job finished” badge. A partial result after the cap is a failed wait, not a recovered artifact.

{{< note type="danger" title="Do not treat a wait ceiling as success" >}}
If a `-p` run stops because the idle wait hit the cap, copy the partial result and fail the job. Do not mark the pipeline green because the process exited.
{{< /note >}}

Unattended runs have a second trap: a permission prompt with nobody at the keyboard. Official docs tell you to pass `--permission-prompts none` when nobody can answer, for example in a scheduled job. Anything that would prompt is denied unless a PermissionRequest hook allows it. Claude is told that nobody can approve the request and not to retry it. The flag requires a recent CLI. Earlier versions reject it as an unknown option. [Source: https://code.claude.com/docs/en/headless]

That flag is not “Full-Auto merge.” It is “do not sit on a prompt until Monday.” Merge rights stay a human seat. See [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/) if your team still treats the model that wrote the PR as the merge gate.

## A small classifier you can paste on the ticket

I want a junior to classify a captured status line without opening a vendor screenshot thread. Save the agent-list dump the host actually printed. Then score it.

```python
from pathlib import Path

raw = Path("agent-list.txt").read_text(encoding="utf-8")
lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

needs = sum(1 for ln in lines if ln.lower().startswith("needs input") or "waiting for your input" in ln.lower())
working = sum(1 for ln in lines if ln.lower().startswith("working"))
done = sum(1 for ln in lines if ln.lower().startswith("completed"))

if working:
    print("CLASS=working_child")
    print("Do not call the job finished. Open logs. Ping the CLI-pin owner.")
elif needs:
    print("CLASS=needs_input")
    print("Stay. Answer, or name who will.")
elif done and not working and not needs:
    print("CLASS=list_empty_or_completed")
    print("Then check the file on disk. Chat is not the artifact.")
else:
    print("CLASS=unknown")
    print("Re-run claude agents. Do not guess from a wait line.")
```

This script does not talk to the network. It does not hide a Working row. It forces three buckets onto the ticket. If your dump uses different headings, fix the dump, not the buckets. Official agent view still groups Needs input, Working, and Completed. [Source: https://code.claude.com/docs/en/agent-view]

A second check belongs next to it: the binary you actually ran.

```bash
claude --version
```

Write that string next to the named owner. This morning `latest` and `next` can sit ahead of `stable`. A host that still runs `stable` will not show the wait-line fix. A host that jumped to `latest` picked up the 12 September git-permission follow-up. Neither tag is a reason to skip the agent list. [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code] [Source: https://code.claude.com/docs/en/changelog]

![Wait line, classify, not done — job-done stamp crossed out](/img/waiting-for-input-is-not-finished-2.png)

## What the coding agent is allowed to do

The agent’s first idea is always the same: make the wait line go away. Quiet status. Hide the child. Export an env so standup looks idle.

Forbidden on this desk:

1. Treat “waiting for your input” as a finished background agent.
2. Close the remote host, or kill the headless process, while Working rows still exist.
3. Write a hide-status recipe so the old wait line comes back. Official notes name an env that restores the old behavior. I do not put that env on a wiki card as a “quiet the spinner” trick. A lying wait line is worse than a noisy Working row. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.269]
4. Paste `--bg` onto `claude -p`. Headless rejects that pair. [Source: https://code.claude.com/docs/en/headless]
5. Mark a 10-minute wait-ceiling exit as recovered.

Allowed:

1. Print `claude --version` on the ticket.
2. Run `claude agents` and copy Needs input / Working / Completed.
3. Run `claude logs <id>` on every Working row.
4. Stop, and ping the named owner of the host and the CLI pin.

I already refused to leave an org-policy why-line unread. Same instinct: a status sentence is a ticket, not a pass. See [Read the Why-Line Before You Trust the Org Policy](/blog/org-policy-why-line/).

## SIGTERM is not a clean stop

Headless docs split signals. If you stop a `claude -p` run with SIGTERM, for example with `kill` or from a process supervisor, Claude Code exits with code 143. The turn in progress is left unfinished. No result is recorded for it. To end the turn instead, send SIGINT, or call the Agent SDK’s `interrupt()`, before you stop the process. [Source: https://code.claude.com/docs/en/headless]

On SIGTERM, Claude Code terminates the process tree of any Bash command that is still running, runs SessionEnd hooks, and exits. If it was waiting for an answer to a permission prompt, SIGTERM leaves the prompt unanswered.

When you resume, Claude Code continues the turn that SIGTERM left unfinished. That is the opposite of “we killed it, so it is done.”

Write the signal on the ticket. 143 is not 0. A supervisor that sends SIGTERM on deploy is a different owner from the person who reads agent view.

{{< note type="note" title="Resume is not recovered" >}}
A resumed turn after SIGTERM is still that turn. Check the file on disk before you tell standup the job finished overnight.
{{< /note >}}

## Merge is not a reason to skip the owner

Background agents are cheap to start. They are not cheap to own.

Juniors hear “background” and think the host can run without a name on the wiki card. Then Friday arrives and nobody knows which box still has Working rows.

I write the owner as a person, not a role. “Platform” is how these hosts stay half-watched until a wait line ships as done.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tool pins live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the agent is touching that stack. A first-week map is at [/start-here/](/start-here/). Do not mix those hubs into the wait-line row.

I already refused to treat a green package bump as ownership of the next repair. Same here. A changelog bullet about wait lines is not permission to skip `claude agents`.

![Version, agent list, logs, named human — not done](/img/waiting-for-input-is-not-finished-3.png)

## What you should do Monday morning

1. Open the remote or headless host the team actually uses. Run `claude --version`. Write the string on the ticket next to one human name. That person owns the CLI pin.
2. Run `claude agents`. Count Needs input, Working, and Completed. If Working is greater than zero, the job is not finished. Do not close the lid.
3. For every Working id, run `claude logs <id>`. Paste the last useful lines into the ticket. Do not summarize from memory.
4. If a row is Needs input, answer it or name who will. Do not leave a permission prompt on a host nobody watches.
5. For `-p` jobs, confirm you did not pass `--bg`. Confirm unattended runs use `--permission-prompts none` so a prompt cannot sit until Monday. Confirm a wait-ceiling exit fails the pipeline.
6. If a supervisor killed a run, check the exit code. 143 after SIGTERM is an unfinished turn. Resume is not recovered. Then apply the three-gate check: file on disk, job log, one fail-once restart.

The question is not whether this demos well in chat. The question is whether the wait line survives maintenance, handoff, and a child that is still running.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.269" label="GitHub release — wait line vs running background agents (11 September 2026)" >}}

{{< source href="https://code.claude.com/docs/en/agent-view" label="Claude Code docs — agent view, Needs input / Working / Completed" >}}

{{< source href="https://code.claude.com/docs/en/headless" label="Claude Code docs — headless -p, background wait ceiling, SIGTERM" >}}
