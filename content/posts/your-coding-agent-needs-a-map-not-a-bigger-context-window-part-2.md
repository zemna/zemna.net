---
title: "Your Coding Agent Needs a Map, Not a Bigger Context Window — Part 2"
date: 2026-08-21T07:00:00+07:00
lastmod: 2026-09-01T07:00:00+07:00
draft: false
topics: ["ai-agents"]
tags: ["context-engineering", "code-graphs", "artifact-contracts", "repo-map", "allow-list"]
cover: /covers/context-window-critique-2.png
description: "A bigger context window still lets a coding agent search the whole tree. Put the map file on the ticket as an allow-list, fail out-of-map paths, and name who updates the list."
seo:
  primaryQuery: "coding agent repository map"
  secondaryQueries:
    - "coding agent context window vs code graph"
    - "AGENTS.md allow-list for coding agents"
    - "artifact contracts agent reliability"
---

The agent grepped the whole Laravel app, opened a sibling Vue folder, and "fixed" shipping in a helper nobody called from the failing test. The PR looked busy. The bug was still in `app/Services/ShippingCost.php`.

That is the failure I now refuse. A bigger context window does not make a coding agent safer. It makes the wrong search cheaper. The map file is the allow-list. I do not let the agent search the whole tree. Paths outside the map fail the job.

The question is not whether this demos well. The question is whether it survives the next review, the next handoff, and the person who has to revert the branch.

<!--more-->

![The map file is the allow-list; out of map fails](/img/context-window-critique-2-1.png)

## The map is not a hint. It is the ticket.

Part 1 argued that agents need a repository map more than a larger window. That page is still live: [Your Coding Agent Needs a Map, Not a Bigger Context Window](/blog/your-coding-agent-needs-a-map-not-a-bigger-context-window/). This page is the desk rule that came after: **the map is an allow-list with a named owner.**

Vendors still sell tokens. OpenAI's GPT-5.5 API lists a 1,050,000-token context window at $5 per 1M input tokens and $30 per 1M output tokens [Source: https://developers.openai.com/api/docs/models/gpt-5.5]. That is evidence, not the title. I do not pin a model name on a ticket because a window grew. I pin the files the agent may read.

`AGENTS.md` is the common name for that brief. It is a README for agents: build commands, tests, conventions, and constraints a human README should not carry. The closest file to the edit wins; a chat prompt overrides it [Source: https://agents.md/]. I use that file as the **list of paths**, not as a vibe essay.

| What the ticket says | What the agent often does | What I require |
| --- | --- | --- |
| "Look around the shipping code" | Recursive search from repo root | Paths listed in the map file |
| "You have the whole repo in context" | Opens sibling apps and env samples | Out-of-map path = fail |
| "Follow AGENTS.md" | Skims it, then greps anyway | Map checked before first search |
| "Someone will update the list later" | List rot | Named human who owns the file |

If the list is missing, I stop. Abort is not stop. Abort still needs a retry owner, a next time, and an artifact. I already ranked that kind of refusal in [Five Things I Refused This Week](/blog/five-refusals-this-week/). Here the artifact is the map itself.

{{< note type="warning" title="Search is not the map" >}}
A recursive search from the repo root is not "being thorough." It is leaving the ticket. If a path is not on the map, the run failed even if the tests later pass.
{{< /note >}}

## Fail the job when the agent leaves the map

Juniors get hurt here because search tools feel harmless. `rg ShippingCost` looks like due diligence. In a monorepo it is how you pull `storage/logs`, a sibling package, or yesterday's dump into the prompt.

I keep a small fixture next to the app so a one-year developer can run it without learning a vendor's internals. It reads the map file, records every path the agent opened, and fails if any path sits outside the list.

```bash {linenos=inline,hl_lines=[18,"24-27"]}
#!/usr/bin/env bash
# scripts/assert-agent-map.sh
# Usage: assert-agent-map.sh MAP_FILE OPENED_PATHS_FILE
set -euo pipefail

MAP="${1:?map file required}"
OPENED="${2:?opened-paths file required}"

if [[ ! -f "$MAP" ]]; then
  echo "FAIL: map file missing: $MAP" >&2
  exit 1
fi

mapfile -t allowed < <(grep -E '^[-*][[:space:]]+' "$MAP" | sed 's/^[-*][[:space:]]*//; s/[[:space:]]*$//')
if [[ ${#allowed[@]} -eq 0 ]]; then
  echo "FAIL: map file has no path bullets" >&2
  exit 1
fi

fail=0
while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  ok=0
  for a in "${allowed[@]}"; do
    case "$path" in
      "$a"|"$a"/*) ok=1; break ;;
    esac
  done
  if [[ "$ok" -ne 1 ]]; then
    echo "FAIL: out-of-map path: $path" >&2
    fail=1
  fi
done < "$OPENED"

if [[ "$fail" -eq 1 ]]; then
  exit 1
fi
echo "PASS: every opened path is on the map"
```

The opened-paths file is the log, not a memory. If the harness cannot print the files it read, I treat the run as unread. Same rule as [Long-Running AI Agents — From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/): a green session is not a surviving boundary.

A map file that only says "be careful" is not a map. I want bullets the fixture can parse:

```markdown
# Agent map — shipping cost ticket

Owner: shinjae
Test: php artisan test --filter=ShippingCostTest

Allowed paths:
- app/Services/ShippingCost.php
- app/Http/Controllers/CheckoutController.php
- tests/Feature/ShippingCostTest.php
- AGENTS.md
```

Four paths. Not the Vue admin. Not `database/seeders`. Not `.env.example` one directory up. If the agent needs another file, it asks the owner to add a line. That line is the review.

![Named owner, not the agent](/img/context-window-critique-2-2.png)

## Who owns the file list

"The agent" is not an owner. "Auto" is not an owner. The owner is the person who will revert the branch if the map was wrong.

I put the name in the map file and on the ticket. When the list is stale, blame is a file, not a chat.

| Fact | Fake owner | Real owner |
| --- | --- | --- |
| Who may add a path? | Whoever is in the session | Named human on the ticket |
| Who may search outside? | Nobody, including me in a hurry | Still nobody |
| Who updates AGENTS.md after a new package? | "We'll remember" | Same named human, in the same PR |
| Who signs the merge? | Not the agent | Same as [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/) |

I do not let the agent edit `AGENTS.md` to enlarge its own list. That is the same refusal as letting it pick its own model. The map is policy. Policy lives in git. A session that rewrites policy is a session that already left the ticket.

{{< field-note title="Field note" >}}
On a Modoo Laravel SaaS checkout, the failing test named `ShippingCostTest`. The agent still opened `resources/js` because the prompt said "the app." Token spend looked fine. The helper it patched was dead code. After that, the ticket started with four bullets and a name. Out-of-map paths fail CI before anyone argues about the diff. Maintenance is the list, not the model.
{{< /field-note >}}

How the opened-paths log gets written is boring on purpose. Wrap the search tool. If the harness already prints tool calls, scrape those paths into `artifacts/opened-paths.txt` at the end of the run. If it does not, the junior on the ticket pastes the files they saw in the trace. Empty log fails. A log that only contains the map file also fails, because then the agent never read the production code.

I keep the log next to the patch, not in chat. Chat scrolls. Git blame does not. When a reviewer asks "why did this agent touch the Vue folder," the answer is a line in the log or it is a process bug.

## Context windows still do the wrong job

Model vendors sell a larger haystack. You still need the needle on a card.

GPT-5.5's API window is 1,050,000 tokens; Codex's GPT-5.5 window is listed separately at 400K on the product page [Source: https://openai.com/index/introducing-gpt-5-5/]. I do not care which number wins the slide. Both numbers are large enough to ingest a medium app, the lockfile, CI YAML, and last week's chat. That is how invariants fall out of the middle.

```
# What a big-window agent often loads
- every PHP class under app/
- Vue files from a sibling folder
- lockfiles and CI
- the last 40 chat turns

# What the shipping bug needed
- ShippingCost.php
- CheckoutController.php
- ShippingCostTest.php
- the assertion that failed in CI
```

Context rot is the name for that drift: a five-minute task holds the right files; a three-day task does not. The industry label is context engineering: control what the agent may see at each step, instead of stuffing the repo [Source: https://sourcegraph.com/blog/context-engineering]. My translation for a junior: **write the allow-list first, then open files.**

I have watched a long session "remember" a file it opened on day one and ignore the test that failed on day two. The window was not full. The attention was. A map file does not fix attention. It makes the miss visible: the opened-paths log either contains `tests/Feature/ShippingCostTest.php` or the contract fails before anyone thanks the model.

A compiler-backed code graph is a later upgrade, not the Monday move. TypeScript teams can query symbols instead of grepping; one public example is the TypeScript compiler graph package under `samchon/ttsc` [Source: https://github.com/samchon/ttsc/tree/master/packages/graph]. Use it after the map file exists. Do not skip the list because a graph demo looked smart.

![Map check, then test, then ping](/img/context-window-critique-2-3.png)

## Prove the artifact before you ping success

Your job is not healthy because the process exited zero. It is healthy when the expected file exists, is fresh, has substance, and passes a domain check. I already wrote that as [Your Cron Job Is Not Healthy Until the Artifact Proves It](/blog/your-cron-job-is-not-healthy-until-the-artifact-proves-it/). The same four questions apply to an agent run.

1. **Path** — the map file, the opened-paths log, and the production file that should change.
2. **Freshness** — mtime after the run started, not last week's map.
3. **Substance** — the map has path bullets; the log is not empty.
4. **Assertion** — `assert-agent-map.sh` passed; the named test passed.

```typescript
interface AgentMapContract {
  mapFile: string;           // "AGENTS.md" or "docs/agent-map-shipping.md"
  openedPathsLog: string;    // "artifacts/opened-paths.txt"
  owner: string;             // git username, not "agent"
  testCommand: string;       // "php artisan test --filter=ShippingCostTest"
}

async function onAgentComplete(c: AgentMapContract): Promise<boolean> {
  const map = await fs.readFile(c.mapFile, "utf8");
  if (!/Allowed paths:/i.test(map)) return false;
  if (!(await run("scripts/assert-agent-map.sh", [c.mapFile, c.openedPathsLog]))) {
    return false;
  }
  if (!(await runShell(c.testCommand))) return false;
  return true;
}
```

Only then ping Healthchecks. The Hobbyist plan is $0 and monitors 20 jobs [Source: https://healthchecks.io/pricing/]. Ping after the contract, not after `exit 0`.

Sentry's Developer plan is free, one user, and 5k errors [Source: https://sentry.io/pricing/]. That is enough to see crashes. It is not a substitute for the map fixture. Cron monitoring on that plan is one monitor. Do not pretend the free error quota is a cron farm.

{{< note type="success" title="Contract before ping" >}}
A success ping before the map check means the process ended. A success ping after the map check means the agent stayed inside the ticket.
{{< /note >}}

## Alerts belong in git, not in a personal console

When the fixture fails, I want a reviewable rule, not a screenshot of someone's phone. Alerting as code treats the rule as a PR: visible, revertible, dated [Source: https://engineering.ab180.co/stories/standardizing-alert-system-with-iac/].

```yaml
# alerts/agent-map.yaml
groups:
  - name: agent-map
    rules:
      - alert: AgentLeftTheMap
        expr: increase(agent_out_of_map_path_total[15m]) > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Agent left the allow-list"
          runbook: "Open the map file. Add a path or revert."
      - alert: AgentMapMissing
        expr: agent_map_file_present == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "No map file on the ticket"
```

I do not start with a custom dashboard. I start with the fixture in CI. Dashboards come after the fail is boring.

## What you can delete this quarter

Same energy as deleting JS you replaced with CSS: delete the prompt that says "search the repo." Replace it with four bullets and a name.

| Habit | Replacement | Why |
| --- | --- | --- |
| "Read the whole app" | Map file with path bullets | Search becomes a bug |
| Similarity search from root | Code graph after the list exists | Ranking is not permission |
| Success on exit code | Map fixture + named test | Green is not in-scope |
| Agent edits AGENTS.md | Owner PR | Policy is not self-serve |
| Personal alert toggle | YAML in git | Next on-call can read it |

```bash
#!/usr/bin/env bash
# scripts/audit-unmapped-search.sh
set -euo pipefail
TARGET="${1:-.}"
echo "=== Prompts that still say search the whole tree ==="
grep -RInE 'search the (whole |entire )?(repo|repository|codebase)|all files' \
  "$TARGET" --include='*.md' --include='*.txt' --include='*.yml' || true
echo "=== Agent maps missing an Owner line ==="
find "$TARGET" -name 'AGENTS.md' -o -name '*agent-map*.md' | while read -r f; do
  if ! grep -qE '^Owner:' "$f"; then
    echo "NO OWNER: $f"
  fi
done
```

Run it on the repo you will touch this week, not on a hypothetical monorepo.

![Monday checklist: map file, four paths, named owner, fail out of map](/img/context-window-critique-2-4.png)

## What you should do Monday morning

1. **Put a map file on the open ticket.** Name the owner. List four to eight paths. If you cannot list them, you are not ready to start the agent.

2. **Add `scripts/assert-agent-map.sh` to CI** on that branch. Feed it the map and the opened-paths log. A missing log is a fail.

3. **Fail out-of-map paths before review.** Do not argue the diff if the fixture already failed. Expand the list in a separate commit with a human name.

4. **Stop the agent from editing the map.** Same PR can update code. The map change needs the owner. If the owner is on leave, the run waits.

5. **Move the success ping behind the fixture.** Healthchecks Hobbyist covers 20 jobs at $0. Ping after PASS, not after the process dies.

6. **Link the three pages your team will actually open:** this Part 2, [Part 1](/blog/your-coding-agent-needs-a-map-not-a-bigger-context-window/), and the [AI agent operations hub](/ai-agent-operations/). If a junior cannot find the allow-list rule from the hub, the hub is wrong.

7. **Delete one "search the repo" sentence** from your agent prompt today. Do not leave dead instructions next to the map. Dead instructions win.

If you only have thirty minutes, do steps 1 and 2. A map without CI is a sticky note. CI without a map is a grep of the whole tree with extra steps. Do both on the same branch. Merge rights stay with the human, same as the merge-rights post. The agent does not get a bonus path because the test went green.

## Further reading

- {{< source href="https://agents.md/" label="AGENTS.md — README for coding agents" >}}
- {{< source href="https://developers.openai.com/api/docs/models/gpt-5.5" label="OpenAI API — GPT-5.5 context window and price" >}}
- {{< source href="https://sourcegraph.com/blog/context-engineering" label="Sourcegraph — Context engineering" >}}

Internal: [Part 1 — repository map](/blog/your-coding-agent-needs-a-map-not-a-bigger-context-window/) · [Long-running agents](/blog/long-running-ai-agents-from-demos-to-production/) · [AI agent operations](/ai-agent-operations/) · [Developer tools](/developer-tools/) · [Start here](/start-here/)
